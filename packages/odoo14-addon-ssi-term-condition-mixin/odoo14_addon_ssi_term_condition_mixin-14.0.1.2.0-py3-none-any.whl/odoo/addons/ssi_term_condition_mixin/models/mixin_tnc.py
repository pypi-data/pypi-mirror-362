# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class MixinTnc(models.AbstractModel):
    _name = "mixin.tnc"
    _description = "Terms and Conditions Mixin"
    _tnc_create_page = False
    _tnc_page_xpath = "//page[@name='note']"

    allowed_tnc_template_ids = fields.Many2many(
        string="Allowed T&C Templates",
        comodel_name="tnc_template",
        compute="_compute_allowed_tnc_template_ids",
        store=False,
    )
    tnc_template_id = fields.Many2one(
        string="T&C Template",
        comodel_name="tnc_template",
        ondelete="restrict",
    )
    tnc_section_ids = fields.One2many(
        string="T&C Section",
        comodel_name="tnc_section",
        inverse_name="tnc_object_id",
        domain=lambda self: [("model_name", "=", self._name)],
        auto_join=True,
        readonly=False,
        copy=True,
    )
    tnc_clause_ids = fields.Many2many(
        string="Clauses",
        comodel_name="tnc_clause",
        compute="_compute_tnc_clause_ids",
        copy=True,
    )

    @api.depends("tnc_section_ids", "tnc_section_ids.clause_ids")
    def _compute_tnc_clause_ids(self):
        for record in self:
            result = record.mapped("tnc_section_ids.clause_ids")
            record.tnc_clause_ids = result

    def _compute_allowed_tnc_template_ids(self):
        for record in self:
            criteria = [
                ("model_id.model", "=", self._name),
            ]
            result = self.env["tnc_template"].search(criteria)
            record.allowed_tnc_template_ids = result

    def action_generate_tnc(self):
        for record in self.sudo():
            record._generate_tnc()

    def _generate_tnc(self):
        self.ensure_one()

        self.tnc_section_ids.unlink()

        if not self.tnc_template_id:
            return True

        for section in self.tnc_template_id.section_ids:
            section._create_tnc_section(self)

    @ssi_decorator.insert_on_form_view()
    def _view_add_form_tnc_page(self, view_arch):
        if self._tnc_create_page:
            view_arch = self._add_view_element(
                view_arch,
                "ssi_term_condition_mixin.tnc_page",
                self._tnc_page_xpath,
                "before",
            )
        return view_arch
