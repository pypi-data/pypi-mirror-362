# -*- coding: UTF-8 -*-
# Copyright 2022-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings
from django.utils import translation

from lino.modlib.publisher.choicelists import SpecialPages

from lino.api import rt


def objects():
    Page = rt.models.publisher.Page
    for sp in SpecialPages.get_list_items():
        translated_from = None
        for lng in settings.SITE.languages:
            with translation.override(lng.django_code):
                kwargs = dict(language=lng.django_code, special_page=sp)
                kwargs.update(publishing_state="published")
                # kwargs.update(sp.default_values)
                if lng.suffix:
                    kwargs.update(translated_from=translated_from)
                obj = Page(**kwargs)
                sp.on_page_created(obj)
                yield obj
                if not lng.suffix:
                    translated_from = obj
