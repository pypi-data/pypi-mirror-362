# -*- coding: UTF-8 -*-
# Copyright 2020-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import os
from copy import copy

from django.db import models
from django.conf import settings
from django.utils import translation
# from django.utils.text import format_lazy

from lino.api import dd, rt, _
from lino.utils.html import E, tostring, join_elems
from lino.mixins.registrable import RegistrableState
from lino.core.choicelists import ChoiceList, Choice
from lino.core.choicelists import PointingChoice, MissingRow

from lino.modlib.jinja.choicelists import JinjaBuildMethod
from lino.modlib.printing.choicelists import BuildMethods


class PublisherBuildMethod(JinjaBuildMethod):
    template_ext = ".pub.html"
    templates_name = "pub"
    default_template = "default.pub.html"
    target_ext = ".html"
    name = "pub"

    def build(self, ar, action, elem):
        filename = action.before_build(self, elem)
        if filename is None:
            return
        tpl = self.get_template(action, elem)
        lang = str(elem.get_print_language() or translation.get_language())
        # or settings.SITE.DEFAULT_LANGUAGE.django_code)
        ar = copy(ar)
        ar.renderer = settings.SITE.plugins.jinja.renderer
        # ar.tableattrs = dict()
        # ar.cellattrs = dict(bgcolor="blue")

        with translation.override(lang):
            cmd_options = elem.get_build_options(self)
            dd.logger.info(
                "%s render %s -> %s (%r, %s)",
                self.name,
                tpl.lino_template_names,
                filename,
                lang,
                cmd_options,
            )
            context = elem.get_printable_context(ar)
            html = tpl.render(context)
            self.html2file(html, filename, context)
            return os.path.getmtime(filename)


BuildMethods.add_item_instance(PublisherBuildMethod())

# class PublisherView(dd.Choice):
#     table_class = None  # TODO: rename this to data_view
#
#     def __init__(self, location, table_class, text=None):
#         self.table_class = table_class
#         self.publisher_location = location
#         # model = dd.resolve_model(table_class.model)
#         # self.model = model
#         # value = dd.full_model_name(model)
#         value = str(table_class)
#         if text is None:
#             text = format_lazy("{} ({})", location, table_class)
#             # text = model._meta.verbose_name + ' (%s)' % dd.full_model_name(model)
#             # text = model._meta.verbose_name + ' (%s.%s)' % (
#             # text = format_lazy("{} ({})", model._meta.verbose_name, value)
#         #     model.__module__, model.__name__)
#         name = None
#         super().__init__(value, text, name)
#
#     def get_publisher_pages(self):
#         return self.table_class.model.objects.all()

# class PublisherViews(dd.ChoiceList):
#     item_class = PublisherView
#     verbose_name = _("Publisher view")
#     verbose_name_plural = _("Publisher views")
#     column_names = "location value name text data_view *"
#
#     @dd.virtualfield(models.CharField(_("Location")))
#     def location(cls, choice, ar):
#         return choice.publisher_location
#
#     @dd.virtualfield(models.CharField(_("Data table")))
#     def data_view(cls, choice, ar):
#         return choice.table_class


class PublishingState(RegistrableState):
    # is_published = False
    is_public = models.BooleanField(_("Public"), default=False)


class PublishingStates(dd.Workflow):
    item_class = PublishingState
    verbose_name = _("Publishing state")
    verbose_name_plural = _("Publishing states")
    column_names = "value name text button_text is_public"

    # @classmethod
    # def get_published_states(cls):
    #     return [o for o in cls.objects() if o.is_public]

    @dd.virtualfield(models.BooleanField(_("public")))
    def is_public(cls, choice, ar):
        return choice.is_public


add = PublishingStates.add_item
# add('10', _("Draft"), 'draft')
# add('20', _("Published"), 'published', is_published=True)
# add('30', _("Removed"), 'removed')
add("10", _("Draft"), "draft", is_public=False)
add("20", _("Ready"), "ready", is_public=False)
add("30", _("Public"), "published", is_public=True)
add("40", _("Removed"), "removed", is_public=False)

# class EntryStates(dd.Workflow):
#     # verbose_name_plural = _("Enrolment states")
#     required_roles = dd.login_required(dd.SiteAdmin)
#     is_public = models.BooleanField(_("Public"), default=False)
#
#     @classmethod
#     def get_column_names(self, ar):
#         return "value name text button_text is_public"
#
# add = EntryStates.add_item
# add('10', _("Draft"), 'draft', is_public=False)
# add('20', _("Ready"), 'ready', is_public=False)
# add('30', _("Public"), 'published', is_public=True)
# add('40', _("Cancelled"), 'cancelled', is_public=False)


class PageFiller(Choice):
    data_view = None

    def __init__(self, data_view, *args, **kwargs):
        self.data_view = data_view
        super().__init__(str(data_view), *args, **kwargs)

    def get_dynamic_story(self, ar, obj, **kwargs):
        txt = ""
        dv = self.data_view
        sar = dv.create_request(parent=ar, limit=dv.preview_limit)
        # print("20231028", dv, list(sar))
        # print("20230409", ar.renderer)
        # rv += "20230325 [show {}]".format(dv)
        for e in sar.renderer.table2story(sar, **kwargs):
            txt += tostring(e)
        return txt

    def get_dynamic_paragraph(self, ar, obj, **kwargs):
        dv = self.data_view
        # sar = dv.create_request(parent=ar, limit=dv.preview_limit)
        sar = dv.create_request(parent=ar)
        return " / ".join([sar.obj2htmls(row) for row in sar])


class PageFillers(ChoiceList):
    verbose_name = _("Page filler")
    verbose_name_plural = _("Page fillers")
    item_class = PageFiller
    max_length = 50
    column_names = "value name text data_view *"

    @dd.virtualfield(models.CharField(_("Data table")))
    def data_view(cls, choice, ar):
        return choice.data_view


# class SpecialPage(PointingChoice):
class SpecialPage(dd.Choice):
    # pointing_field_name = 'publisher.Page.special_page'
    # show_values = True

    def __init__(self, name, text=None, parent=None, **kwargs):
        self.parent_value = parent
        self._default_values = dict()
        for k in ("ref", "title", "filler", "body"):
            if k in kwargs:
                self._default_values[k] = kwargs.pop(k)
        super().__init__(name, text, name, **kwargs)
        # if (filler := self.default_values.get('filler', None)):
        #     if "title" not in self.default_values:
        #         self.default_values["title"] = filler.data_view.get_actor_label()
        # else:
        #     if "title" not in self.default_values:
        #         self.default_values["title"] = self.text

    def on_page_created(self, obj):
        for k, v in self._default_values.items():
            setattr(obj, k, v)
        if obj.filler and not obj.title:
            obj.title = obj.filler.data_view.get_actor_label()
        if not obj.title:
            obj.title = self.text or "20250422"
        if self.parent_value:
            psp = self.choicelist.get_by_value(self.parent_value)
            obj.parent = psp.get_object()

    # def get_object(self, ar):
    def get_object(self):
        language = translation.get_language()
        # if len(settings.SITE.languages) == 1:
        #     language = translation.get_language()
        # else:
        #     language = ar.request.LANGUAGE_CODE
        # return rt.models.publisher.Page.objects.get(ref=self.defaul_values['ref'], language=language)
        return rt.models.publisher.Page.objects.get(special_page=self, language=language)


class SpecialPages(dd.ChoiceList):
    verbose_name = _("Special page")
    verbose_name_plural = _("Special pages")
    item_class = SpecialPage
    required_roles = dd.login_required(dd.SiteStaff)
    column_names = "name text page_objects *"

    # @dd.virtualfield(dd.ForeignKey('publisher.Page'))
    # def db_object(cls, choice, ar):
    #     obj = choice.get_object()
    #     if obj is None or isinstance(obj, MissingRow):
    #         return None
    #     return obj

    @dd.htmlbox(_("Pages"))
    def page_objects(cls, choice, ar):
        lst = []
        Page = rt.models.publisher.Page
        for lng in settings.SITE.languages:
            try:
                page = Page.objects.get(special_page=choice, language=lng.django_code)
                lst.append(ar.obj2html(page, lng.name))
            except Page.DoesNotExist:
                page = _("(create)")
                lst.append(lng.name)
        lst = join_elems(lst, " | ")
        return E.p(*lst)


add = SpecialPages.add_item

add("home", _("Home"), ref="index", body=_("Welcome to our great website."))
add("terms", _("Terms and conditions"))
add("privacy", _("Privacy policy"))
add("cookies", _("Cookie settings"))
add("copyright", _("Copyright"))
add("about", _("About us"))
