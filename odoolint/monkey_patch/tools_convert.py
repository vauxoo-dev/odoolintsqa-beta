# -*- coding: utf-8 -*-
# © 2016  Vauxoo (<http://www.vauxoo.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tools.convert import convert_file


def convert_file_patch(*args, **kwargs):
    import pdb;pdb.set_trace()
    return convert_file(*args, **kwargs)


covert_file = convert_file_patch
