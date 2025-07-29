# -*- coding: UTF-8 -*-
# Copyright 2020-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api.ad import Plugin


class Plugin(Plugin):
    needs_plugins = [
        "lino.modlib.system",  # 'lino.modlib.memo',
        "lino.modlib.linod",
        "lino.modlib.jinja",
        "lino.modlib.bootstrap3",
    ]
    locations = []

    def setup_main_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action("publisher.Pages")

    def setup_config_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action("publisher.SpecialPages")

    def get_requirements(self, site):
        yield "python-lorem"

    def post_site_startup(self, site):
        from lino.core.actors import Actor
        from .renderer import Renderer
        from .mixins import Publishable

        super().post_site_startup(site)
        self.renderer = Renderer(self)

        locations = []
        for loc, view in self.locations:
            app_label, model_name = view.split(".")
            app = site.models.get(app_label)
            cls = getattr(app, model_name, None)
            if not isinstance(cls, type) or not issubclass(cls, Actor):
                raise Exception("location {}: {} is not an Actor".format(view, cls))
            if not issubclass(cls.model, Publishable):
                raise Exception(
                    "location {}: model is a {}, which is not Publishable".format(
                        view, type(cls.model)
                    )
                )

            cls.model._lino_publisher_location = loc
            locations.append((loc, cls))
        self.locations = tuple(locations)

    def get_patterns(self):
        from django.urls import re_path as url
        from lino.core.utils import models_by_base
        from . import views
        # from .choicelists import PublisherViews
        # raise Exception("20220927")
        # print("20220927", list(PublisherViews.get_list_items()))

        # for pv in PublisherViews.get_list_items():
        for publisher_location, table_class in self.locations:
            # print("20220927", pv.publisher_location)
            # if publisher_location is not None:
            yield url(
                "^{}/(?P<pk>.+)$".format(publisher_location),
                views.Element.as_view(table_class=table_class),
            )

        yield url("^$", views.Index.as_view())
        # yield url('^login$',views.Login.as_view())
