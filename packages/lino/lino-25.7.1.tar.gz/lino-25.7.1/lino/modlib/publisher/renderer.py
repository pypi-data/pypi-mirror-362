# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino import logger
from lino.core.renderer import add_user_language
from lino.modlib.bootstrap3.renderer import Renderer


class Renderer(Renderer):
    def __init__(self, front_end):
        super().__init__(front_end)
        dr = front_end.site.kernel.default_renderer
        for k in ("row_action_button", "get_detail_url"):
            setattr(self, k, getattr(dr, k))

    def get_request_url(self, ar, *args, **kwargs):
        obj = ar.selected_rows[0]
        return self.obj2url(ar, obj, **kwargs)
        # return obj.publisher_url(ar, **kwargs)

    def obj2url(self, ar, obj, **kwargs):
        # if ar.actor is None or not isinstance(obj, ar.actor.model):
        loc = obj.__class__._lino_publisher_location
        if loc is None:
            # logger.warning("No location for %s", obj.__class__)
            return None
        add_user_language(kwargs, ar)
        return self.front_end.buildurl(loc, str(obj.pk), **kwargs)
        # for i in PublisherViews.get_list_items():
        #     if isinstance(obj, i.table_class.model):
        #         # print("20230409", self.__class__, i)
        #         # return "/{}/{}".format(i.publisher_location, self.pk)
        #         add_user_language(kwargs, ar)
        #         # return buildurl("/" + i.publisher_location, str(self.pk), **dd.urlkwargs())
        #         return self.front_end.buildurl(i.publisher_location, str(obj.pk), **kwargs)
        if True:
            # leave the author of a blog entry unclickable when there is no
            # publisher view,
            return None
        return self.front_end.site.kernel.default_renderer.obj2url(ar, obj, **kwargs)
        # return super().obj2url(ar, obj, **kwargs)
