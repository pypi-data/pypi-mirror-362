# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class TncSection(models.Model):
    _name = "tnc_section"
    _description = "Terms and Condition Section"
    _inherit = [
        "mixin.tnc_section",
    ]
    _order = "sequence, id"

    model_id = fields.Many2one(
        string="Document Type",
        comodel_name="ir.model",
        index=True,
        required=True,
        ondelete="cascade",
        default=lambda self: self._default_model_id(),
        readonly=True,
    )
    model_name = fields.Char(
        related="model_id.model",
        index=True,
        store=True,
    )
    tnc_object_id = fields.Many2oneReference(
        string="Document ID",
        index=True,
        required=True,
        readonly=False,
        model_field="model_name",
    )

    @api.model
    def _selection_target_model(self):
        return [(model.model, model.name) for model in self.env["ir.model"].search([])]

    @api.depends(
        "model_id",
        "tnc_object_id",
    )
    def _compute_tnc_object_reference(self):
        for document in self:
            result = False
            if document.model_id and document.tnc_object_id:
                result = "%s,%s" % (document.model_name, document.tnc_object_id)
            document.tnc_object_reference = result

    tnc_object_reference = fields.Reference(
        string="Document Reference",
        compute="_compute_tnc_object_reference",
        store=True,
        selection="_selection_target_model",
    )

    content = fields.Text(
        string="Content",
        compute="_compute_content",
        store=False,
        compute_sudo=True,
    )
    clause_ids = fields.One2many(
        comodel_name="tnc_clause",
    )

    @api.model
    def _default_model_id(self):
        model = False
        obj_ir_model = self.env["ir.model"]
        model_name = self.env.context.get("tnc_model", False)
        if model_name:
            criteria = [("model", "=", model_name)]
            model = obj_ir_model.search(criteria)
        return model

    @api.depends(
        "raw_content",
    )
    def _compute_content(self):
        for record in self:
            MailTemplate = self.env["mail.template"]
            result = "-"
            if type(record.id) is int:
                result = MailTemplate._render_template_jinja(
                    template_txt=record.raw_content,
                    model=record._name,
                    res_ids=[record.id],
                )[record.id]
            record.content = result
