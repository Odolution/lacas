
from odoo.tests import TransactionCase

from odoo.tests import tagged
from odoo.tests.common import Form


@tagged('post_install', '-at_install')
class TestWallet(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_tuition_plan_creation(self):
        pass