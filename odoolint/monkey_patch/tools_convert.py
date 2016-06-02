# -*- coding: utf-8 -*-
# © 2016  Vauxoo (<http://www.vauxoo.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import sys

import openerp


convert_file_original = openerp.tools.convert.convert_file
# print "pase por aqui", "-" * 100
def convert_file_patch(*args, **kwargs):
    print "por aqui no he pasado", "+" * 1000
    import pdb;pdb.set_trace()
    return convert_file_original(*args, **kwargs)
openerp.tools.convert.convert_file = convert_file_patch
sys.modules['openerp.tools.convert'].convert_file = convert_file_patch
sys.modules['openerp.tools.convert.convert_file'] = convert_file_patch

print "\n\n\nya parche\n\n\n"
# print "openerp.tools.convert.convert_file", openerp.tools.convert.convert_file
# print "convert_file_original", convert_file_original
# print "convert_file_patch", convert_file_patch

# from openerp.tools.convert import convert_file
# # import pdb;pdb.set_trace()
# print "convert_file", convert_file


