# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class TncClause(models.Model):
    _name = "tnc_clause"
    _inherit = [
        "mixin.tnc_clause",
    ]
    _description = "Terms and Condition Clause"
    _order = "section_id, sequence, id"

    section_id = fields.Many2one(
        comodel_name="tnc_section",
    )

    content = fields.Text(
        string="Content",
        compute="_compute_content",
        store=False,
        compute_sudo=True,
    )

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
