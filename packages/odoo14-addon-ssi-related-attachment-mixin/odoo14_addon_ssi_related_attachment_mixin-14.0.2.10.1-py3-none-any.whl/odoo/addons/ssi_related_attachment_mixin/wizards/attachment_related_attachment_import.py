# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class AttachmentRelatedAttachmentImport(models.TransientModel):
    _name = "attachment.related_attachment_import"
    _description = "Wizard for import attachment"

    action_type = fields.Selection(
        string="Type",
        selection=[
            ("select_file", "Select File"),
            ("upload_file", "Upload File"),
        ],
        default="upload_file",
    )
    file = fields.Binary(
        string="File",
    )
    filename = fields.Char(
        string="Filename",
    )
    date_manual = fields.Datetime(
        string="Date Manual",
    )

    @api.model
    def _default_allowed_attachment_ids(self):
        obj_ir_attachment = self.env["ir.attachment"]
        related_attachment = self._get_record_object()
        criteria = [
            ("res_model", "=", related_attachment.model),
            ("res_id", "=", related_attachment.res_id),
        ]
        attachment_ids = obj_ir_attachment.search(criteria)
        return attachment_ids.ids

    allowed_attachment_ids = fields.Many2many(
        string="Allowed Attachments",
        comodel_name="ir.attachment",
        default=lambda self: self._default_allowed_attachment_ids(),
        relation="rel_related_attachment_2_attachment",
        column1="wizard_id",
        column2="attachment_id",
    )
    attachment_id = fields.Many2one(
        string="Attachment",
        comodel_name="ir.attachment",
    )

    def _get_record_object(self, model=False, res_id=False):
        context = self.env.context
        if not model:
            model = context.get("active_model", False)
        if not res_id:
            res_id = context.get("active_id", False)
        object = self.env[model]
        record = object.browse(res_id).sudo()
        return record

    def action_submit(self):
        self.ensure_one()
        related_attachment = self._get_record_object()
        record = self._get_record_object(
            model=related_attachment.model, res_id=related_attachment.res_id
        )

        if self.action_type == "upload_file":
            if related_attachment.attachment_id:
                self._delete_attachment(related_attachment)
            attachment_id = self.sudo()._create_attachment(record)
            related_attachment.write({
                "attachment_id": attachment_id.id,
                "date_manual": self.date_manual,
            })
        else:
            related_attachment.write({
                "attachment_id": self.attachment_id.id,
                "date_manual": self.date_manual,
            })

    def _prepare_attachment_data(self, record):
        name = "%s" % (self.filename)
        vals = {
            "name": name,
            "type": "binary",
            "datas": self.file,
            "res_model": record._name,
            "res_id": record.id,
        }
        return vals

    def _create_attachment(self, record):
        self.ensure_one()
        obj_ir_attachment = self.env["ir.attachment"]
        attachment_id = obj_ir_attachment.create(self._prepare_attachment_data(record))
        return attachment_id

    def _delete_attachment(self, record):
        self.ensure_one()
        attachment_id = record.attachment_id
        record.write({"attachment_id": False})
        attachment_id.unlink()
        return True
