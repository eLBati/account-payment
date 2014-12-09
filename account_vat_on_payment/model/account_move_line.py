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

from openerp import models, fields, _
from openerp.exceptions import except_orm


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    vat_on_payment_move_id = fields.Many2one(
        'account.move', string='VAT on payment entry'),

    def reconcile_partial(
        self, cr, uid, ids, type='auto', context=None, writeoff_acc_id=False,
        writeoff_period_id=False, writeoff_journal_id=False
    ):
        res = super(AccountMoveLine, self).reconcile_partial(
            cr, uid, ids, type=type, context=context,
            writeoff_acc_id=writeoff_acc_id,
            writeoff_period_id=writeoff_period_id,
            writeoff_journal_id=writeoff_journal_id)
        if context is None:
            context = {}
        if (
            'cash_basis_values' in context
            and 'cash_basis_payment_type' in context
        ):
            # cash_basis_values is in the form
            # {invoice_id: allocated_amount}
            # cash_basis_payment_type can be 'receivable' or 'payable'
            cash_basis_values = context['cash_basis_values']
            for move_line in self.browse(cr, uid, ids, context=context):
                if move_line.invoice:
                    invoice = move_line.invoice
                    if invoice.id not in cash_basis_values:
                        raise except_orm(
                            _('Error'),
                            _('Reconciling invoice %s, but it is not present '
                              'in cash_basis_values') % invoice.number)
                    part = (
                        cash_basis_values[invoice.id] / invoice.amount_total)
                    for invoice_tax in invoice.tax_line:
                        
        return res
