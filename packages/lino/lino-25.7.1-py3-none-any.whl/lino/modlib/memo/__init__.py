# Copyright 2008-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""See :doc:`/specs/memo`.

Adds functionality for using memo commands in your text fields.

.. autosummary::
   :toctree:

   parser


"""

# from importlib import import_module
# from rstgen.utils import py2url_txt
from lino.api import ad
from .parser import Parser, split_name_rest
from lino.utils.html import tostring


class Plugin(ad.Plugin):
    """Base class for this plugin.

    .. attribute:: parser

        An instance of :class:`lino.modlib.memo.parser.Parser`.

    """

    # needs_plugins = ['lino.modlib.gfks', 'lino.modlib.jinja']
    needs_plugins = ["lino.modlib.office", "lino.modlib.gfks"]

    # parser_user = 'memo'
    # """The username of the special user used when parsing preview fields.
    #
    # Preview fields have their memo commands replaced by html, so they are the
    # same for everybody. Even an anonymous user will see a link to the detail of
    # a customer, but when they click on it, they will see data only after
    # authenticating.
    #
    # """

    use_markup = False

    front_end = None
    # front_end = 'extjs'
    # front_end = 'lino_react.react'
    # front_end = 'bootstrap3'
    """The front end to use when writing previews.

    If this is `None`, Lino will use the default :term:`front end`
    (:attr:`lino.core.site.Site.web_front_ends`).

    Used on sites that are available through more than one web front ends.  The
    :term:`server administrator` must then decide which front end is the primary
    one.

    """

    short_preview_length = 300
    # short_preview_image_height = "8em"

    def get_requirements(self, site):
        if self.use_markup:
            yield "markdown"

    def on_plugins_loaded(self, site):
        self.parser = Parser()

        # def url2html(ar, s, cmdname, mentions, context):
        #     url, text = split_name_rest(s)
        #     if text is None:
        #         text = url
        #     return '<a href="%s" target="_blank">%s</a>' % (url, text)
        #
        # self.parser.register_command("url", url2html)

        # 20240920 I disabled the "py" memo command because I don't know anybody
        # who used it (except myself a few times for testing it) and because it
        # requires SETUP_INFO, which has an uncertain future.

        # def py2html(parser, s, cmdname, mentions, context):
        #     url, txt = py2url_txt(s)
        #     if url:
        #         # lines = inspect.getsourcelines(s)
        #         return '<a href="{0}" target="_blank">{1}</a>'.format(url, txt)
        #     return "<pre>{}</pre>".format(s)
        #
        # self.parser.register_command("py", py2html)

        def show2html(ar, s, cmdname, mentions, context):
            # kwargs = dict(header_level=3)  #, nosummary=True)
            kwargs = dict()  # , nosummary=True)
            dv = self.site.models.resolve(s)
            sar = dv.create_request(parent=ar, limit=dv.preview_limit)
            rv = ""
            # rv += "20230325 [show {}]".format(dv)
            for e in sar.renderer.table2story(sar, **kwargs):
                rv += tostring(e)
            return rv

        self.parser.register_command("show", show2html)

        if False:
            # letting website users execute arbitrary code is a security risk
            def eval2html(ar, s, cmdname, mentions, context):
                from django.conf import settings  # context of exec command

                sar = ar.spawn_request(renderer=settings.SITE.kernel.html_renderer)
                return eval(compile(s, cmdname, "eval"))

            self.parser.register_command("eval", eval2html)

    def post_site_startup(self, site):
        if self.front_end is None:
            self.front_end = site.kernel.editing_front_end
            # web_front_ends[0]
        else:
            self.front_end = site.plugins.resolve(self.front_end)

        if site.user_model is None:
            return
        # pu, created = site.user_model.objects.get_or_create(
        #     username=self.parser_user, user_type=site.models.users.UserTypes.admin)
        # if created:
        #     pu.set_unusable_password()
        #     pu.full_clean()
        #     pu.save()

        from lino.core.requests import BaseRequest
        from lino.core.auth.utils import AnonymousUser
        from lino.modlib.users.choicelists import UserTypes

        pu = AnonymousUser("memo", UserTypes.admin)
        self.ar = BaseRequest(
            user=pu, renderer=self.front_end.renderer, permalink_uris=True
        )

        # front_end = None
        #
        # for k in self.front_end_candidates:
        #     try:
        #         m = import_module(k)
        #     except ImportError:
        #         continue
        #     front_end = m
        #     break

    def get_patterns(self):
        # from django.conf.urls import url
        from django.urls import re_path as url
        from . import views

        return [url("^suggestions$", views.Suggestions.as_view())]

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        mg = site.plugins.office
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action("memo.Mentions")
        # m.add_action("about.About.insert_reference")

    # def get_quicklinks(self):
    #     yield "about.About.insert_reference"
