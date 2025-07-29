# -*- coding: UTF-8 -*-
# Copyright 2020-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# from inspect import isclass
from lino.utils.html import tostring
from lino.api import dd, rt, _

from django import http
from django.db import models
from django.conf import settings
from django.utils.translation import get_language
from lino.core.renderer import add_user_language
from lino.core.utils import full_model_name
from lino.utils import buildurl
from lino.utils.html import mark_safe
from lino.modlib.printing.mixins import Printable
from lino.modlib.printing.choicelists import BuildMethods
from .choicelists import PublishingStates, PageFillers
# from .choicelists import PublisherViews, PublishingStates


class PreviewPublication(dd.Action):
    label = _("Preview")
    button_text = "🌐"  # 1F310

    select_rows = True

    def run_from_ui(self, ar, **kw):
        # sr_selected = not isclass(self)
        # if sr_selected:
        #     ar.success(open_url=self.publisher_url())
        # else:
        #     ar.success(open_url=self.publisher_url(self, not sr_selected))
        obj = ar.selected_rows[0]
        # ar.success(open_url=obj.publisher_url(ar))
        ar.success(open_url=dd.plugins.publisher.renderer.obj2url(ar, obj))

    # def get_view_permission(self, user_type):
    #     return super().get_view_permission(user_type)


class Publishable(Printable):
    class Meta:
        abstract = True
        app_label = "publisher"

    publisher_template = "publisher/page.pub.html"
    _lino_publisher_location = None

    @dd.htmlbox()
    def full_page(self, ar):
        if ar is None:
            return ""
        return mark_safe("".join(self.as_page(ar)))

    if dd.is_installed("publisher"):
        # previous_page = dd.ForeignKey("self", null=True, blank=True,
        #     verbose_name=_("Previous page"))

        # previous_page_view = PublisherViews.field(blank=True, null=True,
        #     verbose_name=_("Previous page (view)"))
        # previous_page_id = IntegerField(blank=True, null=True,
        #     verbose_name=_("Previous page (key)"))

        preview_publication = PreviewPublication()

        # @classmethod
        # def on_analyze(cls, site):
        #     # Inject the previous_page field to all models that have a publisher
        #     # view.
        #     # print("20231103", cls, [pv.table_class.model for pv in PublisherViews.get_list_items()])
        #     # for pv in PublisherViews.get_list_items():
        #     for loc, table_class in site.plugins.publisher.locations:
        #         if full_model_name(cls) == table_class.model:
        #             # print("20231103", cls)
        #             dd.inject_field(
        #                 cls, 'previous_page',
        #                 dd.ForeignKey("self", null=True, blank=True,
        #                     verbose_name=_("Previous page")))
        #             return

    # @dd.action(select_rows=False)
    # def preview_publication(self, ar):
    #     sr_selected = not isclass(self)
    #     if sr_selected:
    #         ar.success(open_url=self.publisher_url())
    #     else:
    #         ar.success(open_url=self.publisher_url(self, not sr_selected))

    # def publisher_url(self, ar, **kw):
    #     for i in PublisherViews.get_list_items():
    #         if isinstance(self, i.table_class.model):
    #             # print("20230409", self.__class__, i)
    #             # return "/{}/{}".format(i.publisher_location, self.pk)
    #             add_user_language(kw, ar)
    #             # return buildurl("/" + i.publisher_location, str(self.pk), **dd.urlkwargs())
    #             return ar.renderer.front_end.buildurl(i.publisher_location, str(self.pk), **kw)
    #             # return dd.plugins.publisher.buildurl("/"+i.publisher_location, str(self.pk), **kw)
    #             # return buildurl("/", i.publisher_location, str(self.pk), **kw)
    #     available = [i.table_class.model for i in PublisherViews.get_list_items()]
    #     return "No publisher view for {} in {}".format(self, available)

    def is_public(self):
        return True

    def get_preview_context(self, ar):
        return ar.get_printable_context(obj=self)

    # def set_previous_page(self, ppv, ppi):
    #     if self.previous_page_id != ppi or self.previous_page_view != ppv:
    #         self.previous_page_id = ppi
    #         self.previous_page_view = ppv
    #         self.save()

    # @classmethod
    # def update_publisher_pages(cls):
    #     pass

    # def render_from(self, tplname, ar):
    #     env = settings.SITE.plugins.jinja.renderer.jinja_env
    #     context = self.get_preview_context(ar)
    #     template = env.get_template(tplname)
    #     # print("20210112 publish {} {} using {}".format(cls, obj, template))
    #     # context = dict(obj=self, request=request, language=get_language())
    #     return template.render(**context)

    def home_and_children(self, ar):
        home = rt.models.publisher.SpecialPages.home.get_object()
        return home, rt.models.publisher.Page.objects.filter(parent=home)
        # return dv.model.objects.filter(models.Q(parent=index_node) | models.Q(ref='index'), language=language)

    def get_publisher_response(self, ar):
        if not self.is_public():
            return http.HttpResponseNotFound(
                "{} {} is not public".format(self.__class__, self.pk)
            )
        context = self.get_preview_context(ar)
        # html = ''.join(self.as_page(ar))
        # # context.update(content=html, admin_site_prefix=dd.plugins.publisher.admin_location)
        # context.update(content=html)
        tpl = dd.plugins.jinja.renderer.jinja_env.get_template(self.publisher_template)
        return http.HttpResponse(
            tpl.render(**context), content_type='text/html;charset="utf-8"'
        )


class PublishableContent(Publishable):
    class Meta:
        abstract = True
        app_label = "publisher"

    language = dd.LanguageField()
    publishing_state = PublishingStates.field(default="draft")
    filler = PageFillers.field(blank=True, null=True)
    main_image = dd.ForeignKey('uploads.Upload', blank=True, null=True, verbose_name=_("Main image"))

    def get_print_language(self):
        return self.language

    def on_create(self, ar):
        self.language = ar.get_user().language
        super().on_create(ar)

    def on_duplicate(self, ar, master):
        self.publishing_state = PublishingStates.draft
        super().on_duplicate(ar, master)

    def is_public(self):
        return self.publishing_state.is_public
