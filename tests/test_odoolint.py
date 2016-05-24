# -*- coding: utf-8 -*-
# © 2016  Vauxoo (<http://www.vauxoo.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os

from openerp.tests.common import TransactionCase

MANIFEST_FILES = ['__openerp__.py', '__terp__.py', '__odoo__.py']


class OdooLint(TransactionCase):

    def get_xml_ids(self, modules=None):
        """Search all xml ids and identify the category from manifest file
        :params modules list: List of string with modules to filter.
            None for all modules.
        :return list: ['module1.xml_id1', 'module2.xml_id2', ...]
        """
        domain = [('module', 'in', modules)] if modules else []
        return [
            xml_record.module + '.' + xml_record.name
            for xml_record in self.env['ir.module.data'].search(domain)]

    def get_manifest_path(self, module):
        """Get the path of a odoo module
        :param module str: Name of module to get path
        :return str: Full path of module
        """
        module_path = None  # TODO: Get module_path
        manifest_path = None
        for fname_manifest in MANIFEST_FILES:
            manifest_path = os.path.join(module_path, fname_manifest)
            if os.path.isfile(manifest_path):
                return manifest_path
        raise "Manifest don't found for module %s" % module

    def get_xml_ids_group_by_section(self, xml_ids):
        """Create a dictionary with section from manifest and xml_ids
        :params xml_ids list: List of string with xml_ids names module.xml_id
        :return dict: {'manifest_section': [xml_id1, xml_id2, ...]}
        """
        for module_xml_id in xml_ids:
            module, xml_id = module_xml_id.split('.')
            manifest_path = self.get_manifest_path(module)
            xml_id_section = self.xml_id_get_section(manifest_path, xml_id)
        return xml_id_section

    def test_default_company(self):
        xml_ids = self.get_xml_ids()
        xml_ids_grp = self.get_xml_ids_group_by_section(xml_ids)
        return xml_ids_grp
