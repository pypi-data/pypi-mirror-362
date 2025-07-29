# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CustomInfoTemplateDetail(models.Model):
    _description = "Custom Information Template Detail"
    _name = "custom_info.template_detail"
    _order = "template_id, property_id"
    _sql_constraints = [
        (
            "template_property",
            "UNIQUE (template_id, property_id)",
            "Another Property with that name exists for that Template.",
        ),
    ]

    template_id = fields.Many2one(
        string="Template",
        comodel_name="custom_info.template",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=True,
    )
    property_id = fields.Many2one(
        string="Property",
        comodel_name="custom_info.property",
        required=True,
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="custom_info.category",
    )
