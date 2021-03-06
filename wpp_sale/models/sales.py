from odoo import models, fields, api, _
import urllib.parse as parse
from odoo.exceptions import UserError
from itertools import groupby

class SaleOrderValidation(models.Model):
    _inherit = 'sale.order'

    def sale_wpp(self):
        mobile = self.partner_id.mobile
        if not mobile:
            view = self.env.ref('wpp.wpp_warn_wizard')
            view_id = view and view.id or False
            context = dict(self._context or {})
            context['message'] = "Please add a mobile number!"
            return {
                'name': 'Mobile Number Field Empty',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'display.error.message',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': context
            }
        if not mobile[0] == "+":
            view = self.env.ref('wpp.wpp_warn_wizard')
            view_id = view and view.id or False
            context = dict(self._context or {})
            context['message'] = "No Country Code! Please add a valid mobile number along with country code!"
            return {
                'name': 'Invalid Mobile Number',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'display.error.message',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': context
            }
        else:
            return {'type': 'ir.actions.act_window',
                    'name': _('Whatsapp Message'),
                    'res_model': 'wpp.wizard',
                    'target': 'new',
                    'view_mode': 'form',
                    'view_type': 'form',
                    'context': {
                        'default_template_id': self.env.ref('wpp_sale.wpp_sales_template').id},
                    }

    def send_direct_message(self):
        mobile = self.partner_id.mobile
        if not mobile:
            view = self.env.ref('wpp.wpp_warn_wizard')
            view_id = view and view.id or False
            context = dict(self._context or {})
            context['message'] = "Please add a mobile number!"
            return {
                'name': 'Mobile Number Field Empty',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'display.error.message',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': context
            }
        if not mobile[0] == "+":
            view = self.env.ref('wpp.wpp_warn_wizard')
            view_id = view and view.id or False
            context = dict(self._context or {})
            context['message'] = "No Country Code! Please add a valid mobile number along with country code!"
            return {
                'name': 'Invalid Mobile Number',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'display.error.message',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': context
            }
        else:
            prods = ""
            for rec in self:
                for id in rec.order_line:
                    prods = prods + "*" +str(id.product_id.name) + " : " + str(id.product_uom_qty) + "* \n"

            custom_msg = "Hello *{}*, your Sale Order *{}* with amount *{} {}* is ready. \nYour order contains following items: \n{}".format(str(self.partner_id.name),str(self.name),str(self.currency_id.symbol),str(self.amount_total),prods)
            link = "https://web.whatsapp.com/send?phone=" + mobile
            message_string = parse.quote(custom_msg)

            url_id = link + "&text=" + message_string
            return {
                'type':'ir.actions.act_url',
                'url': url_id,
                'target':'new',
                'res_id': self.id,
            }

    def check_value(self, partner_ids):
        partners = groupby(partner_ids)
        return next(partners, True) and not next(partners, False)

    def multi_sms(self):
        sale_order_ids = self.env['sale.order'].browse(self.env.context.get('active_ids'))

        cust_ids = []
        sale_nums = []
        for sale in sale_order_ids:
            cust_ids.append(sale.partner_id.id)
            sale_nums.append(sale.name)

        # To check unique customers
        cust_check = self.check_value(cust_ids)

        if cust_check:
            sale_numbers = sale_order_ids.mapped('name')
            sale_numbers = "\n".join(sale_numbers)

            form_id = self.env.ref('wpp.wpp_multiple_message_wizard_form').id
            product_all = []
            for each in sale_order_ids:
                prods = ""
                for id in each.order_line:
                    prods = prods + "*" + "Product: "+str(id.product_id.name) + ", Qty: " + str(id.product_uom_qty) + "* \n"
                product_all.append(prods)

            custom_msg = "Hi" + " " + self.partner_id.name + ',' + '\n' + "Your Sale Orders" + '\n' + sale_numbers + \
                         ' ' + '\n' + "are ready for review.\n"
            counter = 0
            for every in product_all:
                custom_msg = custom_msg + "Your order " + "*" + sale_nums[
                    counter] + "*" + " contains following items: \n{}".format(every) + '\n'
                counter += 1

            final_msg = custom_msg + "\nDo not hesitate to contact us if you have any questions."

            ctx = dict(self.env.context)
            ctx.update({
                'default_message': final_msg,
                'default_partner_id': self.partner_id.id,
                'default_mobile': self.partner_id.mobile,
            })
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'wpp.wizard.multiple.contact',
                'views': [(form_id, 'form')],
                'view_id': form_id,
                'target': 'new',
                'context': ctx,
            }
        else:
            raise UserError(_('Please Select Orders of Unique Customers'))