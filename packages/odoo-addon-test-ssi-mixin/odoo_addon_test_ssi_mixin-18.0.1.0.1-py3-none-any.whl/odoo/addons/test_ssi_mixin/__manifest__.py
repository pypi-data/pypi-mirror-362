# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html)
{
    "name": "Development Model for Testing Mixin",
    "summary": "Development Model for Testing Mixin",
    "version": "18.0.1.0.1",
    "website": "https://github.com/open-synergy/ssi-mixin",
    "category": "Tools",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "ssi_master_data_mixin",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/dev_model_type_data.xml",
        "menu.xml",
        "views/dev_model_type_view.xml",
    ],
}
