# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class TncTemplateSection(models.Model):
    _name = "tnc_template.section"
    _inherit = [
        "mixin.tnc_section",
    ]
    _description = "T&C Template Section"
    _order = "sequence, id"

    template_id = fields.Many2one(
        string="Template",
        comodel_name="tnc_template",
        required=True,
        ondelete="cascade",
    )
    clause_ids = fields.One2many(
        comodel_name="tnc_template.clause",
    )

    def _create_tnc_section(self, tnc_object):
        self.ensure_one()
        TNCSection = self.env["tnc_section"]
        data = self._prepare_section_data(tnc_object)
        section = TNCSection.create(data)

        for clause in self.clause_ids:
            clause._create_tnc_clause(section)

    def _prepare_section_data(self, tnc_object):
        self.ensure_one()
        model = self.env["ir.model"].search([("model", "=", tnc_object._name)])[0]
        return {
            "name": self.name,
            "title": self.title,
            "sequence": self.sequence,
            "raw_content": self.raw_content,
            "model_id": model.id,
            "tnc_object_id": tnc_object.id,
        }
