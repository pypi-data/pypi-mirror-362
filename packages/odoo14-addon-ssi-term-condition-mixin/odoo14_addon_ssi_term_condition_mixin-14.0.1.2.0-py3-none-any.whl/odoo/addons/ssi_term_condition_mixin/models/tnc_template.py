# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import test_python_expr


class TncTemplate(models.Model):
    _name = "tnc_template"
    _description = "T&C Template"
    _order = "sequence, id"

    DEFAULT_PYTHON_CODE = """# Available variables:
#  - env: Odoo Environment on which the action is triggered.
#  - document: record on which the action is triggered; may be void."""

    @api.model
    def _default_company_id(self):
        return self.env["res.company"]._company_default_get("approval.template")

    name = fields.Char(
        string="Name",
        required=True,
    )
    model_id = fields.Many2one(
        string="Referenced Model",
        comodel_name="ir.model",
        index=True,
        required=True,
        ondelete="cascade",
    )
    model = fields.Char(
        related="model_id.model",
        index=True,
        store=True,
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        default=lambda self: self._default_company_id(),
    )
    sequence = fields.Integer(
        default=1,
        required=True,
    )
    active = fields.Boolean(
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
    computation_method = fields.Selection(
        string="Computation Method",
        selection=[
            ("use_domain", "Domain"),
            ("use_python", "Python Code"),
        ],
        default="use_python",
        required=True,
    )
    domain = fields.Char(
        string="Domain",
    )
    python_code = fields.Text(
        string="Python Code",
        default=DEFAULT_PYTHON_CODE
        + "\n#  - result: Return result, the value is boolean.",
        copy=True,
    )
    section_ids = fields.One2many(
        string="Sections",
        comodel_name="tnc_template.section",
        inverse_name="template_id",
    )
    clause_ids = fields.Many2many(
        string="Clauses",
        comodel_name="tnc_template.clause",
        compute="_compute_clause_ids",
        copy=True,
    )

    @api.depends("section_ids", "section_ids.clause_ids")
    def _compute_clause_ids(self):
        for record in self:
            result = record.mapped("section_ids.clause_ids")
            record.clause_ids = result

    def name_get(self):
        result = []
        for record in self:
            name = "[{}] {}".format(record.model, record.name)
            result.append((record.id, name))
        return result

    @api.constrains(
        "python_code",
    )
    def _check_python_code(self):
        for action in self.sudo().filtered("python_code"):
            msg = test_python_expr(expr=action.python_code.strip(), mode="exec")
            if msg:
                raise ValidationError(msg)
