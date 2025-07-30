# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Print Policy Mixin",
    "author": "PT. Simetri Sinergi Indonesia",
    "version": "18.0.1.0.1",
    "website": "https://github.com/open-synergy/ssi-mixin",
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
