# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "State Change Constrain Mixin",
    "version": "14.0.1.7.2",
    "category": "Administration",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_status_check_mixin",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "templates/status_check_templates.xml",
        "views/state_change_constrain_template_views.xml",
    ],
}
