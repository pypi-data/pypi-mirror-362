# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import ModelView, fields
#from trytond.modules.product import price_digits
from trytond.modules.stock_package.stock import PackageMixin
from trytond.pool import Pool
from trytond.pyson import Eval
from trytond.transaction import Transaction


class ShipmentCarrierMixin(PackageMixin):
    __slots__ = ()
    """
    Mixin class which implements all the fields and methods required for
    getting shipping rates and generating labels
    """
    shipping_instructions = fields.Text(
        'Shipping Instructions', states={
            'readonly': Eval('state').in_(['cancel', 'done']),
        })

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.packages.context.update({'carrier': Eval('carrier')})
        cls._buttons.update({
                'get_rate': {
                    'readonly': (~Eval('root_packages', False)
                        | ~Eval('carrier', False)
                        | ~Eval('state').in_(['packed', 'done'])),
                    },
                })
        # Following fields are already there in customer shipment
        # (verbatim copy from sale_shipment_cost), have them in mixin
        # so other shipment model can also use them.
        #cls.carrier = fields.Many2One('carrier', 'Carrier', states={
        #        'readonly': ~Eval('state').in_(['draft', 'waiting', 'assigned',
        #                'picked', 'packed']),
        #        })
        #cls.cost = fields.Numeric(
        #    "Cost", digits=price_digits,
        #    states={
        #        'invisible': ~Eval('carrier') | ~Eval('cost_edit', False),
        #        'readonly': ~Eval('state').in_(
        #            ['draft', 'waiting', 'assigned', 'picked', 'packed']),
        #        })
        #cls.cost_currency = fields.Many2One('currency.currency',
        #    'Cost Currency', states={
        #        'invisible': ~Eval('carrier'),
        #        'required': Bool(Eval('carrier')),
        #        'readonly': ~Eval('state').in_(['draft', 'waiting', 'assigned',
        #                'packed']),
        #        })

    @property
    def carrier_cost_moves(self):
        "Moves to use for carrier cost calculation"
        return []

    @classmethod
    @ModelView.button_action(
        'stock_package_rate.act_get_rate_wizard')
    def get_rate(cls, shipments):
        pass

    def _create_default_package(self, package_type=None):
        """
        Create a single stock package for the whole shipment
        """
        pool = Pool()
        Package = pool.get('stock.package')
        ModelData = pool.get('ir.model.data')

        values = {
            'shipment': '%s,%d' % (self.__name__, self.id),
            'moves': [('add', self.carrier_cost_moves)],
            }
        if package_type is not None:
            values['type'] = package_type.id
            values['height_uom'] = package_type.height_uom
            values['height'] = package_type.height
            values['length_uom'] = package_type.length_uom
            values['length'] = package_type.length
            values['width_uom'] = package_type.width_uom
            values['width'] = package_type.width
            values['packaging_volume_uom'] = package_type.packaging_volume_uom
            values['packaging_volume'] = package_type.packaging_volume
            values['packaging_weight_uom'] = package_type.packaging_weight_uom
            values['packaging_weight'] = package_type.packaging_weight
        else:
            default_type = ModelData.get_id(
                'stock_package_rate', 'shipment_package_type')
            values['type'] = default_type
        package, = Package.create([values])
        return package

    def get_shipping_rates(self, carriers=None):
        """
        Gives a list of rates from carriers provided. If no carriers provided,
        return rates from all the carriers.

        List contains dictionary with following minimum keys:
            [
                {
                    'display_name': Name to display,
                    'cost': cost,
                    'cost_currency': currency.currency active repord,
                    'carrier': carrier active record,
                }..
            ]
        """
        Carrier = Pool().get('carrier')

        if carriers is None:
            carriers = Carrier.search([])

        rates = []
        for carrier in carriers:
            rates.extend(
                self.get_shipping_rate(carrier=carrier))
        return rates

    def get_shipping_rate(self, carrier):
        """
        Gives a list of rates from provided carrier and carrier service.

        List contains dictionary with following minimum keys:
            [
                {
                    'display_name': Name to display,
                    'cost': cost,
                    'cost_currency': currency.currency active repord,
                    'carrier': carrier active record,
                }..
            ]
        """
        Company = Pool().get('company.company')

        if carrier.carrier_cost_method == 'product':
            currency = Company(Transaction().context['company']).currency
            rate_dict = {
                'display_name': carrier.rec_name,
                'cost': carrier.carrier_product.list_price,
                'cost_currency': currency,
                'carrier': carrier,
            }
            return [rate_dict]

        return []

    def apply_shipping_rate(self, rate):
        """
        This method applies shipping rate. Rate is a dictionary with
        following minimum keys:

            {
                'display_name': Name to display,
                'cost': cost,
                'cost_currency': currency.currency active repord,
                'carrier': carrier active record,
            }
        """
        Currency = Pool().get('currency.currency')

        shipment_cost = rate['cost_currency'].round(rate['cost'])
        if self.cost_currency != rate['cost_currency']:
            shipment_cost = Currency.compute(
                rate['cost_currency'], shipment_cost, self.cost_currency
            )

        self.cost = shipment_cost
        self.cost_currency = rate['cost_currency']
        self.carrier = rate['carrier']
        self.save()
