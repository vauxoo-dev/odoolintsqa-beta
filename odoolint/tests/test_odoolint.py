# -*- coding: utf-8 -*-
# © 2016  Vauxoo (<http://www.vauxoo.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# import os

# from openerp.modules.module import get_module_resource
from openerp.tests.common import TransactionCase, at_install, post_install

SQL_FOREIGN_RELATIONS = """
SELECT cl1.relname as table_rel,
       att1.attname as column_rel
FROM pg_constraint as con, pg_class as cl1,
     pg_class as cl2, pg_attribute as att1,
     pg_attribute as att2
WHERE con.conrelid = cl1.oid
     AND con.confrelid = cl2.oid
     AND array_lower(con.conkey, 1) = 1
     AND con.conkey[1] = att1.attnum
     AND att1.attrelid = cl1.oid
     AND cl2.relname = %s
     AND att2.attname = 'id'
     AND array_lower(con.confkey, 1) = 1
     AND con.confkey[1] = att2.attnum
     AND att2.attrelid = cl2.oid
     AND con.contype = 'f';
"""


@at_install(False)
@post_install(True)
class OdooLint(TransactionCase):
    def setUp(self):
        super(OdooLint, self).setUp()
        self.model_data = self.env['ir.model.data']
        print "hola mundo"

    def get_model(self, table_name):
        """Get model name of a table name"""
        return self.model_data.search(
            [('table_name', '=', table_name)], limit=1).model

    def test_xml_demo_used_in_data(self):
        # TODO: Consider ir_property case.
        demo_used_in_data = []
        for record in self.model_data.search([('table_name', '!=', False)]):
            self.env.cr.execute(SQL_FOREIGN_RELATIONS, (record.table_name,))
            for table_foreign, column_foreign in self.env.cr.fetchall():
                # Get foreign.xml_id.section and record.xml_id.section
                foreing_model = self.get_model(table_foreign)
                if not foreing_model:
                    # 'base' module case where import data before of the patch
                    continue
                foreing_xml_ids = self.env[foreing_model].search([(
                    column_foreign, '=', record.res_id)])._get_external_ids()
                for foreing_xml_id in foreing_xml_ids.values():
                    if not foreing_xml_id:
                        # foreign without xml_id
                        continue
                    foreing_model_data_id, _, _ = \
                        self.model_data.xmlid_lookup(foreing_xml_id[0])
                    foreing_model_data = \
                        self.model_data.browse(foreing_model_data_id)
                    if record.section != foreing_model_data.section:
                        demo_used_in_data.append((record, foreing_model_data))
        self.assertFalse(demo_used_in_data)

    # def test_wrong_xml_ids(self):
    #     # TODO: Deprecated?
    #     module_paths = os.environ.get('TRAVIS_BUILD_DIR', '').split(",") + \
    #         os.environ.get('TEST_OTHER_PROJECTS', '').split(",")
    #     modules = []
    #     for module_path in module_paths:
    #         modules.extend(get_modules(module_path))
    #     xml_ids = self.get_db_xml_ids(modules)

    # def get_db_xml_ids(self, modules=None):
    #     # TODO: Deprecated?
    #     """Search all xml ids and identify the category from manifest file
    #     :params modules list: List of string with modules to filter.
    #         None for all modules.
    #     :return list: ['module1.xml_id1', 'module2.xml_id2', ...]
    #     """
    #     domain = [('module', 'in', modules)] if modules else []
    #     module_xml_ids_list = [
    #         xml_record.module + '.' + xml_record.name
    #         for xml_record in self.env['ir.model.data'].search(domain)]
    #     return module_xml_ids_list
    #     # for module, xml_id in [
    #     #     do

    # def get_xml_ids_group_by_section(self, xml_ids):
    #     # TODO: Deprecated?
    #     """Create a dictionary with section from manifest and xml_ids
    #     :params xml_ids list: List of string with xml_ids names module.xml_id
    #     :return dict: {'manifest_section': [xml_id1, xml_id2, ...]}
    #     """
    #     for module_xml_id in xml_ids:
    #         module, xml_id = module_xml_id.split('.')
    #         module_path = get_module_resource(module)
    #         manifest_path = is_module(module_path)
    #         xml_id_section = self.get_xml_id_section(manifest_path, xml_id)
    #     return xml_id_section

    # def get_xml_id_section(self, manifest_path, xml_id):
    #     # TODO: Deprecated?
    #     module_dirname = os.path.dirname(manifest_path)
    #     sections = ['data', 'test', 'demo']
    #     manif_dict = eval(open(manifest_path).read())
    #     for root, _, filenames in os.walk(module_dirname, followlinks=True):
    #         for filename in filenames:
    #             fname = os.path.join(root, filename)
    #             fname_r = os.path.relpath(fname, module_dirname)
    #             if xml_id in open(fname).read():
    #                 for section in sections:
    #                     if fname_r in manif_dict.get(section, []):
    #                         return section
