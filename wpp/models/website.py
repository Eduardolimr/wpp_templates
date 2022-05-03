# Copyright 2022, TODAY Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

class Website(models.Model):
    _inherit = 'website'

    def _default_social_whatsapp(self):
        return self.env.ref('base.main_company').social_whatsapp

    phone = fields.Char(String='Mobile Number', default=_default_social_whatsapp)
