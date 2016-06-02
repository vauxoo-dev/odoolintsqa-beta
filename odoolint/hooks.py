# -*- coding: utf-8 -*-
# © 2016  Vauxoo (<http://www.vauxoo.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import imp
import logging

from openerp import tools

_logger = logging.getLogger(__name__)


def monkey_patch_convert_file():
    """Monkey patch to openerp.tools.convert.convert_file method to add custom
    information for importation process.
    """
    convert_file_original = tools.convert.convert_file

    def convert_file(*args, **kwargs):
        import pdb;pdb.set_trace()
        return convert_file_original(*args, **kwargs)
    tools.convert.convert_file = convert_file
    # Reload sys.modules to propagate patch
    imp.reload(tools)


def post_load():
    _logger.info(
        'Patching openerp.tools.convert.convert_file method')
    monkey_patch_convert_file()
