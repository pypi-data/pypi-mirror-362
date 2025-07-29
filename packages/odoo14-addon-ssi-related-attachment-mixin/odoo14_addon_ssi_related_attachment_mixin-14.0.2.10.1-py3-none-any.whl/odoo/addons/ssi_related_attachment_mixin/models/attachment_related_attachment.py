# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class AttachmentRelatedAttachment(models.Model):
    _name = "attachment.related_attachment"
    _description = "Related Attachment"
    _order = "template_id, template_detail_id"

    model = fields.Char(
        string="Related Document Model",
        index=True,
    )
    res_id = fields.Integer(
        string="Related Document ID",
        index=True,
    )
    template_id = fields.Many2one(
        string="# Template",
        comodel_name="attachment.related_attachment_template",
        ondelete="restrict",
    )
    template_detail_id = fields.Many2one(
        string="# Template Detail",
        comodel_name="attachment.related_attachment_template_detail",
        ondelete="restrict",
    )
    attachment_id = fields.Many2one(
        string="Attachment",
        comodel_name="ir.attachment",
        ondelete="restrict",
    )
    attachment_data = fields.Binary(
        string="File Content",
        related="attachment_id.datas",
        store=False,
    )
    datas_fname = fields.Char(
        string="Filename",
        related="attachment_id.name",
        store=False,
    )
    # GANTI
    category_id = fields.Many2one(
        string="Category",
        related="template_detail_id.category_id",
    )
    verify_method = fields.Selection(
        related="template_detail_id.verify_method",
        readonly=True,
    )
    date_manual = fields.Datetime(
        string="Date Manual",
    )

    @api.depends(
        "template_detail_id",
    )
    def _compute_verify_user_ids(self):
        for rec in self:
            list_user = []
            if rec.template_detail_id:
                selection_method = rec.verify_method
                user_ids = rec.template_detail_id.verify_user_ids
                if user_ids:
                    list_user += user_ids.ids

                group_ids = rec.template_detail_id.verify_group_ids
                if group_ids:
                    for group in group_ids:
                        list_user += group.users.ids

                if selection_method == "use_python":
                    python_code = rec.template_detail_id.python_code
                    result = rec._evaluate_python_code(python_code)
                    if result:
                        if "user" in result:
                            list_user += result["user"]
                        else:
                            msg_err = "No User defines on python code"
                            raise UserError(_(msg_err))
            rec.verify_user_ids = list(set(list_user))

    verify_user_ids = fields.Many2many(
        string="Users",
        comodel_name="res.users",
        compute="_compute_verify_user_ids",
        store=False,
    )
    date = fields.Datetime(
        string="Date",
        readonly=True,
    )
    user_id = fields.Many2one(
        string="Verified By",
        comodel_name="res.users",
        readonly=True,
    )

    @api.depends(
        "verify_user_ids",
        "verified",
    )
    def _compute_verify_unverify_ok(self):
        for record in self:
            verify_ok = unverify_ok = False
            if self.env.user.id in record.verify_user_ids.ids:
                if record.verified:
                    unverify_ok = True
                elif not record.verified:
                    verify_ok = True
            record.verify_ok = verify_ok
            record.unverify_ok = unverify_ok

    verify_ok = fields.Boolean(
        string="Verify Ok",
        compute="_compute_verify_unverify_ok",
    )
    unverify_ok = fields.Boolean(
        string="Unverify Ok",
        compute="_compute_verify_unverify_ok",
    )
    verified = fields.Boolean(
        string="Verified",
        default=False,
    )

    def _get_local_record(self):
        document_id = self.res_id
        document_model = self.model

        mixin_record = self.env[document_model].browse([document_id])[0]
        return mixin_record

    def _get_localdict(self):
        return {
            "rec": self._get_local_record(),
            "env": self.env,
        }

    def _evaluate_python_code(self, python_condition):
        localdict = self._get_localdict()
        result = False
        try:
            safe_eval(
                python_condition, globals_dict=localdict, mode="exec", nocopy=True
            )
            result = localdict
        except Exception:
            msg_err = "Error when execute python code"
            raise UserError(_(msg_err))

        return result

    def get_context(self):
        self.ensure_one()
        result = {}
        return result

    def action_verify_attachment(self):
        self.ensure_one()
        for record in self.sudo():
            record._verify_attachment()

    def _verify_attachment(self):
        self.ensure_one()
        if self.env.user.id in self.verify_user_ids.ids:
            self.write(
                {
                    "date": fields.Datetime.now(),
                    "user_id": self.env.user.id,
                    "verified": True,
                }
            )

    def action_unverify_attachment(self):
        for record in self.sudo():
            record._unverify_attachment()

    def _unverify_attachment(self):
        self.ensure_one()
        if self.env.user.id in self.verify_user_ids.ids:
            self.write(
                {
                    "date": False,
                    "user_id": False,
                    "verified": False,
                }
            )

    def action_unlink_attachment(self):
        for record in self.sudo():
            record._unlink_attachment()

    def _unlink_attachment(self):
        self.ensure_one()
        self.write({"attachment_id": False})

    def action_delete_attachment(self):
        for record in self.sudo():
            record._delete_attachment()

    def _delete_attachment(self):
        self.ensure_one()
        attachment = self.attachment_id
        self.write({"attachment_id": False})
        attachment.unlink()

    def unlink(self):
        _super = super()
        error_msg = _("Attachment already exist")
        for record in self:
            if record.attachment_id:
                raise UserError(error_msg)

        return _super.unlink()
