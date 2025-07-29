# -*- coding: UTF-8 -*-
# Copyright 2016-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from pathlib import Path
from lino.modlib.jinja.choicelists import JinjaBuildMethod
from lino.modlib.printing.choicelists import BuildMethods

try:
    from weasyprint import HTML
except ImportError:
    HTML = None

try:
    import bulma
    from weasyprint import CSS
    BULMA_CSS = Path(bulma.__file__).parent / "static/bulma/css/style.min.css"
    assert BULMA_CSS.exists()
except ImportError:
    BULMA_CSS = None


class WeasyBuildMethod(JinjaBuildMethod):
    template_ext = ".weasy.html"
    templates_name = "weasy"
    default_template = "default.weasy.html"


class WeasyHtmlBuildMethod(WeasyBuildMethod):
    target_ext = ".html"
    name = "weasy2html"


class WeasyPdfBuildMethod(WeasyBuildMethod):
    target_ext = ".pdf"
    name = "weasy2pdf"

    def html2file(self, html, filename, context):
        pdf = HTML(string=html)
        if BULMA_CSS and context.get('use_bulma_css', False):
            pdf.write_pdf(filename, stylesheets=[CSS(filename=BULMA_CSS)])
        else:
            pdf.write_pdf(filename)


add = BuildMethods.add_item_instance
add(WeasyHtmlBuildMethod())
add(WeasyPdfBuildMethod())
