# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool

from . import carrier, package, sale, shipment

__all__ = ['register']


def register():
    Pool.register(
        carrier.Carrier,
        carrier.CarrierPackageType,
        package.Package,
        package.PackageType,
        sale.Sale,
        sale.SaleLine,
        sale.ApplyShippingStart,
        sale.ApplyShippingSelectRate,
        shipment.ShipmentOut,
        shipment.ShipmentInReturn,
        module='stock_package_rate', type_='model')
    Pool.register(
        sale.ReturnSale,
        sale.ApplyShipping,
        shipment.GetRate,
        module='stock_package_rate', type_='wizard')
