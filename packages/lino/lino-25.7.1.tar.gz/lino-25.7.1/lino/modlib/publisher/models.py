# -*- coding: UTF-8 -*-
# Copyright 2012-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from html import escape
from django.db import models
from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils import translation
from django.utils.translation import pgettext_lazy

from django.utils import translation
from django.conf import settings

try:
    from lorem import get_paragraph
except ImportError:
    lorem = None

# from django.utils.translation import get_language
from django.utils.html import mark_safe

from lino.api import dd, rt, _
from lino.utils import mti
from lino.utils.html import E, tostring
from lino.core import constants
# from lino.core.renderer import add_user_language

from lino.utils.mldbc.fields import LanguageField
from lino import mixins
from lino.mixins import Hierarchical, Sequenced, Referrable

# from lino.modlib.summaries.mixins import Summarized
from lino.modlib.office.roles import OfficeUser
from lino.modlib.publisher.mixins import Publishable, PublishableContent
from lino.modlib.comments.mixins import Commentable
from lino.modlib.linod.choicelists import schedule_daily
from lino.modlib.memo.mixins import Previewable
from lino.mixins.polymorphic import Polymorphic
from lino_xl.lib.topics.mixins import Taggable
# from .utils import render_node

from lino.api import rt, dd
from .choicelists import PublishingStates, PageFillers, SpecialPages
from .mixins import Publishable
from .ui import *

# class Node(Referrable, Hierarchical, Sequenced, Previewable, Publishable, Commentable):
# Polymorphic,
class Page(
    Hierarchical, Sequenced, Previewable, Commentable, PublishableContent, Taggable
):
    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")
        abstract = dd.is_abstract_model(__name__, "Page")
        unique_together = ["ref", "language"]

    memo_command = "page"

    ref = models.CharField(
        _("Reference"), max_length=200, blank=True, null=True)

    title = dd.CharField(_("Title"), max_length=250, blank=True)
    child_node_depth = models.IntegerField(default=1)
    # page_type = PageTypes.field(blank=True, null=True)
    special_page = SpecialPages.field(blank=True)

    translated_from = dd.ForeignKey(
        "publisher.Page",
        verbose_name=_("Translated from"),
        null=True,
        blank=True,
        related_name="translated_to",
    )

    previous_page = dd.ForeignKey(
        "self", null=True, blank=True, verbose_name=_("Previous page")
    )

    def __str__(self):
        return self.title or self.ref or super().__str__()

    # def on_create(self, ar):
    #     self.page_type = self.get_page_type()
    #     super().on_create(ar)

    # def get_for_language(self, lng):
    #     # lng is a LanguageInfo object settings.SITE.get_language_info()
    #     if lng.prefix:
    #         qs = self.__class__.objects.filter(
    #             translated_from=self, language=lng.code)
    #         return qs.first()
    #     return self

    def get_node_info(self, ar):
        return ""

    # def full_clean(self):
    #     self.page_type = self.mti_child().get_page_type()
    #     super().full_clean()

    def mti_child(self):
        #     if self.page_type:
        #         return mti.get_child(self, self.page_type.nodes_table.model) or self
        return self

    # def as_summary_row(self, ar, **kwargs):
    #     return ar.obj2htmls(self, **kwargs)

    # def as_story_item(self, ar, **kwargs):
    #     return "".join(self.as_page(ar, **kwargs))

    def as_paragraph(self, ar):
        title = E.b(escape(self.title))
        url = ar.obj2url(self)
        if url is not None:
            title = E.a(title, href=url, style="text-decoration: none; color: black;")
        body = self.get_body_parsed(ar, short=True)
        if body:
            body = " - " + body
        item = E.li(title, body)
        return tostring(item)

    def toc_html(self, ar, max_depth=1):
        def li(obj):
            # return "<li>{}</li>".format(obj.memo2html(ar, str(obj)))
            return "<li>{}</li>".format(tostring(ar.obj2html(obj)))

        html = "".join([li(obj) for obj in self.children.all()])
        return '<ul class="publisher-toc">{}</ul>'.format(html)

    def as_page(self, ar, display_mode="detail", hlevel=1, home=None):
        if home is None:
            home = self
        if display_mode == "detail" and hlevel == 1:
            breadcrumbs = list(self.get_parental_line())
            if len(breadcrumbs) > 1:
                breadcrumbs = [
                    """<a href="{0}">{1}</a>""".format(
                        ar.obj2url(p.mti_child()), p.title
                    )
                    for p in breadcrumbs[:-1]
                ]
                yield "<p>{}</p>".format(" &raquo; ".join(breadcrumbs))
        if display_mode in ("detail", "story"):
            title = "<h{0}>{1}</h{0}>".format(hlevel, escape(self.title))
        else:
            title = "<b>{}</b> — ".format(escape(self.title))
            title += self.get_body_parsed(ar, short=True)
            title = "<li>{}</li>".format(title)
        # edit_url = ar.renderer.obj2url(ar, self)
        # url = self.publisher_url(ar)
        # print("20231029", ar.renderer)
        # url = ar.obj2url(self.mti_child())
        url = ar.obj2url(self)
        if url is None:
            yield title
        else:
            yield """<a href="{}"
            style="text-decoration:none; color: black;">{}</a>
            """.format(escape(url), title)

        # if not self.is_public():
        #     return

        if display_mode in ("detail",):
            info = self.get_node_info(ar)
            if info:
                yield """<p class="small">{}</p>""".format(info)
                # https://getbootstrap.com/docs/3.4/css/#small-text

        if display_mode == "story":
            yield self.get_body_parsed(ar, short=True)

        # if display_mode in ("detail", "story"):
        if display_mode == "detail":
            if hlevel == 1 and not dd.plugins.memo.use_markup and self.ref != 'index':
                yield self.toc_html(ar)

            if hlevel == 1 and self.main_image:
                yield f"""
                <div class="row">
                    <div class="center-block">
                        <a href="#" class="thumbnail">
                            <img src="{self.main_image.get_media_file().get_image_url()}">
                        </a>
                    </div>
                </div>
                """

            # yield self.body_full_preview
            yield self.get_body_parsed(ar, short=False)

            if self.filler:
                yield "\n\n"
                if hlevel == 1:
                    yield self.filler.get_dynamic_story(ar, self)
                else:
                    yield self.filler.get_dynamic_paragraph(ar, self)

            # if dd.plugins.memo.use_markup:
            #     return

            if not self.children.exists():
                return

            yield "<p><b>{}</b></p>".format(_("Children:"))

            if hlevel > home.child_node_depth:
                yield " (...)"
                return
            if hlevel == home.child_node_depth:
                display_mode = "list"
                yield "<ul>"
            children = self.children.order_by("seqno")
            for obj in children:
                for i in obj.as_page(ar, display_mode, hlevel=hlevel + 1, home=home):
                    yield i
            if hlevel == home.child_node_depth:
                yield "</ul>"
        # else:
        #     yield " — "
        #     yield self.body_short_preview
        #     for obj in self.children.order_by('seqno'):
        #         for i in obj.as_page(ar, "list", hlevel+1):
        #             yield i

    # @classmethod
    # def lookup_page(cls, ref):
    #     try:
    #         return cls.objects.get(ref=ref, language=get_language())
    #     except cls.DoesNotExist:
    #         pass

    # @dd.htmlbox(_("Preview"))
    @dd.htmlbox()
    def preview(self, ar):
        if ar is None:
            return
        return "".join(ar.row_as_page(self))

    # @classmethod
    # def get_publisher_pages(cls, pv):
    #     root = cls.objects.get(parent__isnull=True)

    # def compute_summary_values(self):
    #     def walk(node, prev=None):
    #         if node.page_type is not None:
    #             node.set_prev(prev)
    #             prev = node
    #         for c in node.children.all():
    #             prev = walk(c, prev)
    #         return prev
    #     root = self.get_ancestor()
    #     last = walk(root)
    #     root.set_prev(last)

    # from pprint import pprint
    # pprint(self.whole_tree())

    # def get_sidebar_caption(self):
    #     if self.title:
    #         return self.title
    #     if self.ref:
    #         return self.ref
    #     return str(self.id)
    #
    #     #~ if self.ref or self.parent:
    #         #~ return self.ref
    #     #~ return unicode(_('Home'))

    # def get_sidebar_item(self, request, other):
    #     kw = dict()
    #     add_user_language(kw, request)
    #     url = self.get_absolute_url(**kw)
    #     a = E.a(self.get_sidebar_caption(), href=url)
    #     if self == other:
    #         return E.li(a, **{'class':'active'})
    #     return E.li(a)
    #
    # def get_sidebar_html(self, request):
    #     items = []
    #     #~ loop over top-level nodes
    #     for n in self.__class__.objects.filter(parent__isnull=True).order_by('seqno'):
    #         #~ items += [li for li in n.get_sidebar_items(request,self)]
    #         items.append(n.get_sidebar_item(request, self))
    #         if self.is_parented(n):
    #             children = []
    #             for ch in n.children.order_by('seqno'):
    #                 children.append(ch.get_sidebar_item(request, self))
    #             if len(children):
    #                 items.append(E.ul(*children, **{'class':'nav nav-list'}))
    #
    #     e = E.ul(*items, **{'class':'nav nav-list'})
    #     return tostring_pretty(e)
    #
    # def get_sidebar_menu(self, request):
    #     qs = self.__class__.objects.filter(parent__isnull=True, language=get_language())
    #     #~ qs = self.children.all()
    #     yield ('/', 'index', str(_('Home')))
    #         #~ yield ('/downloads/', 'downloads', 'Downloads')
    #     #~ yield ('/about', 'about', 'About')
    #     #~ if qs is not None:
    #     for obj in qs.order_by("seqno"):
    #         if obj.ref and obj.title:
    #             yield ('/' + obj.ref, obj.ref, obj.title)
    #         #~ else:
    #             #~ yield ('/','index',obj.title)

    def set_previous_page(self, prev):
        if self.previous_page != prev:
            self.previous_page = prev
            self.save()

    def get_prev_link(self, ar, text="◄"):  # "◄" 0x25c4
        if not self.previous_page_id:
            return text
        # obj = self.previous_page_view.table_class.model.objects.get(pk=self.previous_page_id)
        return tostring(ar.obj2html(self.previous_page, text))
        # url = ar.obj2url(self.prev_node.mti_child())
        # if url is None:
        #     # print("20231029 prev_node has no url?!", self.prev_node)
        #     return text
        # return """<a href="{}">{}</a>""".format(url, text)

    def get_next_link(self, ar, text="►"):  # ► (0x25BA)
        next_node = self.__class__.objects.filter(previous_page=self).first()
        # next_node = Node.objects.filter(prev_node_id=self.id).first()
        if next_node is None:
            return text
        return tostring(ar.obj2html(next_node, text))
        # url = ar.obj2url(next_node.mti_child())
        # return """<a href="{}">{}</a>""".format(url, text)

    @classmethod
    def get_publisher_pages(cls):
        def walk(page, prev=None):
            yield page
            for c in page.children.all():
                for i in walk(c):
                    yield i

        for root in cls.objects.filter(parent__isnull=True):
            for i in walk(root):
                yield i

    @classmethod
    def get_dashboard_objects(cls, user):
        # print("20210114 get_dashboard_objects()", get_language())
        # qs = cls.objects.filter(parent__isnull=True, language=get_language())
        qs = cls.objects.filter(parent__isnull=True)
        for obj in qs.order_by("seqno"):
            yield obj

    # def get_page_type(self):
    #     return PageTypes.pages

    # def is_public(self):
    #     return True

    def get_absolute_url(self, **kwargs):
        if self.ref:
            if self.ref != "index":
                return dd.plugins.publisher.build_plain_url(self.ref, **kwargs)
        return dd.plugins.publisher.build_plain_url(**kwargs)

    def get_publisher_response(self, ar):
        if ar and ar.request and self.language != ar.request.LANGUAGE_CODE:
            rqlang = ar.request.LANGUAGE_CODE
            # tt = rt.models.pages.Translation.objects.filter(
            #     parent=self, language=ar.request.LANGUAGE_CODE).first()
            obj = None
            if self.translated_from_id and self.translated_from.language == rqlang:
                obj = self.translated_from
            else:
                sources = set([self.id])
                p = self.translated_from
                while p is not None:
                    sources.add(p.id)
                    p = p.translated_from
                qs = self.__class__.objects.filter(
                    language=rqlang, translated_from__in=sources
                )
                obj = qs.first()
                # obj = self.translated_to.filter(language=rqlang).first()
            # print("20231027 redirect to translation", tt.language, ar.request.LANGUAGE_CODE)
            if obj is not None:
                # print("20231028", self.language, "!=", ar.request.LANGUAGE_CODE, tt)
                ar.selected_rows = [obj]
                url = ar.get_request_url()
                return HttpResponseRedirect(url)
        return super().get_publisher_response(ar)


if dd.plugins.memo.use_markup:
    dd.update_field(Page, "body", format="plain")

# class Translation(dd.Model):
#     class Meta:
#         verbose_name = _("Page translation")
#         verbose_name_plural = _("Page translations")
#
#     parent = dd.ForeignKey(
#         'publisher.Page',
#         verbose_name=_("Translated from..."),
#         related_name='translated_from')
#     child = dd.ForeignKey(
#         'publisher.Page',
#         blank=True, null=True,
#         verbose_name=_("Translated to..."),
#         related_name='translated_to')
#     language = dd.LanguageField()


@schedule_daily()
def update_publisher_pages(ar):
    # BaseRequest(parent=ar).run(settings.SITE.site_config.check_all_summaries)
    # rt.login().run(settings.SITE.site_config.check_all_summaries)
    Page = settings.SITE.models.publisher.Page
    # for pv in PublisherViews.get_list_items():
    # for m in rt.models_by_base(Published, toplevel_only=True):
    prev = None
    count = 0
    ar.logger.info("Update publisher pages...")

    for obj in Page.get_publisher_pages():
        obj.set_previous_page(prev)
        prev = obj
        count += 1
    ar.logger.info("%d pages have been updated.", count)


def make_demo_pages(pages_desc):
    # Translation = rt.models.pages.Translation
    # for lc in settings.SITE.LANGUAGE_CHOICES:
    #     language = lc[0]
    #     kwargs = dict(language=language, ref='index')
    #     with translation.override(language):

    parent_nodes = []
    for lng in settings.SITE.languages:
        counter = {None: 0}
        # count = 0
        home_page = Page.objects.get(
            special_page=SpecialPages.home, language=lng.django_code)

        with translation.override(lng.django_code):

            def make_pages(pages, parent=None):
                for page in pages:
                    if len(page) != 3:
                        raise Exception(f"Oops {page}")
                    title, body, children = page
                    kwargs = dict(title=title)
                    if body is None:
                        kwargs.update(body=get_paragraph())
                    else:
                        kwargs.update(body=body)
                    if parent is None:
                        # kwargs.update(ref='index')
                        continue  # home page is created by SpecialPages
                    if lng.suffix:
                        kwargs.update(
                            translated_from=parent_nodes[counter[None]])
                    kwargs.update(language=lng.django_code)
                    if dd.is_installed("publisher"):
                        kwargs.update(publishing_state='published')
                    obj = Page(parent=parent, **kwargs)
                    yield obj
                    if not lng.suffix:
                        parent_nodes.append(obj)
                    counter[None] += 1
                    # print("20230324", title, kwargs)
                    yield make_pages(children, obj)

            yield make_pages(pages_desc, parent=home_page)
