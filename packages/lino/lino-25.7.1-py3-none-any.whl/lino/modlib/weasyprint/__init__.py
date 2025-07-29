# Copyright 2016-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""This plugins installs two build methods for generating
:term:`printable documents <printable document>` using `weasyprint
<https://weasyprint.org/>`__.

See :doc:`/specs/weasyprint`.

"""

# trying to get rid of disturbing warnings in
# https://travis-ci.org/lino-framework/book/jobs/260560833
# import warnings
# warnings.filterwarnings(
#     "ignore", 'There are known rendering problems')
# warnings.filterwarnings(
#     "ignore", '@font-face support needs Pango >= 1.38')

try:
    import imagesize
except ImportError:
    imagesize = None

from lino.api import ad, _


class Plugin(ad.Plugin):

    verbose_name = _("WeasyPrint")
    needs_plugins = ["lino.modlib.jinja"]

    header_height = 20
    footer_height = 20
    top_right_width = None
    page_background_image = None
    top_right_image = None
    header_image = None
    margin = 10
    margin_left = 17
    margin_right = 10
    space_before_recipient = 15

    def get_requirements(self, site):
        yield "imagesize"

    def pre_site_startup(self, site):
        for ext in ("jpg", "png"):
            if self.header_height:
                fn = site.confdirs.find_config_file("top-right." + ext, "weasyprint")
                if fn:
                    self.top_right_image = fn
                    if self.top_right_width is None:
                        if imagesize is None:
                            site.logger.warning("imagesize is not installed")
                            continue
                        w, h = imagesize.get(fn)
                        self.top_right_width = self.header_height * w / h
                fn = site.confdirs.find_config_file("header." + ext, "weasyprint")
                if fn:
                    # site.logger.info("Found header_image %s", fn)
                    self.header_image = fn
            if self.page_background_image is None:
                fn = site.confdirs.find_config_file(
                    "page-background." + ext, "weasyprint")
                if fn:
                    # site.logger.info("Found page_background_image %s", fn)
                    self.page_background_image = fn
        super().pre_site_startup(site)
