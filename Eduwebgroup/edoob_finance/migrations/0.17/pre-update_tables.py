# -*- coding: utf-8 -*-

from odoo import _
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    versions = version.split('.')
    try:
        if versions[2] == '0' and int(versions[3]) >= 12:
            cr.execute("UPDATE tuition_plan SET pricelist_option = 'fixed_pricelist' WHERE pricelist_option = 'fixed'")
            cr.execute("UPDATE tuition_template SET pricelist_option = 'fixed_pricelist' WHERE pricelist_option = 'fixed'")
    except Exception as e:
        _logger.warning(_("Error during edoob_finance update fixed_pricelist name"))
        _logger.error(e)
