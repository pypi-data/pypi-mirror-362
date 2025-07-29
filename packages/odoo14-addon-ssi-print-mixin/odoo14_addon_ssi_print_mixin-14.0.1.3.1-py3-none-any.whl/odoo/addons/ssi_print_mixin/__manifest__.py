# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Print Policy Mixin",
    "version": "14.0.1.3.1",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "base",
        "mail",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/base_print_document.xml",
        "templates/mixin_print_templates.xml",
        "views/print_document_type_views.xml",
        "views/ir_actions_report_views.xml",
    ],
}
