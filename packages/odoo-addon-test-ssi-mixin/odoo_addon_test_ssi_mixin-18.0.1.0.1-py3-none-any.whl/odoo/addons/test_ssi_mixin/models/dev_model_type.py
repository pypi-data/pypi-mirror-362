# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html)

from odoo import fields, models


class DevModelType(models.Model):
    _name = "dev.model.type"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Development Model Type"
    _field_name_string = "Type"

    value = fields.Integer(
        string="Numeric Value",
        help="Numeric value for development model type.",
    )
