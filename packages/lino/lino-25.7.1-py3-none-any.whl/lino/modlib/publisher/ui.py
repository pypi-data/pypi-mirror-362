# -*- coding: UTF-8 -*-
# Copyright 2012-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from html import escape
from django.db import models
from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils import translation
from django.utils.translation import pgettext_lazy

# from django.utils.translation import get_language
from django.utils.html import mark_safe
from django.utils.html import format_html

from lino.api import dd, rt, _
from lino.utils.html import E
from lino.core import constants
# from lino.core.renderer import add_user_language

from lino.utils.mldbc.fields import LanguageField
from lino import mixins
from lino.mixins import Hierarchical, Sequenced, Referrable
from lino.modlib.office.roles import OfficeUser
from lino.modlib.publisher.mixins import Publishable

# from lino.modlib.publisher.choicelists import PublisherViews
from lino.modlib.memo.mixins import Previewable
# from .utils import render_node

# class NodeDetail(dd.DetailLayout):
#     main = "first_panel general more"
#
#     first_panel = dd.Panel("""
#     treeview_panel:20 preview:60
#     """, label=_("Preview"))
#
#     general = dd.Panel("""
#     content_panel:60 right_panel:20
#     """, label=_("General"), required_roles=dd.login_required(OfficeUser))
#
#     more = dd.Panel("""
#     # topics.TagsByOwner:20 add_interest
#     comments.CommentsByRFC:20
#     """, label=_("More"), required_roles=dd.login_required(OfficeUser))
#
#     content_panel = """
#     title id
#     body
#     publisher.PagesByParent
#     """
#
#     right_panel = """
#     parent seqno
#     child_node_depth
#     page_type
#     filler
#     """
#
#
# class Nodes(dd.Table):
#     model = 'pages.Node'
#     column_names = "title page_type id *"
#     order_by = ["id"]
#     detail_layout = 'pages.NodeDetail'
#     insert_layout = """
#     title
#     page_type filler
#     """
#     display_mode = ((None, constants.DISPLAY_MODE_STORY),)
#
#

# class Translations(dd.Table):
#     model = 'pages.Translation'
#
# class TranslationsByParent(Translations):
#     master_key = 'parent'
#     label = _("Translated to...")
#
# class TranslationsByChild(Translations):
#     master_key = 'child'
#     label = _("Translated from...")


if dd.is_installed("comments") and dd.is_installed("topics"):
    DISCUSSION_PANEL = """
    topics.TagsByOwner:20 comments.CommentsByRFC:60
    """
else:
    DISCUSSION_PANEL = ""


class PageDetail(dd.DetailLayout):
    main = "general first_panel more"

    first_panel = dd.Panel(
        """
    treeview_panel:20 preview:60
    """,
        label=_("Preview"),
    )

    general = dd.Panel(
        """
    content_panel:60 right_panel:20
    """,
        label=_("General"),
        required_roles=dd.login_required(OfficeUser),
    )

    more = dd.Panel(
        DISCUSSION_PANEL,
        label=_("Discussion"),
        required_roles=dd.login_required(OfficeUser),
    )

    content_panel = """
    title id
    body
    publisher.PagesByParent
    """

    # right_panel = """
    # parent seqno
    # child_node_depth
    # page_type
    # filler
    # """

    right_panel = """
    ref language
    parent seqno
    child_node_depth main_image
    #page_type filler
    publishing_state special_page
    publisher.TranslationsByPage
    """


class Pages(dd.Table):
    model = "publisher.Page"
    column_names = "ref title #page_type id *"
    detail_layout = "publisher.PageDetail"
    insert_layout = """
    title
    ref
    #page_type filler
    """
    default_display_modes = {None: constants.DISPLAY_MODE_LIST}


class PagesByParent(Pages):
    master_key = "parent"
    label = _("Children")
    # ~ column_names = "title user *"
    order_by = ["seqno"]
    column_names = "seqno title *"
    default_display_modes = {None: constants.DISPLAY_MODE_LIST}


# PublisherViews.add_item_lazy("p", Pages)
# PublisherViews.add_item_lazy("n", Nodes)

# PageTypes.add_item(Pages, 'pages')


class TranslationsByPage(Pages):
    master_key = "translated_from"
    label = _("Translations")
    column_names = "ref title language id *"
    default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}

    @classmethod
    def row_as_summary(cls, ar, obj, text=None, **kwargs):
        # return format_html("({}) {}", obj.language, obj.as_summary_row(ar, **kwargs))
        return E.span("({}) ".format(obj.language), obj.as_summary_item(ar, text, **kwargs))
