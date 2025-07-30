# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import base64
import re
import ssl

from math import ceil

import requests

from trytond.config import config
from trytond.exceptions import UserError
from trytond.i18n import gettext
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.wizard import StateAction, StateTransition, Wizard

SERVER_URLS = {
    'testing': 'https://api-sandbox.dhl.com/parcel/de/shipping/v2/orders',
    'production': 'https://api-eu.dhl.com/parcel/de/shipping/v2/orders',
    'tracking': 'https://www.dhl.de/de/privatkunden/pakete-empfangen/verfolgen.html?piececode=',
    }


class ShipmentOut(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out'

    def validate_packing_dhl_de(self):
        warehouse_address = self.warehouse.address
        if not warehouse_address:
            raise UserError(gettext(
                    'stock_package_shipping_dhl_de.warehouse_address_required',
                    warehouse=self.warehouse.rec_name))


class Package(metaclass=PoolMeta):
    __name__ = 'stock.package'

    def get_shipping_tracking_url(self, name):
        url = super().get_shipping_tracking_url(name)
        if (self.shipping_reference
                and self.shipment
                and self.shipment.id >= 0
                and self.shipment.carrier
                and self.shipment.carrier.shipping_service == 'dhl_de'):
            url = ''.join([SERVER_URLS['tracking'], self.shipping_reference])
        return url


class CreateShipping(metaclass=PoolMeta):
    __name__ = 'stock.shipment.create_shipping'

    dhl_de = StateAction(
        'stock_package_shipping_dhl_de.act_create_shipping_dhl_de_wizard')

    def transition_start(self):
        pool = Pool()
        ShipmentOut = pool.get('stock.shipment.out')

        shipment = ShipmentOut(Transaction().context['active_id'])
        next_state = super().transition_start()
        if shipment.carrier.shipping_service == 'dhl_de':
            next_state = 'dhl_de'
        return next_state

    def do_dhl_de(self, action):
        ctx = Transaction().context
        return action, {
            'model': ctx['active_model'],
            'id': ctx['active_id'],
            'ids': [ctx['active_id']],
            }


class CreateShippingDHL(Wizard):
    'Create DHL Shipping'
    __name__ = 'stock.shipment.create_shipping.dhl_de'

    start = StateTransition()

    def transition_start(self):
        pool = Pool()
        ShipmentOut = pool.get('stock.shipment.out')
        Package = pool.get('stock.package')

        shipment = ShipmentOut(Transaction().context['active_id'])
        if shipment.reference:
            raise UserError(gettext(
                    'stock_package_shipping_dhl_de.has_reference_number',
                    shipment=shipment.rec_name))

        credential = self.get_credential(shipment)
        api_url = config.get('stock_package_shipping_dhl_de',
            credential.server, default=SERVER_URLS[credential.server])
        headers = self.get_request_header(credential)
        auth = self.get_authorization(credential)
        packages = [p for p in shipment.root_packages
            if not p.shipping_reference]
        shipment_request = self.get_request(shipment, packages, credential)

        nb_tries, response = 0, None
        error_message = ''
        try:
            while nb_tries < 5 and response is None:
                try:
                    req = requests.post(api_url, headers=headers,
                        json=shipment_request, auth=auth)
                except ssl.SSLError as e:
                    error_message = e.message
                    nb_tries += 1
                    continue
                req.raise_for_status()
                response = req.json()
        except requests.HTTPError as e:
            msg = req.json()
            if msg.get('items'):
                description = msg['items'][0]
            elif msg.get('detail'):
                description = msg['detail']
            else:
                description = msg
            error_message = str(description)

        if error_message:
            raise UserError(gettext(
                    'stock_package_shipping_dhl_de.dhl_de_webservice_error',
                    message=error_message))

        dhl_packages = response['items']

        for tryton_pkg, dhl_pkg in zip(packages, dhl_packages):
            tryton_pkg.shipping_reference = dhl_pkg['shipmentNo']
            tryton_pkg.shipping_label = fields.Binary.cast(base64.b64decode(
                    dhl_pkg['label']['b64']))
            if hasattr(tryton_pkg, 'label_file_name'):
                tryton_pkg.label_file_name = dhl_pkg['routingCode'] + '.pdf'
        Package.save(packages)
        shipment.save()
        return 'end'

    def get_credential_pattern(self, shipment):
        return {
            'company': shipment.company.id,
            'server': shipment.carrier.dhl_server,
            }

    def get_credential(self, shipment):
        pool = Pool()
        DHLCredential = pool.get('carrier.credential.dhl_de')

        credential_pattern = self.get_credential_pattern(shipment)
        for credential in DHLCredential.search([]):
            if credential.match(credential_pattern):
                return credential
        raise UserError(gettext(
                'stock_package_shipping_dhl_de.missing_configuration',
                company=shipment.company.rec_name))

    def get_authorization(self, credential):
        if credential.server == 'testing':
            dhl_user = 'user-valid'
            password = 'SandboxPasswort2023!'
        else:
            dhl_user = f'{credential.dhl_user}'
            password = f'{credential.password}'
        return (dhl_user, password)

    def get_request_header(self, credential):
        return {
            'Accept-Language': 'de-DE',
            'Content-type': 'application/json',
            'DHL-API-Key': f'{credential.api_key}',
            }

    def get_request_address(self, party, address):
        assert party == address.party

        def format_field(field, length):
            res = ''
            # address.subdivison returns the record instead of rec_name
            if field:
                if not isinstance(field, str):
                    res = field.rec_name[0:length]
                else:
                    res = field[0:length]
            return res

        def split_street_and_number(address):
            """
            Separates address into street and house number.
            Works with german and austrian addresses.
            Example:
            "Musterstraße 12a" → ("Musterstraße", "12a")
            "Am Hang 5" → ("Am Hang", "5")
            "Hauptstr. 99b/1" → ("Hauptstr.", "99b/1")
            """
            pattern = r'^(.*?)[\s,]+(\d+\w*(?:\/\d+)?)$'
            match = re.match(pattern, address.strip())
            if match:
                return match.group(1), match.group(2)
            return address, ''

        # We assume street and number in first line, in subsequent lines
        # anything else
        # address.party_name == Zustellzusatz, instead of party.name
        # address.name == Building
        street_lines = address.street.splitlines()
        street_house = split_street_and_number(street_lines.pop(0))
        add_info = ' '.join(street_lines)
        delivery_address = {
            'name1': format_field(address.party_full_name, 40),
            'addressStreet': street_house[0],
            'addressHouse': street_house[1],
            'country': address.country.code3 if address.country else 'DEU',
            'postalCode': format_field(address.postal_code, 10),
            'city': format_field(address.city, 40),
            #'state': format_field(address.subdivision, 40),
            }
        if address.name:
            delivery_address['additionalAddressInformation1'] = format_field(
                address.name, 60)
        if add_info:
            delivery_address['additionalAddressInformation2'] = format_field(
                add_info, 60)

        phone = ''
        mobile = ''
        email = ''
        for mechanism in party.contact_mechanisms:
            if mechanism.type == 'phone':
                phone = mechanism.value
            elif mechanism.type == 'mobile':
                mobile = mechanism.value
            elif mechanism.type == 'email':
                email = mechanism.value
        if phone:
            delivery_address['phone'] = phone
        if mobile and not phone:
            delivery_address['mobile'] = mobile
        if email:
            delivery_address['email'] = email
        return delivery_address

    def get_package(self, package, shipment):
        pool = Pool()
        UoM = pool.get('product.uom')
        ModelData = pool.get('ir.model.data')

        cm = UoM(ModelData.get_id('product', 'uom_centimeter'))

        weight = ceil(package.total_weight)
        if weight < 1:
            weight = 1

        res = {
            'weight': {
                'uom': 'kg',
                'value': weight,
                },
            'dim': {
                'uom': 'cm',
                'length': ceil(
                    UoM.compute_qty(
                        package.length_uom, package.length, cm, round=False)),
                'height': ceil(
                    UoM.compute_qty(
                        package.height_uom, package.height, cm, round=False)),
                'width': ceil(
                    UoM.compute_qty(
                        package.width_uom, package.width, cm, round=False)),
                },
            }
        return res

    def get_request(self, shipment, packages, credential):
        pool = Pool()
        Date = pool.get('ir.date')
        today = Date.today()

        shipper_address = self.get_request_address(shipment.company.party,
            shipment.warehouse.address)
        delivery_address = self.get_request_address(shipment.customer,
            shipment.delivery_address)
        packages = [self.get_package(p, shipment) for p in packages]

        return {
            'profile': 'STANDARD_GRUPPENPROFIL',
            'shipments': [
                {
                    'summary': 'DHL Paket (V01PAK)',
                    'description': shipment.shipping_description,
                    'product': shipment.carrier.dhl_service_type,
                    'billingNumber': (shipment.carrier.dhl_billing_number
                        if credential.server == 'production'
                        else '33333333330101'),
                    'refNo': f'Shipment No. {shipment.number}',
                    # 'costCenter': ''
                    'creationSoftware': 'MBSolutions Shipping DHL DE',
                    'shipDate': str(today),
                    'shipper': shipper_address,
                    'consignee': delivery_address,
                    'details': packages[0],
                    'docFormat': shipment.carrier.dhl_label_image_format,
                    'printFormat': shipment.carrier.dhl_label_size,
                    }
                ]
            }
