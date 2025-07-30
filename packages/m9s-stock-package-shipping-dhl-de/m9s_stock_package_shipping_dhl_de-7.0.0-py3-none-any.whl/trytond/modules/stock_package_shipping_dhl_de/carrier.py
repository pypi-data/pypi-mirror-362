# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import MatchMixin, ModelSQL, ModelView, fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval


class CredentialDHL(ModelSQL, ModelView, MatchMixin):
    'DHL Credential'
    __name__ = 'carrier.credential.dhl_de'

    company = fields.Many2One('company.company', 'Company')
    dhl_user = fields.Char('DHL User', required=True)
    password = fields.Char('Password', required=True)
    api_key = fields.Char('API Key', required=True)
    api_secret = fields.Char('API Secret', required=True)
    server = fields.Selection([
            ('testing', 'Testing'),
            ('production', 'Production'),
            ], 'Server')

    @classmethod
    def default_server(cls):
        return 'testing'


class Carrier(metaclass=PoolMeta):
    __name__ = 'carrier'

    _states_dhl_de = {
            'required': Eval('shipping_service') == 'dhl_de',
            'invisible': Eval('shipping_service') != 'dhl_de',
            }

    dhl_server = fields.Selection([
            ('testing', 'Testing'),
            ('production', 'Production'),
            ], 'Server',
        states=_states_dhl_de)
    dhl_service_type = fields.Selection([
            (None, ''),
            ('V01PAK', 'DHL PAKET'),
            ('V53WPAK', 'DHL PAKET International'),
            ('V54EPAK', 'DHL Europaket'),
            ('V62KP', 'DHL Kleinpaket'),
            ('V66WPI', 'Warenpost International'),
            ], 'Service Type', sort=False, translate=False,
        states=_states_dhl_de)
    dhl_billing_number = fields.Char('DHL Billing Number',
        states=_states_dhl_de)
    dhl_label_image_format = fields.Selection([
            (None, ''),
            ('PDF', 'PDF'),
            ('ZPL2', 'ZPL2'),
            ], 'Label Image Format', sort=False, translate=False,
        states=_states_dhl_de)
    dhl_label_size = fields.Selection([
            (None, ''),
            ('A4', 'Common Label Laserdruck A4 Normalpapier'),
            ('910-300-700', 'Common Label Laserdruck (Bogen A5) 105x208mm (910-300-700)'),
            ('910-300-700-oz', 'Common Label Laserdruck (Bogen A5) 105x208mm (910-300-700) ohne Zusatzetiketten'),
            ('910-300-710', 'Common Label Laserdruck 105x209mm (910-300-710)'),
            ('910-300-600', 'Common Label Thermodruck (Faltband) 103x199mm (910-300-600)'),
            ('910-300-610', 'Common Label Thermodruck (Rolle) 103x199mm (910-300-610)'),
            ('910-300-400', 'Common Label Thermodruck (Faltband) 103x150mm (910-300-400)'),
            ('910-300-410', 'Common Label Thermodruck (Rolle) 103x150mm (910-300-410)'),
            ('910-300-300', 'Common Label Laserdruck (Bogen A5) 105x148mm (910-300-300)'),
            ('910-300-300-oz', 'Common Label Laserdruck (Bogen A5) 105x148mm (910-300-300) ohne Zusatzetiketten'),
            ], 'Label Size', sort=False, translate=False,
        states=_states_dhl_de)

    del _states_dhl_de

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.shipping_service.selection.append(('dhl_de', 'DHL DE'))

    @classmethod
    def view_attributes(cls):
        return super().view_attributes() + [
            ("/form/separator[@id='dhl_de']", 'states', {
                    'invisible': Eval('shipping_service') != 'dhl_de',
                    }),
            ]

    @staticmethod
    def default_dhl_service_type():
        return 'V01PAK'

    @staticmethod
    def default_dhl_label_image_format():
        return 'PDF'

    @staticmethod
    def default_dhl_label_size():
        return '910-300-700'
