# -*- coding: utf-8 -*-
# © 2016  Vauxoo (<http://www.vauxoo.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os
import logging

from openerp import api, fields, models, tools
from openerp.addons.odoolint.hooks import get_file_info
from openerp.modules.module import get_module_resource

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

    @api.multi
    def _check_data_ref_demo(self):
        """Check data where a xml_id of section demo or test is referenced
        """
        self.ensure_one()
        imd_new = get_file_info()
        if self.section in ['demo', 'demo_xml', 'test'] and \
                imd_new.get('section') in ['data', 'init', 'update']:
            _logger.warning(
                "Demo xml_id '%s' of '%s/%s' is referenced "
                "from data xml '%s/%s'",
                self.name, self.module_real, self.file_name,
                imd_new['module_real'], imd_new['file_name'],
            )
            return False
        return True

    @api.multi
    def _get_module_upstream_dependencies(self, module_ids, known_dep_ids=None,
        exclude_states=['installed', 'uninstallable', 'to remove'],
        context=None):
        # noqa
        """Copied from odoo native ir.module.module v9.0
        Return the dependency tree of modules of the given `ids`, and that
        satisfy the `exclude_states` filter """
        # TODO: Move a ir_module_module.py
        ids = module_ids
        cr = self.env.cr
        if not ids:
            return []
        known_dep_ids = set(known_dep_ids or [])
        cr.execute('''SELECT DISTINCT m.id
                        FROM
                            ir_module_module_dependency d
                        JOIN
                            ir_module_module m ON (d.module_id=m.id)
                        WHERE
                            m.name IN (SELECT name from ir_module_module_dependency where module_id in %s) AND
                            m.state NOT IN %s AND
                            m.id NOT IN %s ''',
                   (tuple(ids), tuple(exclude_states), tuple(known_dep_ids or ids)))
        new_dep_ids = set([m[0] for m in cr.fetchall()])
        missing_mod_ids = new_dep_ids - known_dep_ids
        known_dep_ids |= new_dep_ids
        if missing_mod_ids:
            known_dep_ids |= set(self._get_module_upstream_dependencies(list(missing_mod_ids),
                                                              known_dep_ids, exclude_states, context))
        return list(known_dep_ids)

    @api.multi
    def _check_xml_id_unachievable(self, xmlid):
        """Check a unachievable xml_id referenced
        """
        self.ensure_one()
        module = self.env['ir.module.module']
        imd_new = get_file_info()
        module_curr_str = imd_new.get('module_real')
        module_ref_str = self.module
        if not module_curr_str or not module_ref_str or \
                module_ref_str == module_curr_str:
            return True
        module_curr = module.search([('name', '=', module_curr_str)], limit=1)
        module_curr_dep_ids = self._get_module_upstream_dependencies(
            module_curr.ids, exclude_states=['uninstallable', 'to remove'])
        module_curr_deps = module.browse(module_curr_dep_ids).mapped('name')
        for mod_autinst in module.search([
                ('auto_install', '=', True),
                ('name', 'not in', module_curr_deps)]):
            # TODO: Get recursively the auto_install of auto_install modules
            mod_autinst_deps = mod_autinst.dependencies_id.mapped('name')
            if not mod_autinst_deps or \
                    set(mod_autinst_deps).issubset(set(module_curr_deps)):
                module_curr_deps.append(mod_autinst.name)

        if module_curr_deps and module_ref_str not in module_curr_deps:
            file_path = os.path.join(
                get_module_resource(imd_new['module_real']),
                imd_new['file_name'])
            # TODO: Use a cache of file content
            file_content = open(file_path).read()
            # TODO: Validate all xmlid cases, e.g. model_ in csv
            if xmlid in file_content:
                # Many times a ref id is used from a default or inherit method
                # If the xml_id is in the content of the file, then is a real
                _logger.warning("The xml_id '%s.%s' is unachievable.",
                                module_ref_str, self.name)
                return False
        return True

    @tools.ormcache(skiparg=3)
    def xmlid_lookup(self, cr, uid, xmlid):
        res = super(IrModelData, self).xmlid_lookup(cr, uid, xmlid)
        self._check_data_ref_demo(cr, uid, res[0])
        self._check_xml_id_unachievable(cr, uid, res[0], xmlid)
        return res
