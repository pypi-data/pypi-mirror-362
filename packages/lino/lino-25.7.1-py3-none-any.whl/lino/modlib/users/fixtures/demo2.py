# -*- coding: UTF-8 -*-
# Copyright 2012-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Set password to :setting:`users.demo_password` for all users.

This is an additive fixture designed to work also on existing data.

"""

from django.conf import settings
from lino.api import dd


def objects():
    for u in settings.SITE.user_model.objects.exclude(user_type=""):
        u.set_password(dd.plugins.users.demo_password)
        yield u
