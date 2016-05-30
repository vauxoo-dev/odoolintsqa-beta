# -*- coding: utf-8 -*-
# © 2016  Vauxoo (<http://www.vauxoo.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models

class IrModelData(models.Model):
    _inherit = "ir.model.data"

    @api.model
    def create(self, values):
        import pdb;pdb.set_trace()
        print values
        return super(IrModelData, self).create(values)
