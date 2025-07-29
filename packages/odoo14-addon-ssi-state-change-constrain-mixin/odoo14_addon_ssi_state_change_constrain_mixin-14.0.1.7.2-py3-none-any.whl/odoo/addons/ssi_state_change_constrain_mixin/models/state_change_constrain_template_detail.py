# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import api, fields, models


class StateChangeConstrainTemplateDetail(models.Model):
    _name = "state.change.constrain.template_detail"
    _description = "Status Check Template Detail"
    _order = "sequence, id"

    template_id = fields.Many2one(
        string="State Change Constrain Template",
        comodel_name="state.change.constrain.template",
        ondelete="cascade",
    )
    company_id = fields.Many2one(
        related="template_id.company_id",
        store=True,
    )

    @api.depends(
        "template_id",
        "template_id.state_field_id",
    )
    def _compute_allowed_state_ids(self):
        obj_fields_selection = self.env["ir.model.fields.selection"]

        for document in self:
            result = []
            state_field_id = document.template_id.state_field_id
            if state_field_id:
                criteria = [("field_id", "=", state_field_id.id)]
                selection_ids = obj_fields_selection.search(criteria)
                result = selection_ids.ids
            document.allowed_state_ids = result

    allowed_state_ids = fields.Many2many(
        string="Allowed States",
        comodel_name="ir.model.fields.selection",
        compute="_compute_allowed_state_ids",
        store=False,
    )
    state_id = fields.Many2one(
        string="State",
        comodel_name="ir.model.fields.selection",
    )
    status_check_item_ids = fields.Many2many(
        string="Status Check Item",
        comodel_name="status.check.item",
        relation="rel_state_change_constrain_detail_check_item",
        column1="status_check_item_id",
        column2="state_change_constrain_detail_id",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=1,
    )
    active = fields.Boolean(
        default=True,
    )
