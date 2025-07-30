# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool

from . import carrier, stock

__all__ = ['register']


def register():
    Pool.register(
        stock.Package,
        stock.ShipmentOut,
        carrier.CredentialDHL,
        carrier.Carrier,
        module='stock_package_shipping_dhl_de', type_='model')
    Pool.register(
        stock.CreateShipping,
        stock.CreateShippingDHL,
        module='stock_package_shipping_dhl_de', type_='wizard')
