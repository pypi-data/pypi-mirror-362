# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CustomInfoProperty(models.Model):
    _description = "Custom information property"
    _name = "custom_info.property"

    name = fields.Char(
        required=True,
        translate=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
    field_type = fields.Selection(
        selection=[
            ("str", "Text"),
            ("int", "Whole number"),
            ("float", "Decimal number"),
            ("bool", "Yes/No"),
            ("id", "Selection"),
            ("ids", "Multiple Selection"),
            ("date", "Date"),
            ("datetime", "Datetime"),
        ],
        default="str",
        required=True,
    )
    option_set_id = fields.Many2one(
        string="Option Set",
        comodel_name="custom_info.option_set",
    )
    option_ids = fields.Many2many(
        string="Options",
        comodel_name="custom_info.option",
        related="option_set_id.option_ids",
        store=False,
        readonly=True,
    )
