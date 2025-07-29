# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json

from odoo import _, api, fields, models
from odoo.tools.misc import formatLang, get_lang


class CustomInfoValue(models.Model):
    _description = "Custom information value"
    _name = "custom_info.value"
    _rec_name = "value"

    model = fields.Char(
        string="Related Document Model",
        index=True,
    )
    res_id = fields.Integer(
        string="Related Document ID",
        index=True,
    )
    detail_id = fields.Many2one(
        comodel_name="custom_info.template_detail",
        required=True,
        string="Template Detail",
    )
    property_id = fields.Many2one(
        comodel_name="custom_info.property",
        related="detail_id.property_id",
        string="Property",
    )
    sequence = fields.Integer(
        index=True,
        readonly=True,
        related="detail_id.sequence",
        store=True,
    )
    category_id = fields.Many2one(
        related="detail_id.category_id",
        store=True,
        readonly=True,
    )
    name = fields.Char(
        related="property_id.name",
        readonly=True,
    )
    field_type = fields.Selection(
        related="property_id.field_type",
        readonly=True,
    )

    @api.depends(
        "property_id.field_type",
    )
    def _compute_field_name(self):
        """Get the technical name where the real typed value is stored."""
        for s in self:
            s.field_name = "value_{!s}".format(s.property_id.field_type)

    field_name = fields.Char(
        compute="_compute_field_name",
        help="Technical name of the field where the value is stored.",
    )

    @api.model
    def _search_value(self, operator, value):
        """Search from the stored field directly."""
        options = (
            o[0]
            for o in self.property_id._fields["field_type"].get_description(self.env)[
                "selection"
            ]
        )
        domain = []
        for fmt in options:
            try:
                _value = (
                    self._transform_value(value, fmt)
                    if not isinstance(value, list)
                    else [self._transform_value(v, fmt) for v in value]
                )
            except ValueError:
                # If you are searching something that cannot be casted, then
                # your property is probably from another type
                continue
            domain += [
                "&",
                ("field_type", "=", fmt),
                ("value_" + fmt, operator, _value),
            ]
        return ["|"] * (len(domain) / 3 - 1) + domain

    @api.depends(
        "property_id.field_type",
        "field_name",
        "value_str",
        "value_int",
        "value_float",
        "value_bool",
        "value_id",
    )
    def _compute_value(self):
        """Get the value as a string, from the original field."""
        for s in self:
            if s.field_type == "id":
                s.value = s.value_id.display_name
            elif s.field_type == "bool":
                s.value = _("Yes") if s.value_bool else _("No")
            elif s.field_type == "date":
                s.value = getattr(s, s.field_name, False)
            elif s.field_type == "datetime":
                s.value = getattr(s, s.field_name, False)
            elif s.field_type == "ids":
                num_ids = 1
                result = ""
                for value in s.value_ids:
                    result += "{}) {} \n".format(num_ids, value.name)
                    num_ids += 1
                s.value = result
            elif s.field_type in ["int", "float"]:
                if s.field_type == "int":
                    fmt = "%.{0}f".format(0)
                else:
                    fmt = "%.{0}f".format(2)
                lang = get_lang(self.env)
                amount = float(getattr(s, s.field_name, False))
                formatted_amount = lang.format(fmt, amount, grouping=True, monetary=True)
                s.value = formatted_amount
            else:
                s.value = getattr(s, s.field_name, False)

    value = fields.Char(
        compute="_compute_value",
        help="Value, always converted to/from the typed field.",
    )
    value_str = fields.Char(string="Text value", translate=True, index=True)
    value_int = fields.Integer(
        string="Whole number value",
        index=True,
    )
    value_float = fields.Float(
        string="Decimal number value",
        index=True,
    )
    value_bool = fields.Boolean(
        string="Yes/No value",
        index=True,
    )
    value_date = fields.Date(
        string="Date value",
        index=True,
    )
    value_datetime = fields.Datetime(
        string="Datetime value",
        index=True,
    )
    value_id = fields.Many2one(
        string="Selection value",
        comodel_name="custom_info.option",
        ondelete="cascade",
        domain="[]",
    )
    value_ids = fields.Many2many(
        string="Multiple Selection value",
        comodel_name="custom_info.option",
        relation="rel_custom_info_value_2_option",
        column1="value_id",
        column2="option_id",
    )

    @api.depends(
        "detail_id",
    )
    def _compute_allowed_option_ids(self):
        for record in self:
            result = []
            if record.detail_id and record.detail_id.property_id.field_type in [
                "id",
                "ids",
            ]:
                result = record.detail_id.property_id.option_set_id.option_ids
            record.allowed_option_ids = result

    allowed_option_ids = fields.Many2many(
        string="Allowed Options",
        comodel_name="custom_info.option",
        compute="_compute_allowed_option_ids",
        store=False,
    )
