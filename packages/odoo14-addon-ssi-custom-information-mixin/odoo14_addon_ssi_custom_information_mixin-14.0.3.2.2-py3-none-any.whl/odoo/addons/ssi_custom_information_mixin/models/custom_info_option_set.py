# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CustomInfoOptionSet(models.Model):
    _description = "Option Sets for Custom Information"
    _name = "custom_info.option_set"

    name = fields.Char(
        index=True,
        translate=True,
        required=True,
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
    option_ids = fields.Many2many(
        string="Options",
        comodel_name="custom_info.option",
        relation="rel_option_set_2_option",
        column1="set_id",
        column2="option_id",
    )
