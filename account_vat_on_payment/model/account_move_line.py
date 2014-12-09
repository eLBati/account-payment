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


    def _prepare_vat_move(self, move):
        return {
            'journal_id': (
                move.journal_id.vat_on_payment_related_journal_id.id
            ),
            'period_id': move.period_id.id,
            'date': move.date,
        }

    def _get_move_lines_to_transform(self):
        """
        Returns {invoice_id: [line_id, line_id]}
        Dict values are income/expense and tax lines
        """
        move_lines_to_transform = {}
        for move_line in self:
            if move_line.invoice:
                move_lines_to_transform[move_line.invoice.id] = []
                for partner_move_line in move_line.move_id.line_id:
                    if (
                        partner_move_line.invoice and
                        partner_move_line.account_id.type
                        != self._context['cash_basis_payment_type']
                    ):
                        move_lines_to_transform[move_line.invoice.id].append(
                            partner_move_line.id)
        return move_lines_to_transform

    def 

    @api.multi
    def _create_vat_on_payment_move(self):
        """
        to be used setting the following values in context:
         - cash_basis_paid_percentage is in the form
           {invoice_id: percentage}
         - cash_basis_payment_type can be 'receivable' or 'payable'
         - cash_basis_payment_date is the payment date
         - cash_basis_payment_move_id is the account.move on the bank/cash
           journal
        """
        if (
            'cash_basis_paid_percentage' in self._context
            and 'cash_basis_payment_type' in self._context
            and 'cash_basis_payment_date' in self._context
            and 'cash_basis_payment_move_id' in self._context
        ):
            cash_basis_paid_percentage = self._context[
                'cash_basis_paid_percentage']
            move_lines_to_transform = self._get_move_lines_to_transform()

    def reconcile_partial(
        self, cr, uid, ids, type='auto', context=None, writeoff_acc_id=False,
        writeoff_period_id=False, writeoff_journal_id=False
    ):
        res = super(AccountMoveLine, self).reconcile_partial(
            cr, uid, ids, type=type, context=context,
            writeoff_acc_id=writeoff_acc_id,
            writeoff_period_id=writeoff_period_id,
            writeoff_journal_id=writeoff_journal_id)
        self._create_vat_on_payment_move(cr, uid, ids, context=context)
        return res
