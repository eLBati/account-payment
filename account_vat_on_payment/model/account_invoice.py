# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-2012 Domsense s.r.l. (<http://www.domsense.com>).
#    Copyright (C) 2014 Agile Business Group sagl (<http://www.agilebg.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
from openerp.exceptions import Warning


class AccountInvoice(models.Model):

    def _get_vat_on_payment(self):
        return self.env.user.company_id.vat_on_payment

    @api.multi
    def onchange_partner_id(
            self, type, partner_id, date_invoice=False,
            payment_term=False, partner_bank_id=False, company_id=False
    ):
        res = super(AccountInvoice, self).onchange_partner_id(
            type, partner_id, date_invoice, payment_term, partner_bank_id,
            company_id)
        # default value for VAT on Payment is changed every time the
        # customer/supplier is changed
        if partner_id:
            p = self.env['res.partner'].browse(partner_id)
            p.with_context(self.env['res.users'].context_get())
            if p.property_account_position:
                res['value'][
                    'vat_on_payment'
                ] = p.property_account_position.default_has_vat_on_payment
        return res

    _inherit = "account.invoice"

    vat_on_payment = fields.Boolean(
        string='Vat on payment', default=_get_vat_on_payment),
