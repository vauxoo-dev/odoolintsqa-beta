# -*- coding: utf-8 -*-
# © 2016  Vauxoo (<http://www.vauxoo.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os

from openerp.modules.module import get_module_resource
from openerp.tests.common import TransactionCase

from getaddons import get_modules, is_module


class OdooLint(TransactionCase):

    def test_wrong_xml_ids(self):
        module_paths = os.environ.get('TRAVIS_BUILD_DIR', '').split(",") + \
            os.environ.get('TEST_OTHER_PROJECTS', '').split(",")
        modules = []
        for module_path in module_paths:
            modules.extend(get_modules(module_path))
        xml_ids = self.get_db_xml_ids(modules)

    def get_db_xml_ids(self, modules=None):
        """Search all xml ids and identify the category from manifest file
        :params modules list: List of string with modules to filter.
            None for all modules.
        :return list: ['module1.xml_id1', 'module2.xml_id2', ...]
        """
        domain = [('module', 'in', modules)] if modules else []
        return [
            xml_record.module + '.' + xml_record.name
            for xml_record in self.env['ir.model.data'].search(domain)]

    def get_xml_ids_group_by_section(self, xml_ids):
        """Create a dictionary with section from manifest and xml_ids
        :params xml_ids list: List of string with xml_ids names module.xml_id
        :return dict: {'manifest_section': [xml_id1, xml_id2, ...]}
        """
        for module_xml_id in xml_ids:
            module, xml_id = module_xml_id.split('.')
            module_path = get_module_resource(module)
            manifest_path = self.is_module(module_path)
            xml_id_section = self.get_xml_id_section(manifest_path, xml_id)
        return xml_id_section

    def get_xml_id_section(self, manifest_path, xml_id):
        module_dirname = os.path.dirname(manifest_path)
        sections = ['data', 'test', 'demo']
        manif_dict = eval(open(manifest_path).read())
        for root, _, filenames in os.walk(module_dirname, followlinks=True):
            for filename in filenames:
                fname = os.path.join(root, filename)
                fname_r = os.path.relpath(fname, module_dirname)
                if xml_id in open(fname).read():
                    for section in sections:
                        if fname_r in manif_dict.get(section, []):
                            return section
