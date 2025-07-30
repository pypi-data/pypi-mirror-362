# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.transaction import Transaction


class Package(metaclass=PoolMeta):
    __name__ = 'stock.package'

    available_package_types = fields.Function(
        fields.One2Many("stock.package.type", None, "Available Package Types"),
        "on_change_with_available_package_types",
        setter="set_available_package_types")

    @classmethod
    def __setup__(cls):
        super().__setup__()
        type_domain = ('id', 'in', Eval('available_package_types'))
        if type_domain not in cls.type.domain:
            cls.type.domain.append(type_domain)

    @fields.depends('shipment')
    def on_change_with_available_package_types(self, name=None):
        pool = Pool()
        Carrier = pool.get('carrier')
        PackageType = pool.get('stock.package.type')

        carrier = None
        if self.shipment:
            carrier = self.shipment.carrier
        elif Transaction().context.get('carrier'):
            carrier = Carrier(Transaction().context.get('carrier'))

        if carrier is not None:
            return list(map(int, carrier.package_types))
        else:
            return list(map(int, PackageType.search([])))

    @classmethod
    def set_available_package_types(cls, packages, name, value):
        pass


class PackageType(metaclass=PoolMeta):
    __name__ = 'stock.package.type'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.name.translate = True

    @classmethod
    def check_xml_record(cls, records, values):
        return True
