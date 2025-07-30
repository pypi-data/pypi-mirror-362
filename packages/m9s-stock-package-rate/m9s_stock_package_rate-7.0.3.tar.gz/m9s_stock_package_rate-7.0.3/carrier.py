# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from decimal import Decimal

from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction


class Carrier(metaclass=PoolMeta):
    __name__ = 'carrier'

    package_types = fields.Many2Many("carrier.carrier-stock.package.type",
        "carrier", "package_type", "Package Types")

    def get_sale_price(self):
        """
        Returns sale price for a carrier in following format:
            price, currency_id

        You can ignore the computation by passing `skip_carrier_computation`
        variable in context, in that case it will always return sale price as
        zero.

        :Example:

        >>> with Transaction().set_context(skip_carrier_computation=True):
        ...   sale.get_sale_price()
        Decimal('0'), 1
        """
        Company = Pool().get('company.company')

        context = Transaction().context
        if context.get('skip_carrier_computation'):
            company = Company(context.get('company'))
            return Decimal('0'), company.currency.id
        return super(Carrier, self).get_sale_price()


class CarrierPackageType(ModelSQL):
    "Carrier - Package Type"
    __name__ = "carrier.carrier-stock.package.type"

    carrier = fields.Many2One("carrier", "Carrier", ondelete="CASCADE",
        required=True)
    package_type = fields.Many2One("stock.package.type", "Package Type",
        ondelete="CASCADE", required=True)


class SaleChannelCarrier(ModelSQL, ModelView):
    """
    Shipping Carriers

    This model stores the carriers, each record
    here can be mapped to a carrier in tryton which will then be
    used for managing export of tracking info.
    """
    __name__ = 'sale.channel.carrier'

    name = fields.Char('Name')
    code = fields.Char("Code")
    carrier = fields.Many2One('carrier', 'Carrier')
    channel = fields.Many2One('sale.channel', 'Channel', readonly=True)
