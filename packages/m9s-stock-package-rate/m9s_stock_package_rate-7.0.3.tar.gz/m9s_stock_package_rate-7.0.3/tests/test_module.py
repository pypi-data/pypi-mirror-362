# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class StockPackageRateTestCase(ModuleTestCase):
    "Test Stock Package Rate module"
    module = 'stock_package_rate'
    extras = ['sale_shipment_cost', 'stock_package_shipping']

del ModuleTestCase
