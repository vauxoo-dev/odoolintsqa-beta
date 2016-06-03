# -*- coding: utf-8 -*-
# © 2016  Vauxoo (<http://www.vauxoo.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from openerp import api, fields, models, tools
from openerp.addons.odoolint.hooks import get_file_info

_logger = logging.getLogger(__name__)


class IrModelData(models.Model):
    _inherit = "ir.model.data"

    module_real = fields.Char(
        help="The `module` original field get the value from `module.xml_id`."
        "\nThis `module_real` field get the real module from module/ path."
    )
    section = fields.Char(
        size=8,
        help="Section of file from manifest file. E.g. (data, demo, test, ...)"
    )
    file_name = fields.Char(
        size=32,
        help="Record origin file name")
    table_name = fields.Char(
        size=64,
        help="Table name of database where is stored this record"
    )
    # TODO: Add xml_id computed field store=True

    @api.model
    def create(self, values):
        """Inherit create for add custom values"""
        if values is None:
            values = {}
        new_values = get_file_info()
        model = values.get('model')
        if model:
            new_values['table_name'] = self.env[model]._table
        values.update(new_values)
        return super(IrModelData, self).create(values)

    @tools.ormcache(skiparg=3)
    def xmlid_lookup(self, cr, uid, xmlid):
        res = super(IrModelData, self).xmlid_lookup(cr, uid, xmlid)
        imd_new = get_file_info()
        imd_ref = self.pool['ir.model.data'].browse(cr, uid, res[0])
        if imd_ref.section in ['demo', 'demo_xml', 'test'] and \
                imd_new.get('section') in ['data', 'init', 'update']:
            _logger.warning(
                "Demo xml '%s/%s' id '%s' referenced from data xml '%s/%s'",
                imd_ref.module_real, imd_ref.file_name, imd_ref.name,
                imd_new['module_real'], imd_new['file_name'],
            )
        return res
