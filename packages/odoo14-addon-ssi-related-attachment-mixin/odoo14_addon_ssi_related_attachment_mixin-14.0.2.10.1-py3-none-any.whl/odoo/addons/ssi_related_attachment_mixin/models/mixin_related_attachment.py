# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval

from odoo.addons.ssi_decorator import ssi_decorator


class MixinRelatedAttachment(models.AbstractModel):
    _name = "mixin.related_attachment"
    _inherit = [
        "mixin.decorator",
    ]
    _description = "Mixin Object for Related Attachment"

    _related_attachment_create_page = False
    _related_attachment_page_xpath = "//page[last()]"

    def _compute_allowed_related_attachment_template_ids(self):
        obj_template = self.env["attachment.related_attachment_template"]
        for record in self:
            criteria = [("model", "=", self._name)]
            result = obj_template.search(criteria).ids
            record.allowed_related_attachment_template_ids = result

    related_attachment_template_id = fields.Many2one(
        string="Related Attachment Template",
        comodel_name="attachment.related_attachment_template",
        copy=False,
        domain=lambda self: [("model", "=", self._name)],
    )
    allowed_related_attachment_template_ids = fields.Many2many(
        string="Allowed Related Attachment Template",
        comodel_name="attachment.related_attachment_template",
        compute="_compute_allowed_related_attachment_template_ids",
        store=False,
    )
    related_attachment_ids = fields.One2many(
        string="Related Attachments",
        comodel_name="attachment.related_attachment",
        inverse_name="res_id",
        domain=lambda self: [("model", "=", self._name)],
        auto_join=True,
    )
    num_of_related_attachment = fields.Integer(
        string="Num. of Related Attachments",
        compute="_compute_num_of_related_attachment",
        store=True,
        compute_sudo=True,
        help="Number of all related attchments",
    )
    num_of_verified_related_attachment = fields.Integer(
        string="Num. of Verified Related Attachments",
        compute="_compute_num_of_related_attachment",
        store=True,
        compute_sudo=True,
        help="Number of verified related attchments",
    )
    num_of_unverified_related_attachment = fields.Integer(
        string="Num. of Unverified Related Attachments",
        compute="_compute_num_of_related_attachment",
        store=True,
        compute_sudo=True,
        help="Number of unverified related attchments",
    )
    related_attchment_status = fields.Selection(
        string="Related Attachment Status",
        selection=[
            ("not_needed", "Not Needed"),
            ("open", "In Progress"),
            ("done", "Done"),
        ],
        compute="_compute_related_attchment_status",
        store=True,
        compute_sudo=True,
        help="Related attachment status.\n\n"
        "This will change when users verified/unverified related attchments\n"
        "Not Needed: No related attchment for this document\n"
        "In Progress: There is/are unverified related attachments\n"
        "Done: All related attchment verified",
    )

    @api.depends(
        "related_attachment_ids",
        "related_attachment_ids.verified",
    )
    def _compute_num_of_related_attachment(self):
        for record in self:
            num_of_attachment = num_of_verified_attachment = (
                num_of_unverified_attachment
            ) = 0
            criteria = [
                ("model", "=", self._name),
                ("res_id", "=", record.id),
                ("category_id", "!=", False),
            ]
            RelatedAttachment = self.env["attachment.related_attachment"]

            for attachment in RelatedAttachment.search(criteria):
                num_of_attachment += 1
                if attachment.verified:
                    num_of_verified_attachment += 1
                else:
                    num_of_unverified_attachment += 1
            record.num_of_related_attachment = num_of_attachment
            record.num_of_verified_related_attachment = num_of_verified_attachment
            record.num_of_unverified_related_attachment = num_of_unverified_attachment

    @api.depends(
        "num_of_related_attachment",
        "num_of_verified_related_attachment",
    )
    def _compute_related_attchment_status(self):
        for record in self:
            result = "not_needed"
            if (
                record.num_of_related_attachment != 0
                and record.num_of_related_attachment
                != record.num_of_verified_related_attachment
            ):
                result = "open"
            elif (
                record.num_of_related_attachment != 0
                and record.num_of_related_attachment
                == record.num_of_verified_related_attachment
            ):
                result = "done"

            record.related_attchment_status = result

    @ssi_decorator.insert_on_form_view()
    def _related_attachment_insert_form_element(self, view_arch):
        if self._related_attachment_create_page:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id="ssi_related_attachment_mixin.related_attachment_page",
                xpath=self._related_attachment_page_xpath,
                position="after",
            )
        return view_arch

    def _get_related_attachment_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    def _evaluate_related_attachment(self, template):
        self.ensure_one()
        res = False
        localdict = self._get_related_attachment_localdict()
        if template:
            try:
                safe_eval(template.python_code, localdict, mode="exec", nocopy=True)
                if "result" in localdict:
                    res = localdict["result"]
            except Exception as error:
                error_message = """Context: Related Attachment
Error: %s
""" % (
                    error
                )
                raise UserError(_(error_message))
        return res

    def _get_template_related_attachment(self):
        result = False
        obj_related_attachment_template = self.env[
            "attachment.related_attachment_template"
        ]
        criteria = [
            ("model_id.model", "=", str(self._name)),
        ]
        templates = obj_related_attachment_template.search(
            criteria,
        )
        for template in templates:
            if self._evaluate_related_attachment(template):
                result = template.id
                return result
        return result

    # @api.onchange(
    #     "related_attachment_template_id",
    # )
    # def onchange_related_attachment_ids(self):
    #     res = []
    #     if self.related_attachment_ids:
    #         to_check = self.related_attachment_ids.mapped("attachment_id")
    #         if to_check:
    #             error_msg = _("Attachment already exist")
    #             raise UserError(_("%s") % (error_msg))
    #     self.related_attachment_ids = [(5, 0, 0)]
    #     if self.related_attachment_template_id:
    #         res = self.create_related_attachment_ids()
    #     self.related_attachment_ids = res

    def create_related_attachment_ids(self):
        self.ensure_one()
        TemplateDetail = self.env["attachment.related_attachment_template_detail"]
        RelatedAttachment = res = self.env["attachment.related_attachment"]
        criteria = [("template_id", "=", self.related_attachment_template_id.id)]
        related_attachment_ids = TemplateDetail.search(criteria, order="sequence")
        if related_attachment_ids:
            for related_attachment in related_attachment_ids:
                RelatedAttachment.create(
                    {
                        "model": self._name,
                        "res_id": self.id,
                        "template_id": self.related_attachment_template_id.id,
                        "template_detail_id": related_attachment.id,
                    }
                )
        return res

    def action_reload_rel_attachment_template(self):
        for record in self.sudo():
            record.write(
                {
                    "related_attachment_template_id": self._get_template_related_attachment(),
                }
            )
            record._reload_rel_attachment_detail()

    def action_reload_rel_attachment_detail(self):
        for record in self.sudo():
            record._reload_rel_attachment_detail()

    def _reload_rel_attachment_detail(self):
        self.ensure_one()
        if self.related_attachment_template_id:
            template = self.related_attachment_template_id
            allowed_details = template.detail_ids
            self.related_attachment_ids.filtered(
                lambda r: r.template_detail_id.id not in allowed_details.ids
            ).unlink()
            to_be_added = template.detail_ids - self.related_attachment_ids.mapped(
                "template_detail_id"
            )
            for detail in to_be_added:
                data = {
                    "model": self._name,
                    "res_id": self.id,
                    "template_id": template.id,
                    "template_detail_id": detail.id,
                }
                self.write({"related_attachment_ids": [(0, 0, data)]})
        else:
            self.related_attachment_ids.unlink()
        self._compute_num_of_related_attachment()

    def unlink(self):
        related_attachments = self.mapped("related_attachment_ids")
        res = super().unlink()
        if res:
            related_attachments.unlink()
        return res

    @api.model
    def create(self, values):
        _super = super()
        result = _super.create(values)
        if not result.related_attachment_template_id:
            template_id = result._get_template_related_attachment()
            if template_id:
                result.sudo().write({"related_attachment_template_id": template_id})
        if result.related_attachment_template_id:
            result.sudo().action_reload_rel_attachment_detail()
        return result
