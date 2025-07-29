# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import test_python_expr


class StateChangeConstrainTemplate(models.Model):
    _name = "state.change.constrain.template"
    _description = "State Change Constrain Template"
    _order = "sequence"

    DEFAULT_PYTHON_CODE = """# Available variables:
#  - env: Odoo Environment on which the action is triggered.
#  - document: record on which the action is triggered; may be void."""

    @api.model
    def _default_company_id(self):
        return self.env["res.company"]._company_default_get(
            "state.change.constrain.template"
        )

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
    state_field_id = fields.Many2one(
        string="State Field",
        comodel_name="ir.model.fields",
        required=True,
        ondelete="cascade",
        domain="[('ttype', '=', 'selection'), ('model_id', '=', model_id)]",
        copy=True,
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        default=lambda self: self._default_company_id(),
    )
    status_check_template_id = fields.Many2one(
        string="Status Check Template",
        comodel_name="status.check.template",
        index=True,
        required=True,
    )

    @api.depends("status_check_template_id")
    def _compute_allowed_check_item_ids(self):
        obj_status_check_template = self.env["status.check.template"]
        item_ids = []
        for document in self:
            if document.status_check_template_id:
                template_id = obj_status_check_template.search(
                    [("id", "=", document.status_check_template_id.id)]
                )
                if template_id:
                    item_ids = template_id.mapped("detail_ids").mapped(
                        "status_check_item_id"
                    )
            document.allowed_check_item_ids = item_ids

    allowed_check_item_ids = fields.Many2many(
        string="Allowed Check Items",
        comodel_name="status.check.item",
        compute="_compute_allowed_check_item_ids",
        store=False,
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Notes",
    )
    python_code = fields.Text(
        string="Python Code",
        default=DEFAULT_PYTHON_CODE
        + "\n# - result: Return result, the value is boolean.",
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="state.change.constrain.template_detail",
        inverse_name="template_id",
    )

    def name_get(self):
        result = []
        for record in self:
            if record.name == "/":
                name = "*" + str(record.id)
            else:
                name = record.name
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
