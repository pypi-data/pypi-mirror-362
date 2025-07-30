# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Sequence Mixin",
    "version": "18.0.1.0.1",
    "category": "Administration",
    "website": "https://github.com/open-synergy/ssi-mixin",
    "author": "PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "views/sequence_template_views.xml",
    ],
}
