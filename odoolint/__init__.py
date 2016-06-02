# -*- coding: utf-8 -*-
# © 2016  Vauxoo (<http://www.vauxoo.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import imp
import logging

from openerp import tools

from . import models

_logger = logging.getLogger(__name__)


def patch_openerp():
    orig_convert_file = tools.convert.convert_file

    def convert_file(*args, **kwargs):
        import pdb;pdb.set_trace()
        return orig_convert_file(*args, **kwargs)
    tools.convert.convert_file = convert_file
    imp.reload(tools)


def post_load():
    _logger.warning(
        'Post load patching openerp.tools.convert.convert_file method')
    patch_openerp()
