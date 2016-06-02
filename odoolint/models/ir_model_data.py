# -*- coding: utf-8 -*-
# © 2016  Vauxoo (<http://www.vauxoo.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models
from openerp.tools.convert import convert_file

class IrModelData(models.Model):
    _inherit = "ir.model.data"

    @api.model
    def create(self, values):
        # import pdb;pdb.set_trace()
        print "convert_file.func_code", convert_file.func_code
        return super(IrModelData, self).create(values)
