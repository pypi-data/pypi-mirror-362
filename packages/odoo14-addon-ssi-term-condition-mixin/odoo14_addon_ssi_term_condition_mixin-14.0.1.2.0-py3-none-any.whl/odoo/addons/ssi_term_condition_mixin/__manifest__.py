# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Terms and Conditions Mixin",
    "version": "14.0.1.2.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "mail",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "templates/tnc_templates.xml",
        "views/tnc_section_views.xml",
        "views/tnc_clause_views.xml",
        "views/tnc_template_section_views.xml",
        "views/tnc_template_clause_views.xml",
        "views/tnc_template_views.xml",
        # "views/ir_model_views.xml",
    ],
    "demo": [],
}
