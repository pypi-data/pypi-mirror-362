# -*- coding: UTF-8 -*-
# Copyright 2008-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Defines extended database field classes and utility functions
related to fields.
"""

#fmt: off

import datetime
from decimal import Decimal

from django import http
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import format_lazy
from django.core.exceptions import ValidationError
from django.core.exceptions import FieldDoesNotExist
from django.db.models.fields import NOT_PROVIDED
from django.utils.functional import cached_property

from lino import logger
if settings.SITE.is_installed("contenttypes"):
    from lino.modlib.gfks.fields import GenericForeignKey
from lino.utils.html import E, forcetext, tostring, SafeString, escape, mark_safe

from lino.core.utils import (
    resolve_field,
    full_model_name,
    resolve_model,
    ParameterPanel,
)
from lino.core.exceptions import ChangedAPI
from lino.core.diff import ChangeWatcher
from lino.core import constants
from lino.core import atomizer

from lino.utils import isiterable
from lino.utils import choosers
# from lino.utils import get_class_attr
from lino.utils import IncompleteDate
from lino.utils import quantities
from lino.utils.quantities import Duration
# from lino.modlib.gfks.fields import GenericForeignKeyIdField

from .signals import pre_ui_save


def none_getter(obj, ar=None):
    return None


def validate_incomplete_date(value):
    """Raise ValidationError if user enters e.g. a date 30.02.2009."""
    try:
        value.as_date()
    except ValueError:
        raise ValidationError(_("Invalid date"))


def set_default_verbose_name(f):
    """

    If the verbose_name of a ForeignKey was not set by user code, Lino sets it
    to the verbose_name of the model pointed to.  This rule holds also for
    virtual FK fields.

    For every FK field defined on a model (including virtual FK fields) this is
    called during kernel startup.  Django sets the `verbose_name` of every
    field to ``field.name.replace('_', ' ')``.

    For virtual FK fields defined on an actor or an action it is called a bit
    later. These fields don't have a name.

    """
    if f.verbose_name is None or (
            f.name is not None and f.verbose_name == f.name.replace("_", " ")):
        f.verbose_name = f.remote_field.model._meta.verbose_name


class PasswordField(models.CharField):
    """Stored as plain text in database, but not displayed in user
    interface.

    """

    pass


class RichTextField(models.TextField):
    # See :doc:`/dev/textfield`.

    def __init__(self, *args, **kw):
        # textfield_format was still accepted for backward compatibility
        # self.format = kw.pop('format', kw.pop('textfield_format', None))
        self.format = kw.pop("format", None)
        self.bleached = kw.pop("bleached", None)
        super().__init__(*args, **kw)

    def set_format(self, fmt):
        self.format = fmt


class PreviewTextField(RichTextField):
    pass


class PercentageField(models.DecimalField):
    """
    A field to express a percentage.
    The database stores this like a DecimalField.
    Plain HTML adds a "%".
    """

    def __init__(self, *args, **kwargs):
        defaults = dict(
            max_length=5,
            max_digits=5,
            decimal_places=0,
        )
        defaults.update(kwargs)
        super().__init__(*args, **defaults)


class TimeField(models.TimeField):
    """
    Like a TimeField, but allowed values are between
    :attr:`calendar_start_hour
    <lino.core.site.Site.calendar_start_hour>` and
    :attr:`calendar_end_hour <lino.core.site.Site.calendar_end_hour>`.
    """

    pass


class DatePickerField(models.DateField):
    """
    A DateField that uses a DatePicker instead of a normal DateWidget.
    Doesn't yet work.
    """

    pass


class MonthField(models.DateField):
    """
    A DateField that uses a MonthPicker instead of a normal DateWidget
    """

    pass
    # def __init__(self, *args, **kw):
    #     models.DateField.__init__(self, *args, **kw)


# def PriceField(*args, **kwargs):
#     defaults = dict(
#         max_length=10,
#         max_digits=10,
#         decimal_places=2,
#     )
#     defaults.update(kwargs)
#     return models.DecimalField(*args, **defaults)


class PriceField(models.DecimalField):
    """
    A thin wrapper around Django's `DecimalField
    <https://docs.djangoproject.com/en/5.2/ref/models/fields/#decimalfield>`_
    with price-like default values for `decimal_places`, `max_length` and
    `max_digits`.
    """

    # def __init__(self, verbose_name=None, max_digits=10, **kwargs):
    #     defaults = dict(
    #         max_length=max_digits,
    #         max_digits=max_digits,
    #         decimal_places=2,
    #     )
    #     defaults.update(kwargs)
    #     super().__init__(verbose_name, **defaults)

    def __init__(self, verbose_name=None, max_digits=10, **kwargs):
        defaults = dict(
            max_digits=max_digits,
            decimal_places=2,
        )
        defaults.update(kwargs)
        super().__init__(verbose_name, **defaults)


# from lino.core.utils import resolve_field
#
# class FieldRange(ParameterPanel):
#
#     def __init__(self, fldspec, **kwargs):
#         fld = resolve_field(fldspec)
#         self.start_field = dbfield2params_field(fld)
#         self.end_field = dbfield2params_field(fld)


class PriceRange(ParameterPanel):
    def __init__(self, field_name, verbose_name=_("Price"), **kwargs):
        self.field_name = field_name
        self.verbose_name = verbose_name
        kwargs["start_" + field_name] = PriceField(
            verbose_name=format_lazy(_("{} from"), verbose_name), blank=True, null=True
        )
        kwargs["end_" + field_name] = PriceField(
            verbose_name=_("to"), blank=True, null=True
        )
        super().__init__(**kwargs)

    def check_values(self, pv):
        start_value = getattr(pv, "start_" + self.field_name)
        if start_value is None:
            return
        end_value = getattr(pv, "end_" + self.field_name)
        if end_value is None:
            return
        if start_value > end_value:
            raise Warning(_("Invalid price range"))

    def get_title_tags(self, ar):
        pv = ar.param_values
        start_value = getattr(pv, "start_" + self.field_name)
        end_value = getattr(pv, "end_" + self.field_name)
        if start_value:
            if end_value:
                yield _("{} {}...{}").format(self.verbose_name, start_value, end_value)
            else:
                yield _("{} from {}").format(self.verbose_name, start_value)
        elif end_value:
            yield _("{} until {}").format(self.verbose_name, end_value)


# ~ class MyDateField(models.DateField):

# ~ def formfield(self, **kwargs):
# ~ fld = super(MyDateField, self).formfield(**kwargs)
# ~ # display size is smaller than full size:
# ~ fld.widget.attrs['size'] = "8"
# ~ return fld
"""
https://stackoverflow.com/questions/454436/unique-fields-that-allow-nulls-in-django
answer Dec 20 '09 at 3:40 by mightyhal
https://stackoverflow.com/a/1934764
"""

# class NullCharField(models.CharField):  # subclass the CharField
#     description = "CharField that stores empty strings as NULL instead of ''."

#     def __init__(self, *args, **kwargs):
#         defaults = dict(blank=True, null=True)
#         defaults.update(kwargs)
#         super(NullCharField, self).__init__(*args, **defaults)

#     # this is the value right out of the db, or an instance
#     def to_python(self, value):
#         # ~ if isinstance(value, models.CharField): #if an instance, just return the instance
#         if isinstance(value, six.string_types):  # if a string, just return the value
#             return value
#         if value is None:  # if the db has a NULL (==None in Python)
#             return ''  # convert it into the Django-friendly '' string
#         else:
#             return value  # otherwise, return just the value

#     def get_db_prep_value(self, value, connection, prepared=False):
#         # catches value right before sending to db
#         # if Django tries to save '' string, send the db None (NULL)
#         if value == '':
#             return None
#         else:
#             return value  # otherwise, just pass the value


class FakeField(object):
    """
    Base class for :class:`RemoteField` and :class:`DisplayField`.
    """

    _lino_atomizer = None
    model = None
    db_column = None
    choices = []
    primary_key = False
    editable = False
    name = None
    null = True
    serialize = False
    verbose_name = None
    help_text = None
    preferred_width = 30
    preferred_height = 3
    max_digits = None
    decimal_places = None
    default = NOT_PROVIDED
    generate_reverse_relation = False  # needed when AFTER17
    remote_field = None
    blank = True  # 20200425
    delayed_value = False
    max_length = None
    generated = False
    choicelist = None  # avoid 'DummyField' object has no attribute 'choicelist'
    hide_unless_explicit = True

    wildcard_data_elem = False
    """Whether to consider this field as wildcard data element.
    """

    sortable_by = None
    """
    A list of names of real fields to be used for sorting when this
    fake field is selected.  For remote fields this is set
    automatically, on virtual fields you can set it yourself.
    """

    # required by Django 1.8+:
    is_relation = False
    concrete = False
    auto_created = False
    column = None
    empty_values = set([None, ""])

    # required by Django 1.10+:
    one_to_many = False
    one_to_one = False

    # required since 20171003
    rel = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if not hasattr(self, k):
                raise Exception("{} has no attribute {}".format(self, k))
            setattr(self, k, v)

    def __repr__(self):
        # copied from django Field
        path = "%s.%s" % (self.__class__.__module__,
                          self.__class__.__qualname__)
        name = getattr(self, "name", None)
        if name is not None:
            return "<%s: %s>" % (path, name)
        return "<%s>" % path

    def is_enabled(self, lh):
        """
        Overridden by mti.EnableChild
        """
        return self.editable

    def clean(self, raw_value, obj):
        # needed for Django 1.8
        return raw_value

    def has_default(self):
        return self.default is not NOT_PROVIDED

    def get_default(self):
        return self.default

    def set_attributes_from_name(self, name):
        if not self.name:
            self.name = name
        self.attname = name
        self.column = None
        self.concrete = False
        # if self.verbose_name is None and self.name:
        #     self.verbose_name = self.name.replace('_', ' ')


class RemoteField(FakeField):
    """
    A field on a related object.

    Remote fields are created by :func:`lino.core.atomizer.create_atomizer`
    (which itself is called by :meth:`lino.core.model.Model.get_data_elem`) when
    needed.

    .. attribute:: field

        The bottom-level (leaf) field object.

    """

    # ~ primary_key = False
    # ~ editable = False

    def __init__(self, getter, name, fld, setter=None, **kwargs):
        # from lino.core import choicelists
        self.func = getter
        self.name = name
        self.attname = name
        # self.db_column = name  # 20200423
        self.field = fld
        # for k in ('verbose_name', 'help_text', 'blank', 'default', 'null'):
        #     kwargs.setdefault(k, getattr(fld, k))
        self.verbose_name = fld.verbose_name
        self.help_text = fld.help_text
        # self.blank = fld.blank
        self.blank = True
        self.default = None
        # self.null = fld.null
        # self.null = getattr(fld, 'null', None)
        self.max_length = getattr(fld, "max_length", None)
        self.max_digits = getattr(fld, "max_digits", None)
        self.decimal_places = getattr(fld, "decimal_places", None)
        self.sortable_by = [name]

        self.setter = setter
        if setter is not None:
            self.editable = True
            self.choices = getattr(fld, "choices", None)
        super().__init__(**kwargs)
        # ~ print 20120424, self.name
        # ~ settings.SITE.register_virtual_field(self)

        # The remote_field of a FK field has nothing to do with our RemoteField,
        # it is set by Django on each FK field and points to

        if isinstance(fld, VirtualField) and isinstance(
            fld.return_type, models.ForeignKey
        ):
            fld.lino_resolve_type()  # 20200425
            fk = fld.return_type
        # elif isinstance(fld, choicelists.ChoiceListField):
        #     self.choicelist = fld.choicelist
        #     fk = None
        elif isinstance(fld, models.ForeignKey):
            fk = fld
        else:
            fk = None
        if fk is not None:
            # if not fk.remote_field:
            #     raise Exception("20200425 {} has no remote_field".format(fk))
            self.remote_field = fk.remote_field
            atomizer.get_atomizer(self.remote_field, self, name)

    def __str__(self):
        # return "<RemoteField({})>".format(self.name)
        return self.name

    def value_from_object(self, obj, ar=None):
        """
        Return the value of this field in the specified model instance
        `obj`.  `ar` may be `None`, it's forwarded to the getter
        method who may decide to return values depending on it.
        """
        return self.func(obj, ar)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.value_from_object(instance)


class DisplayField(FakeField):
    """
    A field to be rendered like a normal read-only form field, but with
    plain HTML instead of an ``<input>`` tag.

    This is to be used as
    the `return_type` of a :class:`VirtualField`.

    The value to be represented is either some unicode text, a
    translatable text or a :mod:`HTML element <etgen.html>`.
    """

    choices = None
    blank = True  # 20200425
    drop_zone = None
    max_length = None

    def __init__(self, verbose_name=None, **kwargs):
        self.verbose_name = verbose_name
        super().__init__(**kwargs)

    # the following dummy methods are never called but needed when
    # using a DisplayField as return_type of a VirtualField

    def to_python(self, *args, **kw):
        return None
        # raise NotImplementedError(
        #     "{}.to_python({},{})".format(self.name, args, kw))

    def save_form_data(self, *args, **kw):
        raise NotImplementedError

    def value_to_string(self, *args, **kw):
        raise NotImplementedError

    def value_from_object(self, obj, ar=None):
        return self.default


class HtmlBox(DisplayField):
    """
    Like :class:`DisplayField`, but to be rendered as a panel rather
    than as a form field.
    """

    # Needed when the object passes through the process of params_values creation, as if this object were a choicelist
    empty_strings_allowed = True


class DelayedHtmlBox(HtmlBox):
    """

    A simple extension of :class:`HtmlBox` that uses the :class:`DelayedValue
    <lino.core.utils.DelayedValue>` for its related store field value.

    """

    def __init__(self, *args, **kwargs):
        kwargs.update(delayed_value=True)
        super().__init__(*args, **kwargs)


# class VirtualGetter(object):
#     """A wrapper object for getting the content of a virtual field
#     programmatically.

#     """

#     def __init__(self, vf, instance):
#         self.vf = vf
#         self.instance = instance

#     def __call__(self, ar=None):
#         return self.vf.value_from_object(self.instance, ar)

#     # def __get__(self, instance, owner):
#     #     return self.vf.value_from_object(instance, None)

#     def __getattr__(self, name):
#         obj = self.vf.value_from_object(self.instance, None)
#         return getattr(obj, name)

#     def __repr__(self):
#         return "<{0}>.{1}".format(repr(self.instance), self.vf.name)


class VirtualModel:
    def __init__(self, model):
        self.wrapped_model = model
        self._meta = model._meta


VFIELD_ATTRIBS = frozenset([
    "to_python", "choices", "save_form_data",
    "value_to_string", "max_length", "remote_field",
    "max_digits", "verbose_name", "decimal_places",
    "wildcard_data_elem", "blank"
])


def return_none(obj, ar):
    return None


class VirtualField(FakeField):
    """
    Represents a virtual field. Values of virtual fields are not stored
    in the database, but computed on the fly each time they get
    read. Django doesn't see them.

    A virtual field must have a `return_type`, which can be either a
    Django field type (CharField, TextField, IntegerField,
    BooleanField, ...) or one of Lino's custom fields
    :class:`DisplayField`, :class:`HtmlBox` or :class:`RequestField`.

    The `get` must be a callable which takes two arguments: `obj` the
    database object and `ar` an action request.

    The :attr:`model` of a VirtualField is the class where the field
    was *defined*. This can be an abstract model. The VirtualField
    instance does not have a list of the concrete models which use it
    (because they inherit from that class).
    """

    # simple_elem = False
    # """
    # Used in :meth:`get_field_options` to set :term:`front end` rendering options.
    # """

    def __init__(self, return_type, get=return_none, **kwargs):
        """
        Normal VirtualFields are read-only and not editable.
        We don't want to require application developers to explicitly
        specify `editable=False` in their return_type::

          @dd.virtualfield(dd.PriceField(_("Total")))
          def total(self, ar=None):
              return self.total_excl + self.total_vat
        """
        self.return_type = return_type  # a Django Field instance
        self.get = get

        # self.simple_elem = kwargs.get("simple_elem", self.simple_elem)

        # if isinstance(return_type, FakeField):
        #     sortable_by = return_type.sortable_by
        #     self.sortable_by = sortable_by
        #     if sortable_by and isinstance(sortable_by, list):
        #             sortable_by = sortable_by[0]
        #     self.column = sortable_by
        # for k in VFIELD_ATTRIBS:
        #     setattr(self, k, getattr(return_type, k, None))

        settings.SITE.register_virtual_field(self)
        super().__init__(**kwargs)

    def lino_resolve_type(self):
        """
        Called on every virtual field when all models are loaded.
        """

        f = self.return_type

        if isinstance(f, str):
            try:
                f = self.return_type = resolve_field(f)
            except Exception as e:
                raise Exception(
                    "Invalid return type spec {} for {} : {}".format(
                        f, self, e)
                )
        self.field = f

        if isinstance(f, FakeField):
            # sortable_by = f.sortable_by
            self.sortable_by = f.sortable_by
            if f.sortable_by is not None:
                assert isinstance(f.sortable_by, list)
                self.column = f.sortable_by[0]
            # if sortable_by and isinstance(sortable_by, list):
            #     sortable_by = sortable_by[0]

        # if isinstance(f, VirtualField):
        #     delegate = f.return_type
        # else:
        #     delegate = f

        if isinstance(f, models.ForeignKey):
            f.remote_field.model = resolve_model(f.remote_field.model)
            set_default_verbose_name(f)
            self.get_lookup = f.remote_field.get_lookup  # 20200425
            self.get_path_info = f.remote_field.get_path_info  # 20200425
            self.remote_field = f.remote_field

        for k in VFIELD_ATTRIBS:
            setattr(self, k, getattr(f, k, None))

        # copy help_text if it hasn't been set by help_texts_extractor
        if f.help_text and not self.help_text:
            self.help_text = f.help_text

        # if self.name == 'detail_pointer':
        #     logger.info('20170905 resolve_type 1 %s on %s',
        #                 self.name, self.verbose_name)

        # ~ removed 20120919 self.return_type.editable = self.editable
        # if self.name == 'detail_pointer':
        #     logger.info('20170905 resolve_type done %s %s',
        #                 self.name, self.verbose_name)

        # if self.name is None or self.model is None:
        #     return

        atomizer.get_atomizer(self.model, self, self.name)

        # print("20181023 Done: lino_resolve_type() for {}".format(self))

    def override_getter(self, get):
        self.get = get

    def attach_to_model(self, model, name):
        self.model = model
        self.name = name
        self.attname = name
        # if getattr(self.return_type, "model", False):
        if hasattr(self.return_type, "model"):
            # logger.info("20200425 return_type for virtual "
            #     "field %s has a model %s (not %s)", self, self.return_type.model, model)
            return
        self.return_type.model = VirtualModel(model)
        self.return_type.column = None
        self.return_type.name = name

        # if name == "overview":
        #     print("20181022", self, self.verbose_name)

        # ~ self.return_type.name = name
        # ~ self.return_type.attname = name
        # ~ if issubclass(model,models.Model):
        # ~ self.lino_resolve_type(model,name)

        # must now be done by caller code:
        # if AFTER17:
        #     model._meta.add_field(self, virtual=True)
        # else:
        #     model._meta.add_virtual_field(self)

        # if self.get is None:
        #     return
        # if self.get.func_code.co_argcount != 2:
        #     if self.get.func_code.co_argcount == 2:
        #         getter = self.get
        #         def w(fld, obj, ar=None):
        #             return getter(obj, ar)
        #         self.get = w
        #         logger.warning("DeprecationWarning")
        #     else:
        #         msg = "Invalid getter for VirtualField {}".format(self)
        #         raise ChangedAPI(msg)

        # ~ logger.info('20120831 VirtualField %s.%s',full_model_name(model),name)

    def __repr__(self):
        if self.model is None:
            return "{} {} ({})".format(
                self.__class__.__name__, self.name, self.verbose_name
            )
            # return super(VirtualField, self).__repr__()
        return "%s.%s.%s" % (self.model.__module__, self.model.__name__, self.name)

    def get_default(self):
        return self.return_type.get_default()
        # ~

    def has_default(self):
        return self.return_type.has_default()

    def unused_contribute_to_class(self, cls, name):
        # if defined in abstract base class, called once on each submodel
        if self.name:
            if self.name != name:
                raise Exception(
                    "Attempt to re-use %s as %s in %s"
                    % (self.__class__.__name__, name, cls)
                )
        else:
            self.name = name
            if self.verbose_name is None and self.name:
                self.verbose_name = self.name.replace("_", " ")
        self.model = cls
        cls._meta.add_virtual_field(self)
        # ~ cls._meta.add_field(self)

    def to_python(self, *args, **kwargs):
        return self.return_type.to_python(*args, **kwargs)

    # ~ def save_form_data(self,*args,**kw): return self.return_type.save_form_data(*args,**kw)
    # ~ def value_to_string(self,*args,**kw): return self.return_type.value_to_string(*args,**kw)
    # ~ def get_choices(self): return self.return_type.choices
    # ~ choices = property(get_choices)

    def set_value_in_object(self, ar, obj, value):
        """
        Stores the specified `value` in the specified model instance
        `obj`.  `request` may be `None`.

        Note that any implementation must return `obj`, and
        callers must be ready to get another instance.  This special
        behaviour is needed to implement
        :class:`lino.utils.mti.EnableChild`.
        """
        pass
        # if value is not None:
        #     raise NotImplementedError("Cannot write %s to field %s" %
        #                               (value, self))

    def value_from_object(self, obj, ar=None):
        """
        Return the value of this field in the specified model instance
        `obj`.  `ar` may be `None`, it's forwarded to the getter
        method who may decide to return values depending on it.
        """
        m = self.get
        # ~ print self.field.name
        # return m(self, obj, ar)
        return m(obj, ar)
        # try:
        #     return m(obj, ar)
        # except TypeError as e:
        #     return "{} : {}".format(self, e)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.value_from_object(instance, None)
        # return VirtualGetter(self, instance)

    def __set__(self, instance, value):
        return self.set_value_in_object(None, instance, value)

    def get_col(self, alias, output_field=None):
        if output_field is None:
            output_field = self
        if alias != self.model._meta.db_table or output_field != self:
            from django.db.models.expressions import Col

            return Col(alias, self, output_field)
        else:
            return self.cached_col

    @cached_property
    def cached_col(self):
        from django.db.models.expressions import Col

        return Col(self.model._meta.db_table, self)

    def select_format(self, compiler, sql, params):
        """
        Custom format for select clauses. For example, GIS columns need to be
        selected as AsText(table.col) on MySQL as the table.col data can't be
        used by Django.
        """
        return sql, params


class VirtualBooleanField(VirtualField):
    """An editable virtual boolean field."""

    editable = True

    def __init__(self, ref_attr, label=None, **kw):
        self.ref_attr = ref_attr
        return_type = models.BooleanField(label)
        VirtualField.__init__(self, return_type, None, **kw)

    def set_value_in_object(self, request, obj, value):
        if value is not None:
            setattr(obj, self.ref_attr, value)

    def value_from_object(self, obj, ar):
        return getattr(obj, self.ref_attr)


def virtualfield(return_type, **kwargs):
    """
    Decorator to turn a model method into a :class:`VirtualField`.
    """

    def decorator(fn):
        if isinstance(return_type, DummyField):
            rv = DummyField(return_type.get_default())
        else:
            rv = VirtualField(return_type, fn, **kwargs)
        rv.__doc__ = fn.__doc__
        return rv

    return decorator


class Constant(FakeField):
    """
    Deserves more documentation.
    """

    def __init__(self, text_fn, **kwargs):
        self.text_fn = text_fn
        super().__init__(**kwargs)


def constant():
    """
    Decorator to turn a function into a :class:`Constant`.  The
    function must accept one positional argument `datasource`.
    """

    def decorator(fn):
        return Constant(fn)

    return decorator


class RequestField(VirtualField):
    """
    A :class:`VirtualField` whose values are table action requests to
    be rendered as a clickable integer containing the number of rows.
    Clicking on it will open a window with the table.
    """

    def __init__(self, get, *args, **kw):
        kw.setdefault("max_length", 8)
        VirtualField.__init__(self, DisplayField(*args, **kw), get)


def displayfield(*args, **kw):
    """
    Decorator to turn a method into a :class:`VirtualField` of type
    :class:`DisplayField`.
    """
    return virtualfield(DisplayField(*args, **kw))


def htmlbox(*args, **kwargs):
    """
    Decorator shortcut to turn a method into a a :class:`VirtualField`
    of type :class:`HtmlBox`.
    """
    return virtualfield(HtmlBox(*args, **kwargs))


def delayedhtmlbox(*args, **kwargs):
    return virtualfield(DelayedHtmlBox(*args, **kwargs))


def requestfield(*args, **kw):
    """
    Decorator shortcut to turn a method into a a :class:`VirtualField`
    of type :class:`RequestField`.
    """

    def decorator(fn):
        # ~ def wrapped(*args):
        # ~ return fn(*args)
        # ~ return RequestField(wrapped,*args,**kw)
        return RequestField(fn, *args, **kw)

    return decorator


class CharField(models.CharField):
    """
    An extension of Django's `models.CharField`.

    Adds two keywords `mask_re` and `strip_chars_re` which, when using
    the ExtJS front end, will be rendered as the `maskRe` and `stripCharsRe`
    config options of `TextField` as described in the `ExtJS
    documentation
    <https://docs.sencha.com/extjs/3.4.0/#!/api/Ext.form.TextField>`__,
    converting naming conventions as follows:

    =============== ============ ==========================
    regex           regex        A JavaScript RegExp object to be tested against the field value during validation (defaults to null). If the test fails, the field will be marked invalid using regexText.
    mask_re         maskRe       An input mask regular expression that will be used to filter keystrokes that do not match (defaults to null). The maskRe will not operate on any paste events.
    strip_chars_re  stripCharsRe A JavaScript RegExp object used to strip unwanted content from the value before validation (defaults to null).
    =============== ============ ==========================

    Example usage::

      belgian_phone_no = dd.CharField(max_length=15, strip_chars_re='')

    """

    def __init__(self, *args, **kw):
        self.strip_chars_re = kw.pop("strip_chars_re", None)
        self.mask_re = kw.pop("mask_re", None)
        self.regex = kw.pop("regex", None)
        super().__init__(*args, **kw)


class QuantityField(models.CharField):
    """
    A field that accepts :class:`Quantity
    <lino.utils.quantities.Quantity>`, :class:`Percentage
    <lino.utils.quantities.Percentage>` and :class:`Duration
    <lino.utils.quantities.Duration>` values.

    Implemented as a CharField, which means that
    sorting or filter ranges may not work as expected,
    and you cannot use SUM or AVG agregators on quantity fields
    since the database does not know how to calculate sums from them.

    When you set `blank=True`, then you should also set `null=True`.

    """

    description = _("Quantity (Decimal or Duration)")
    # overflow_value = None

    def __init__(self, *args, **kw):
        kw.setdefault("max_length", settings.SITE.quantity_max_length)
        super().__init__(*args, **kw)
        if self.blank and not self.null:
            raise ChangedAPI(
                "When `blank` is True, `null` must be True as well.")

    # ~ def get_internal_type(self):
    # ~ return "CharField"

    def to_python(self, value):
        """
        Excerpt from `Django docs
        <https://docs.djangoproject.com/en/5.2/howto/custom-model-fields/#converting-values-to-python-objects>`__:

            As a general rule, :meth:`to_python` should deal gracefully with
            any of the following arguments:

            - An instance of the correct type (e.g., `Hand` in our ongoing example).
            - A string (e.g., from a deserializer).
            - `None` (if the field allows `null=True`)

        I'd add "Any value allowed for this field when instantiating a model."

        """
        if isinstance(value, quantities.Quantity):
            return value
        elif isinstance(value, Decimal):
            return quantities.Quantity(value)
        elif isinstance(value, str):
            return quantities.parse(value)
        elif value:
            # try:
            return quantities.Quantity(value)
            # except Exception as e:
            #     raise ValidationError(
            #         "Invalid value {} for {} : {}".format(value, self, e))
        return None

    def from_db_value(self, value, expression, connection, context=None):
        return self.to_python(value)
        # if value is None or value == '':
        #     return self.get_default()
        # return quantities.parse(value)

    # def get_db_prep_value(self, value, connection, prepared=False):
    #     return str(value) if value else ''

    def get_prep_value(self, value):
        if value is None:
            return ""
        return str(value)  # if value is None else ''

    def clean(self, raw_value, obj):
        # if isinstance(raw_value, quantities.Quantity):
        raw_value = self.to_python(raw_value)
        if raw_value is not None:
            raw_value = raw_value.limit_length(self.max_length, ValidationError)
        # if len(str(raw_value)) > self.max_length:
        #     if self.overflow_value:
        #         return self.overflow_value
        #     raise ValidationError(
        #         f"Cannot accept quantity {raw_value} "
        #         + f"because max_length is {self.max_length}")
        #     # print("20230129 Can't store {}={} in {}".format(self.name, raw_value, obj))
        #     # return -1
        return super().clean(raw_value, obj)


class DurationField(QuantityField):
    """
    A field that stores :class:`Duration
    <lino.utils.quantities.Duration>` values as CHAR.

    """

    def from_db_value(self, value, expression, connection, context=None):
        if value is None or value == "":
            return self.get_default()
        return Duration(value)

    def to_python(self, value):
        if isinstance(value, Duration):
            return value
        if value:
            # if isinstance(value, six.string_types):
            #     return Duration(value)
            return Duration(value)
        return None


class IncompleteDateField(models.CharField):
    """
    A field that behaves like a DateField, but accepts incomplete
    dates represented using
    :class:`lino.utils.format_date.IncompleteDate`.
    """

    default_validators = [validate_incomplete_date]

    def __init__(self, *args, **kw):
        kw.update(max_length=11)
        # msgkw = dict()
        # msgkw.update(ex1=IncompleteDate(1980, 0, 0)
        #              .strftime(settings.SITE.date_format_strftime))
        # msgkw.update(ex2=IncompleteDate(1980, 7, 0)
        #              .strftime(settings.SITE.date_format_strftime))
        # msgkw.update(ex3=IncompleteDate(0, 7, 23)
        #              .strftime(settings.SITE.date_format_strftime))
        kw.setdefault(
            "help_text",
            _(
                """\
Uncomplete dates are allowed, e.g.
"00.00.1980" means "some day in 1980",
"00.07.1980" means "in July 1980"
or "23.07.0000" means "on a 23th of July"."""
            ),
        )
        models.CharField.__init__(self, *args, **kw)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    # def get_internal_type(self):
    #     return "CharField"

    def from_db_value(self, value, expression, connection, context=None):
        return IncompleteDate.parse(value) if value else self.get_default()
        # if value:
        #     return IncompleteDate.parse(value)
        # return ''

    def to_python(self, value):
        if isinstance(value, IncompleteDate):
            return value
        if isinstance(value, datetime.date):
            # ~ return IncompleteDate(value.strftime("%Y-%m-%d"))
            # ~ return IncompleteDate(d2iso(value))
            return IncompleteDate.from_date(value)
        # if value:
        #     return IncompleteDate.parse(value)
        # return ''
        return IncompleteDate.parse(value) if value else ""

    # def get_prep_value(self, value):
    #     return str(value)

    def get_prep_value(self, value):
        return str(value) if value else ""
        # if value:
        #     return str(value)
        #     # return '"' + str(value) + '"'
        #     #~ return value.format("%04d%02d%02d")
        # return ''

    # ~ def value_to_string(self, obj):
    # ~ value = self._get_val_from_obj(obj)
    # ~ return self.get_prep_value(value)


class Dummy(object):
    pass


class DummyField(FakeField):
    """
    Represents a field that doesn't exist in the current configuration
    but might exist in other configurations.

    The "value" of a DummyField is always `None` or any other value to be
    optionally specified at instantiation.

    .. attribute:: dummy_value

        The value to be returned by this field. Default value is `None`.

    Usage examples:

    - The value of :attr:`lino.modlib.users.User.nickname` is always ``""`` when
      :data:`lino.modlib.users.with_nickname` is `False`.


    See e.g. :func:`ForeignKey` and :func:`fields_list`.
    """

    # choices = []
    # primary_key = False
    field = None  # Used e.g. to test whether it's a dummy field

    def __init__(self, dummy_value=None):
        super().__init__()
        self.dummy_value = dummy_value

    # def __init__(self, name, *args, **kw):
    #     self.name = name

    def __str__(self):
        return self.name or "unnamed DummyField"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.dummy_value

    def get_default(self):
        return self.dummy_value

    def contribute_to_class(self, cls, name):
        self.name = name
        v = getattr(cls, name, NOT_PROVIDED)
        if v is not NOT_PROVIDED:
            msg = (
                "{0} cannot contribute to {1} because it has already "
                "an attribute '{2}'."
            )
            msg = msg.format(self, cls, name)
            if settings.SITE.ignore_model_errors:
                logger.warning(msg)
            else:
                raise Exception(msg)
        setattr(cls, name, self)

    def set_attributes_from_name(self, k):
        pass


class RecurrenceField(models.CharField):
    """
    Deserves more documentation.
    """

    def __init__(self, *args, **kw):
        kw.setdefault("max_length", 200)
        models.CharField.__init__(self, *args, **kw)


def OneToOneField(*args, **kwargs):
    """
    Instantiate a :class:`django.db.models.OneToOneField` using :func:`pointer_factory`.
    """
    return pointer_factory(models.OneToOneField, *args, **kwargs)


def ForeignKey(*args, **kwargs):
    """
    Instantiate a :class:`django.db.models.ForeignKey` using
    :func:`pointer_factory`.
    """
    return pointer_factory(models.ForeignKey, *args, **kwargs)


class CustomField(object):
    """
    Mixin to create a custom field.

    It defines a single method :meth:`create_layout_elem`.
    """

    def create_layout_elem(self, base_class, layout_handle, field, **kw):
        """Return the widget to represent this field in the specified
        `layout_handle`.

        The widget must be an instance of the given `base_class`.

        `self` and `field` are identical unless `self` is a
        :class:`RemoteField` or a :class:`VirtualField`.

        """
        return None


class ImportedFields(object):
    """
    Mixin for models which have "imported fields".
    """

    _imported_fields = set()

    @classmethod
    def declare_imported_fields(cls, names):
        cls._imported_fields = cls._imported_fields | set(
            atomizer.fields_list(cls, names))
        # ~ logger.info('20120801 %s.declare_imported_fields() --> %s' % (
        # ~ cls,cls._imported_fields))


class TableRow(object):
    """Base class for everything that can be used as a table row."""

    _lino_default_table = None
    _widget_options = {}
    extra_display_modes = None
    """
    A set of extra display modes to make available on actors that use this model.

    See :ref:`dg.dd.table.extra_display_modes`.
    """

    pk = None

    hidden_columns = frozenset()
    """If specified, this is the default value for
    :attr:`hidden_columns<lino.core.tables.AbstractTable.hidden_columns>`
    of every `Table` on this model.

    """

    @classmethod
    def get_chooser_for_field(cls, fieldname):
        d = getattr(cls, "_choosers_dict", {})
        # if fieldname.endswith("__municipality"):
        # print("20200425 Model.get_chooser_for_field", cls, fieldname, d)
        return d.get(fieldname, None)

    @classmethod
    def setup_parameters(cls, params):
        """Inheritable hook for defining parameters for every actor on this model.

        Called at site startup once for each actor using this model.

        Toes not return anything. Receives a `dict` object `params` and is
        expected to update that `dict`, which will be used to fill the actor's
        :attr:`parameters`.

        See also :meth:`get_simple_parameters`.

        """
        pass

    @classmethod
    def get_simple_parameters(cls):
        """
        Return or yield a list of names of simple parameter fields of every
        actor that uses this model.

        When the list contains names for which no parameter field is
        defined, then Lino creates that parameter field as a copy of
        the database field of the same name.

        This is also called by :meth:`get_title_tags`, you don't need to
        manually define title tags for simple parameters.

        """
        return []

    @classmethod
    def param_defaults(self, ar, **kw):
        return kw

    @classmethod
    def get_title_tags(self, ar):
        return []

    @classmethod
    def get_default_table(self):
        """Used internally. Lino chooses during the kernel startup, for each
        model, one of the discovered Table subclasses as the "default
        table".

        """
        return self._lino_default_table  # set in dbtables.py

    @classmethod
    def get_data_elem(cls, name):
        return None

        # v = getattr(cls, name, None)
        # if isinstance(v, VirtualField):
        #     return v

        # return getattr(cls, name, None)

        # return get_class_attr(cls, name)

        # v = get_class_attr(cls, name)
        # if v is not None:
        #     if isinstance(v, fields.DummyField):
        #         return v
        #     raise Exception("Oops, {} on {} is {}".format(name, cls, v))

    @classmethod
    def override_column_headers(cls, ar, **headers):
        return headers

    @classmethod
    def disable_create(self, ar):
        return None

    def before_ui_save(self, ar, cw):
        # Needed for polls.AnswerRemarkField
        pass

    def get_master_data(self, ar, master_instance=None):
        # Needed for polls.AnswerRemarkField
        return

    def get_detail_action(self, ar):
        """
        Return the (bound) detail action to use for showing this database row in
        a detail window.  Return `None` when no detail window exists or the
        requesting user has no permission to see it.

        `ar` is the action request that asks to see the detail.
        If the action request's actor can be used for this model,
        then use its `detail_action`. Otherwise use the
        `detail_action` of this model's default table.

        When `ar` is `None`, the permission check is bypassed.

        If `self` has a special attribute `_detail_action` defined,
        return this.  This magic is used by
        :meth:`Menu.add_instance_action
        <lino.core.menus.Menu.add_instance_action>`.

        Usage example: :class:`courses.Course <lino_xl.lib.courses.Course>`
        overrides this to return the detail action depending on the
        :term:`activity layout`.

        """
        a = getattr(self, "_detail_action", None)
        # print("20201230 get_detail_action", ar.actor, ar.actor.model, self.__class__)
        # if a is not None:
        #     raise Exception("20230425")
        if a is None:
            if ar and ar.actor and ar.actor.model is self.__class__:
                a = ar.actor.detail_action
            else:
                # if ar and ar.actor and ar.actor.model:
                #     print("20170902 {} : {} is not {}".format(
                #         ar.actor, self.__class__, ar.actor.model))
                dt = self.__class__.get_default_table()
                if dt is not None:
                    a = dt.get_request_detail_action(ar)
                    # a = dt.detail_action
                # print(f"20250121 {ar} {ar.actor} {dt} {a}")
        if a is None or ar is None:
            return a
        if a.get_view_permission(ar.get_user().user_type):
            # raise Exception("20230425 {}".format(ar.actor))
            return a

    def get_choices_text(self, ar, actor, field):
        return self.as_str(ar)
        # return str(self)

    # @fields.displayfield(_("Description"))
    # @htmlbox(_("Overview"))
    @htmlbox()
    def overview(self, ar):
        if ar is None:
            return ""
        # return E.div(*forcetext(self.get_overview_elems(ar)))
        s = "".join(tostring(i) for i in self.get_overview_elems(ar))
        return SafeString("<div>{}</div>".format(s))

    @htmlbox()
    def list_item(self, ar):
        if ar is None:
            return escape(str(self))
        return self.as_paragraph(ar)

    @displayfield(_("Select multiple rows"), wildcard_data_elem=True)
    def rowselect(self, ar):
        """A place holder for primereact Datatable column "Selection Column\""""
        return None

    def get_overview_elems(self, ar):
        # return [ar.obj2html(self)]
        return [self.as_summary_item(ar)]

    def as_str(self, ar):
        # must return a str
        if ar.actor is None:
            return str(self)
        elif ar.actor.row_template is None or not isinstance(self, ar.actor.model):
            return " ".join(self.get_str_words(ar))
        return ar.actor.row_template.format(row=self)

    def get_str_words(self, ar):
        # must yield a sequence of str (or Promise)
        yield str(self)

    def as_summary_item(self, ar, text=None, **kwargs):
        # must return an ET element
        if ar is None:
            return text or str(self)
        if text is None:
            text = self.as_str(ar)
        return ar.obj2html(self, text, **kwargs)

    def as_paragraph(self, ar, **kwargs):
        # must return a safe html string
        if ar is None:
            return escape(str(self))
        return tostring(self.as_summary_item(ar, **kwargs))

    def as_tile(self, ar, prev, **kwargs):
        s = self.as_paragraph(ar, **kwargs)
        return constants.TILE_TEMPLATE.format(chunk=s)

    def as_story_item(self, ar, **kwargs):
        kwargs.update(display_mode=constants.DISPLAY_MODE_STORY)
        return mark_safe("".join(self.as_page(ar, **kwargs)))

    def as_page(self, ar, **kwargs):
        yield "<h1>{}</h1>".format(self)
        yield "<p>{}</p>".format(self.as_paragraph(ar))
        # yield "<p style=\"padding-left:1em\">{}</p>".format(self.as_paragraph(ar))
        # for e in self.get_overview_elems(ar):
        #     yield tostring(e)

    def save_existing_instance(self, ar):
        watcher = ChangeWatcher(self)
        # print("20210213 save_existing_instance", ar.ah, ar.rqdata, self.disabled_fields)
        ar.ah.store.form2obj(ar, ar.rqdata, self, False)
        self.full_clean()
        pre_ui_save.send(sender=self.__class__, instance=self, ar=ar)
        self.before_ui_save(ar, watcher)
        self.save_watched_instance(ar, watcher)

    @classmethod
    def get_layout_aliases(cls):
        """

        Yield a series of (ALIAS, repl) tuples that cause a name ALIAS in a
        layout based on this model to be replaced by its replacement `repl`.

        """
        return []

    @classmethod
    def set_widget_options(self, name, **options):
        # from lino.modlib.extjs.elems import FieldElement
        # for k in options.keys():
        #     if not hasattr(FieldElement, k):
        #         raise Exception("Invalid widget option {}".format(k))
        self._widget_options = dict(**self._widget_options)
        d = self._widget_options.setdefault(name, {})
        d.update(options)

    @classmethod
    def get_widget_options(self, name, **options):
        options.update(self._widget_options.get(name, {}))
        if name == self.pk:
            options.setdefault("detail_pointer", True)
        return options


def wildcard_data_elems(model):
    """
    Yield names to be used as wildcard in the :attr:`column_names` of a
    table or when :func:`fields_list` finds a ``*``.
    """
    meta = model._meta
    for f in meta.fields:
        # if not isinstance(f, fields.RichTextField):
        if isinstance(f, VirtualField):
            if f.wildcard_data_elem:
                yield f
        else:
            if not getattr(f, "_lino_babel_field", False):
                yield f
    for f in meta.many_to_many:
        yield f

    # private_fields are available at meta.fields on which we iterate
    # over just above, but, some field.is_relation are filtered out.
    for f in meta.private_fields:
        if settings.SITE.is_installed("contenttypes"):
            if isinstance(f, GenericForeignKey):
                yield f
    # todo: for slave in self.report.slaves


def use_as_wildcard(de):
    if de.name.endswith("_ptr"):
        return False
    return True


def pointer_factory(cls, othermodel, *args, **kw):
    """
    Instantiate a `ForeignKey` or `OneToOneField` with some subtle
    differences:

    - It supports `othermodel` being `None` or the name of some
      non-installed model and returns a :class:`DummyField` in that
      case. This is useful when designing reusable models.

    - Explicitly sets the default value for `on_delete
      <https://docs.djangoproject.com/en/5.2/ref/models/fields/#django.db.models.ForeignKey.on_delete>`__
      to ``CASCADE`` (as required by Django 2).

    """
    if othermodel is None:
        # return DummyField(othermodel, *args, **kw)
        return DummyField(None)
    if isinstance(othermodel, str):
        if not settings.SITE.is_installed_model_spec(othermodel):
            # return DummyField(othermodel, *args, **kw)
            return DummyField(None)

    kw.setdefault("on_delete", models.CASCADE)
    return cls(othermodel, *args, **kw)


# # would be nice for lino_xl.lib.vat.VatItemBase.item_total
# class FieldAlias(VirtualField):
#     def __init__(self, orig_name):
#         ...
#
#


def choices_for_field(ar, holder, field):
    """
    Return the choices for the given field and the given HTTP request
    whose `holder` is either a Model, an Actor or an Action.
    """
    if not holder.get_view_permission(ar.request.user.user_type):
        raise Exception(
            "{user} has no permission for {holder}".format(
                user=ar.request.user, holder=holder
            )
        )
    # model = holder.get_chooser_model()
    chooser = holder.get_chooser_for_field(field.name)
    # logger.info('20140822 choices_for_field(%s.%s) --> %s',
    #             holder, field.name, chooser)
    if chooser:
        qs = chooser.get_request_choices(ar, holder)
        if not isiterable(qs):
            raise Exception(
                "%s.%s_choices() returned non-iterable %r"
                % (holder.model, field.name, qs)
            )
        if chooser.simple_values:

            def row2dict(obj, d):
                d[constants.CHOICES_TEXT_FIELD] = str(obj)
                d[constants.CHOICES_VALUE_FIELD] = obj
                return d
        elif chooser.instance_values:
            # same code as for ForeignKey
            def row2dict(obj, d):
                d[constants.CHOICES_TEXT_FIELD] = holder.get_choices_text(
                    obj, ar, field)
                d[constants.CHOICES_VALUE_FIELD] = obj.pk
                return d
        else:  # values are (value, text) tuples
            def row2dict(obj, d):
                d[constants.CHOICES_TEXT_FIELD] = str(obj[1])
                d[constants.CHOICES_VALUE_FIELD] = obj[0]
                return d

        return (qs, row2dict)

    if field.choices:
        qs = field.choices

        def row2dict(obj, d):
            if type(obj) is list or type(obj) is tuple:
                d[constants.CHOICES_TEXT_FIELD] = str(obj[1])
                d[constants.CHOICES_VALUE_FIELD] = obj[0]
            else:
                d[constants.CHOICES_TEXT_FIELD] = holder.get_choices_text(
                    obj, ar, field)
                d[constants.CHOICES_VALUE_FIELD] = str(obj)
            return d

        return (qs, row2dict)

    if isinstance(field, VirtualField):
        field = field.return_type

    if isinstance(field, RemoteField):
        field = field.field
        if isinstance(field, VirtualField):  # 20200425
            field = field.return_type

    if isinstance(field, models.ForeignKey):
        m = field.remote_field.model
        t = m.get_default_table()
        # qs = t.create_request(request=ar.request).data_iterator
        qs = t.create_request(parent=ar).data_iterator
        # logger.info('20120710 choices_view(FK) %s --> %s', t, qs.query)

        def row2dict(obj, d):
            d[constants.CHOICES_TEXT_FIELD] = holder.get_choices_text(
                obj, ar, field)
            d[constants.CHOICES_VALUE_FIELD] = obj.pk
            return d
    # elif isinstance(field, GenericForeignKeyIdField):
    #     ct = getattr(ar.selected_rows[0], field.type_field)
    #     m = ct.model_class()
    #     # print(f"20250511 {field.remote_field} {repr(field.type_field)}")
    #     t = m.get_default_table()
    #     qs = t.create_request(parent=ar).data_iterator
    #
    #     def row2dict(obj, d):
    #         d[constants.CHOICES_TEXT_FIELD] = holder.get_choices_text(
    #             obj, ar, field)
    #         d[constants.CHOICES_VALUE_FIELD] = obj.pk
    #         return d
    else:
        raise http.Http404("No choices for %s" % field)
    return (qs, row2dict)


def setup_params_choosers(self):
    if self.parameters:
        for k, fld in self.parameters.items():
            if isinstance(fld, models.ForeignKey):
                msg = "Invalid target %s in parameter {} of {}".format(k, self)
                fld.remote_field.model = resolve_model(
                    fld.remote_field.model, strict=msg
                )
                set_default_verbose_name(fld)

            choosers.check_for_chooser(self, fld)
