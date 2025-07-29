# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class IrModel(models.Model):
    _name = "ir.model"
    _inherit = "ir.model"

    related_attchment_include_field_ids = fields.Many2many(
        string="Related Attachment Trigger Fields",
        comodel_name="ir.model.fields",
        relation="rel_model_2_related_attachment_trigger_field",
        column1="model_id",
        column2="field_id",
        domain="[('model_id', '=', id)]",
    )
