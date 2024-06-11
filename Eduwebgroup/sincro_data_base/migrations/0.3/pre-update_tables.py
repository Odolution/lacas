# -*- coding: utf-8 -*-

def migrate(cr, version):
    cr.execute("DELETE FROM ir_model WHERE model='sincro_data_base.telegram_bot'")
    cr.execute("DELETE FROM sincro_data_base_server WHERE api_id IS NULL")
