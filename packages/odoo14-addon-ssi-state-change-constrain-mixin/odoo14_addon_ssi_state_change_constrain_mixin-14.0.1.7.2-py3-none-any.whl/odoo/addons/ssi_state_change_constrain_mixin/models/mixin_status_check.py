# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import models


class MixinStatusCheck(models.AbstractModel):
    _inherit = "mixin.status_check"

    def action_reload_status_check_template(self):
        _super = super(MixinStatusCheck, self)
        _super.action_reload_status_check_template()
        for record in self:
            record.onchange_state_change_constrain_template_id()
