from odoo import models, fields, api, _
import html2text
import urllib.parse as parse


class WizardContact(models.TransientModel):
    _name = 'wpp.wizard.contact'
    _description = "Wizard for managing contact whatsapp messages"

    partner_id = fields.Many2one('res.partner', string="Recipient Name", default=lambda self: self.env[self._context.get('active_model')].browse(self.env.context.get('active_ids')))
    mobile = fields.Char(related='partner_id.mobile', string="Mobile Number", required=True)
    message = fields.Text(string="Message", required=True)
        
    def send_contact_message(self):
        if self.message:
            self.message.replace(' ', '%20')
            number = self.partner_id.mobile
            link = "https://web.whatsapp.com/send?phone=" + number
            send_msg = {
                'type': 'ir.actions.act_url',
                'url': link + "&text=" + self.message,
                'target': 'new',
                'res_id': self.id,
            }
            return send_msg
