# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class MixinStateChangeConstrain(models.AbstractModel):
    _name = "mixin.state_change_constrain"
    _description = "Mixin Object for State Change Constrain"

    state_change_constrain_template_id = fields.Many2one(
        string="State Change Constrain Template",
        comodel_name="state.change.constrain.template",
        domain=lambda self: [("model", "=", self._name)],
        copy=False,
    )

    def _get_state_change_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    def _evaluate_state_change(self, template):
        self.ensure_one()
        res = False
        localdict = self._get_state_change_localdict()
        try:
            safe_eval(template.python_code, localdict, mode="exec", nocopy=True)
            if "result" in localdict:
                res = localdict["result"]
        except Exception as error:
            raise UserError(_("Error evaluating conditions.\n %s") % error)
        return res

    def _get_template_state_change(self):
        self.ensure_one()
        result = False
        obj_state_change_template = self.env["state.change.constrain.template"]
        criteria = [
            ("status_check_template_id", "=", self.status_check_template_id.id),
        ]
        template_ids = obj_state_change_template.search(
            criteria,
            order="sequence desc",
        )
        if template_ids:
            for template_id in template_ids:
                if self._evaluate_state_change(template_id):
                    result = template_id.id
                    break
        return result

    @api.onchange(
        "status_check_template_id",
    )
    def onchange_state_change_constrain_template_id(self):
        self.state_change_constrain_template_id = False
        if self.status_check_template_id:
            template_id = self._get_template_state_change()
            self.state_change_constrain_template_id = template_id

    @api.constrains(
        "state",
    )
    def _check_state_constrain(self):
        for document in self:
            if document.state_change_constrain_template_id:
                detail_ids = document.state_change_constrain_template_id.detail_ids
                check_detail_ids = detail_ids.filtered(
                    lambda r: r.state_id.value == document.state
                )
                if check_detail_ids:
                    status_check_item_ids = check_detail_ids.status_check_item_ids
                    status_check_ids = document.status_check_ids
                    for detail in status_check_item_ids:
                        status_check = status_check_ids.filtered(
                            lambda r: r.status_check_item_id.id == detail.id
                        )
                        if not status_check.status_ok:
                            item = status_check.status_check_item_id.name
                            state_name = dict(self._fields["state"].selection).get(
                                document.state
                            )
                            error_message = """
                            Document Type: %s
                            Context: Change document state into %s
                            Database ID: %s
                            Problem: Status check %s failed
                            Solution: Follow check status resolution instruction
                            """ % (
                                self._description,
                                state_name,
                                document.id,
                                item,
                            )
                            raise UserError(error_message)

    @api.model
    def create(self, values):
        _super = super(MixinStateChangeConstrain, self)
        result = _super.create(values)
        if not result.state_change_constrain_template_id:
            template_id = result._get_template_state_change()
            if template_id:
                result.write({"state_change_constrain_template_id": template_id})
        return result
