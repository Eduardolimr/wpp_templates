# Copyright 2022, TODAY Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models

class WppPartner(models.Model):
    _name = 'wpp.base'
    
    message = fields.Text(string="Message", required=True)
    phone = fields.Char(string="Mobile Number", required=True)
    
    def wpp_parse_message(self):
        if not phone[0] == "+":
            view = self.env.ref('wpp.message_wizard')
            view_id = view and view.id or False
            context = dict(self._context or {})
            context['message'] = "Please add a valid mobile number with the Country Code! (Including the '+')"
            return {
                'name': 'Missing Country Code',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'display.error.message',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': context,
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': _('Whatsapp Message'),
                'res_model': 'wpp.wizard',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {
                    'default_template_id': self.env.ref('wpp.wpp_template').id},
            }