# -*- coding: UTF-8 -*-
# Copyright 2016-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lxml.html import fragments_fromstring
import lxml

try:
    import markdown
except ImportError:
    markdown = None

from django.conf import settings
from django.utils import translation
from django.utils.html import format_html

from lino.core.gfks import gfk2lookup
from lino.core.fields import RichTextField, PreviewTextField
from lino.utils.html import E, tostring, mark_safe
from lino.utils.restify import restify
from lino.utils.soup import truncate_comment
from lino.utils.mldbc.fields import BabelTextField
from lino.modlib.checkdata.choicelists import Checker
from lino.api import rt, dd, _


MARKDOWNCFG = dict(
    extensions=["toc"], extension_configs=dict(toc=dict(toc_depth=3, permalink=True))
)


def rich_text_to_elems(ar, description):
    description = ar.parse_memo(description)

    # After 20250213 #5929 (Links in the description of a ticket aren't rendered
    # correctly) we no longer try to automatically detect reSTructuredText
    # markup in a RichTextField. Anyway nobody has ever used this feature
    # (except for the furniture fixture of the products plugin).

    # if description.startswith("<"):
    if True:
        # desc = E.raw('<div>%s</div>' % self.description)
        desc = fragments_fromstring(description)
        return desc
    # desc = E.raw('<div>%s</div>' % self.description)
    html = restify(description)
    # logger.info(u"20180320 restify %s --> %s", description, html)
    # html = html.strip()
    try:
        desc = fragments_fromstring(html)
    except Exception as e:
        raise Exception("Could not parse {!r} : {}".format(html, e))
    # logger.info(
    #     "20160704c parsed --> %s", tostring(desc))
    return desc
    # if desc.tag == 'body':
    #     # happens if it contains more than one paragraph
    #     return list(desc)  # .children
    # return [desc]


def body_subject_to_elems(ar, title, description):
    if description:
        elems = [E.p(E.b(title), E.br())]
        elems += rich_text_to_elems(ar, description)

    else:
        elems = [E.b(title)]
        # return E.span(self.title)
    return elems


class MemoReferrable(dd.Model):
    class Meta:
        abstract = True

    memo_command = None

    if dd.is_installed("memo"):

        @classmethod
        def on_analyze(cls, site):
            super().on_analyze(site)
            if cls.memo_command is None:
                return
            mp = site.plugins.memo.parser
            mp.register_django_model(cls.memo_command, cls)
            # mp.add_suggester("[" + cls.memo_command + " ", cls.objects.all(), 'pk')

    def memo2html(self, ar, txt, **kwargs):
        if txt:
            kwargs.update(title=txt)
        e = self.as_summary_item(ar)
        return tostring(e)
        # return ar.obj2str(self, **kwargs)

    def obj2memo(self, text=None):
        """Render the given database object as memo markup."""
        if self.memo_command is None:
            return "**{}**".format(self)
        # title = self.get_memo_title()
        if text is None:
            # text = str(self)
            return "[{} {}]".format(self.memo_command, self.id)
        # return "[{} {}] ({})".format(self.memo_command, self.id, title)
        return "[{} {} {}]".format(self.memo_command, self.id, text)


# class MentionGenerator(dd.Model):
#
#     class Meta:
#         abstract = True
#
#     def get_memo_text(self):
#         return None
#
#     if dd.is_installed("memo"):
#         def after_ui_save(self, ar, cw):
#             super().after_ui_save(ar, cw)
#             memo_parser = settings.SITE.plugins.memo.parser
#             ref_objects = memo_parser.get_referred_objects(self.get_memo_text())
#             Mention = rt.models.memo.Mention
#             for ref_object in ref_objects:
#                 created_mention = Mention(owner=self,
#                         owner_id=ref_object.pk,
#                         owner_type=ContentType.objects.get_for_model(ref_object.__class__))
#                 created_mention.touch()
#                 created_mention.save()


# class BasePreviewable(MentionGenerator):
class BasePreviewable(dd.Model):
    class Meta:
        abstract = True

    previewable_field = None

    def get_preview_length(self):
        return settings.SITE.plugins.memo.short_preview_length

    def save(self, *args, **kwargs):
        """Updates the preview fields and the list of mentioned objects."""
        pf = self.previewable_field
        mentions = set()
        txt = self.get_previewable_text(settings.SITE.DEFAULT_LANGUAGE)
        short, full = self.parse_previews(txt, None, mentions)
        # if "choose one or the other" in short:
        #     raise Exception("20230928 {} {}".format(len(short), short))
        # print("20231023 b", short)
        setattr(self, pf + "_short_preview", short)
        setattr(self, pf + "_full_preview", full)
        if isinstance(self, BabelPreviewable):
            for lng in settings.SITE.BABEL_LANGS:
                src = self.get_previewable_text(lng)
                # src = getattr(self, pf + lng.suffix)
                with translation.override(lng.django_code):
                    short, full = self.parse_previews(src, None, mentions)
                setattr(self, pf + "_short_preview" + lng.suffix, short)
                setattr(self, pf + "_full_preview" + lng.suffix, full)
        super().save(*args, **kwargs)
        self.synchronize_mentions(mentions)

    def get_previewable_text(self, lng):
        return getattr(self, self.previewable_field + lng.suffix)

    def parse_previews(self, source, ar=None, mentions=None, **context):
        context.update(self=self)
        full = settings.SITE.plugins.memo.parser.parse(
            source, ar=ar, context=context, mentions=mentions
        )
        short = truncate_comment(full, self.get_preview_length())
        if not full.startswith("<"):
            if settings.SITE.plugins.memo.use_markup:
                full = markdown.markdown(full, **MARKDOWNCFG)
        return (short, full)

    def get_saved_mentions(self):
        Mention = rt.models.memo.Mention
        flt = gfk2lookup(Mention.owner, self)
        return Mention.objects.filter(**flt).order_by("target_type", "target_id")

    def synchronize_mentions(self, mentions):
        Mention = rt.models.memo.Mention
        for obj in self.get_saved_mentions():
            if obj.target in mentions:
                mentions.remove(obj.target)
            else:
                obj.delete()
        for target in mentions:
            obj = Mention(owner=self, target=target)
            # source_id=source.pk,
            # source_type=ContentType.objects.get_for_model(source.__class__))
            obj.full_clean()
            obj.save()

    def get_overview_elems(self, ar):
        yield E.h1(str(self))

        if self.body_short_preview:
            try:
                for e in lxml.html.fragments_fromstring(self.body_short_preview):
                    yield e
            except Exception as e:
                yield "{} [{}]".format(self.body_short_preview, e)


class Previewable(BasePreviewable):
    class Meta:
        abstract = True

    previewable_field = "body"

    body = PreviewTextField(_("Body"), blank=True, format="html", bleached=True)
    body_short_preview = RichTextField(_("Preview"), blank=True, editable=False)
    body_full_preview = RichTextField(_("Preview (full)"), blank=True, editable=False)

    def get_body_parsed(self, ar, short=False):
        if ar.renderer is settings.SITE.kernel.editing_front_end.renderer:
            return self.body_short_preview if short else self.body_full_preview
        # raise Exception("{} is not {}".format(
        #     ar.renderer, settings.SITE.kernel.editing_front_end.renderer))
        src = self.body
        s, f = self.parse_previews(src, ar, set())
        return s if short else f

    def as_paragraph(self, ar):
        s = super().as_paragraph(ar)
        # s = format_html("<b>{}</b> : {}", .format(ar.add_detail_link(self, str(self)))
        # s = ar.obj2htmls(self)
        s = format_html(
            "<b>{}</b> : {}", s, mark_safe(self.body_short_preview) or _("(no preview)")
        )
        return s


class BabelPreviewable(BasePreviewable):
    class Meta:
        abstract = True

    previewable_field = "body"

    body = BabelTextField(_("Body"), blank=True, format="html", bleached=True)
    body_short_preview = BabelTextField(_("Preview"), blank=True, editable=False)
    body_full_preview = BabelTextField(_("Preview (full)"), blank=True, editable=False)

    # def save(self, *args, **kwargs):
    #     pf = self.previewable_field
    #     mentions = set()
    #     for lng in settings.SITE.BABEL_LANGS:
    #         src = getattr(self, self.previewable_field+lng.suffix)
    #         with translation.override(lng.django_code):
    #             short, full = self.parse_previews(src, mentions)
    #         setattr(self, pf+'_short_preview'+lng.suffix, short)
    #         setattr(self, pf+'_full_preview'+lng.suffix, full)
    #     super().save(*args, **kwargs)
    #     self.synchronize_mentions(mentions)


class PreviewableChecker(Checker):
    verbose_name = _("Check for previewables needing update")
    model = BasePreviewable

    def _get_checkdata_problems(self, lng, obj, fix=False):
        src = obj.get_previewable_text(lng)
        pf = obj.previewable_field
        # src = getattr(obj, pf+suffix)
        expected_mentions = set()
        short, full = obj.parse_previews(src, None, expected_mentions)
        is_broken = False
        if (
            getattr(obj, pf + "_short_preview" + lng.suffix) != short
            or getattr(obj, pf + "_full_preview" + lng.suffix) != full
        ):
            yield (True, _("Preview differs from source."))
            is_broken = True
        found_mentions = set([obj.target for obj in obj.get_saved_mentions()])
        if expected_mentions != found_mentions:
            yield (True, _("Mentions differ from expected mentions."))
            is_broken = True
        if is_broken and fix:
            # setattr(obj, pf+'_short_preview'+suffix, short)
            # setattr(obj, pf+'_full_preview'+suffix, full)
            obj.full_clean()
            obj.save()
        # self.synchronize_mentions(mentions)

    def get_checkdata_problems(self, ar, obj, fix=False):
        for x in self._get_checkdata_problems(settings.SITE.DEFAULT_LANGUAGE, obj, fix):
            yield x
        if isinstance(obj, BabelPreviewable):
            for lng in settings.SITE.BABEL_LANGS:
                with translation.override(lng.django_code):
                    for x in self._get_checkdata_problems(lng, obj, fix):
                        yield x


PreviewableChecker.activate()
