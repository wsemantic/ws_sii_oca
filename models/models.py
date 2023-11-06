# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class wsem_sii_oca(models.Model):
#     _name = 'wsem_sii_oca.wsem_sii_oca'
#     _description = 'wsem_sii_oca.wsem_sii_oca'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_sii_identifier(self):
        gen_type = self._get_sii_gen_type()
        (
            country_code,
            identifier_type,
            identifier,
        ) = self._sii_get_partner()._parse_aeat_vat_info()
        if identifier:
            identifier = "".join(e for e in identifier if e.isalnum()).upper()
        else:
            identifier = "NO_DISPONIBLE"
            identifier_type = "06"

        # Comprobación para el caso de país europeo pero fiscal position "Nacional"
        if gen_type == 1 and self.fiscal_position_id.name=="Régimen Nacional" and country_code!='ES' and "1117" not in (self.sii_send_error or ""):        
            return {
                    "IDOtro": {
                        "CodigoPais": country_code,
                        "IDType": "04",
                        "ID": country_code + identifier
                        if self.commercial_partner_id._map_aeat_country_code(
                            country_code
                        )
                        in self.commercial_partner_id._get_aeat_europe_codes()
                        else identifier,
                    },
                }

        # Si no cumple la condición anterior, se llama al comportamiento original
        return super()._get_sii_identifier()