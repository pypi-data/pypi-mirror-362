# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Multiple Approval",
    "version": "14.0.1.10.2",
    "category": "Administration",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "base",
        "ssi_decorator",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "templates/mixin_multiple_approval_templates.xml",
        "views/approval_template_detail_views.xml",
        "views/approval_template_views.xml",
        "views/approval_approval_views.xml",
    ],
}
