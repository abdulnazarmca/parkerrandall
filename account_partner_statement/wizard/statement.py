# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning, RedirectWarning, UserError, ValidationError
import odoo.addons.decimal_precision as dp

class PartnerStatementWizard(models.TransientModel):
    _name = 'partner.statement.wizard'

    def _get_default_note(self):
        result = """
            <div>
                <p><b>Dear Sir/Madam</b></p>
                <p>Kindly verify the below statement.<p/>
            </div>"""
        return result



    date_from = fields.Date(string='From Date')
    date_to = fields.Date(string='To Date')
    payment_date_to = fields.Date(string='Upto Date of Payments')
    note = fields.Html(string='Content', required=True, default=_get_default_note)
    partner_type = fields.Selection([('customer', 'Customer'), ('supplier', 'Vendor')], string='Partner Type', required=True)
    partner_ids = fields.Many2many('res.partner', string='Partners', required=True)   
    print_landscape = fields.Boolean(string='Print Landscape')
    currency_id = fields.Many2one('res.currency', string='Currency')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env['res.company']._company_default_get('partner.statement.wizard'))


    @api.constrains('date_from','date_to')
    def _check_date_constrains(self):
        if self.date_from and self.date_to and self.date_from > self.date_to:
            raise ValidationError(_("To Date should be greater than From Date"))


    @api.onchange('partner_type')
    def _onchange_partner_type(self):
        # Set partner_id domain
        self.partner_ids = False
        if self.partner_type:
            return {'domain': {'partner_ids': [(self.partner_type, '=', True)]}}



    def get_domain(self, domain):
        if self.partner_type == 'customer':domain += [('type', 'in', ('out_invoice', 'out_refund'))]
        else:domain += [('type', 'in', ('in_invoice', 'in_refund'))]
        if self.date_from:domain += [('date_invoice', '>=', self.date_from)]
        if self.date_to:domain += [('date_invoice', '<=', self.date_to)]
        return domain

    def get_invoice(self, partner):
        invoice_obj = self.env['account.invoice']
        domain = [('partner_id', '=', partner.id), ('state', 'not in', ['draft', 'cancel']), ('company_id','=',self.company_id.id)]
        domain += self.get_domain(domain)
        invoice_ids = invoice_obj.search(domain, order='date_invoice')
        return sorted(invoice_ids, key=lambda x: x.id, reverse=False)

    def convert_rate(self, amount, date, from_currency):
        to_currency = self.company_id.currency_id
        if self.currency_id:to_currency = self.currency_id
        amount = from_currency._convert(amount, to_currency, self.company_id, date or fields.Date.today())
        return amount


    def _compute_payments(self, invoice):
        payment_lines = set()
        for line in invoice.move_id.line_ids.filtered(lambda l: l.account_id.id == invoice.account_id.id):
            payment_lines.update(line.mapped('matched_credit_ids.credit_move_id.id'))
            payment_lines.update(line.mapped('matched_debit_ids.debit_move_id.id'))
        result = self.env['account.move.line'].browse(list(payment_lines)).sorted()


    def get_outstanding_payments(self, partner):
        outstanding_debits = 0
        outstanding_credits = 0

        info = {'title': _('Outstanding Payment'), 'content': []}

        receivable_account_ids = [account.id for account in self.env['account.account'].search([('company_id','=',self.company_id.id), ('deprecated', '=', False)]) if account.internal_type == 'receivable']
        payable_account_ids = [account.id for account in self.env['account.account'].search([('company_id','=',self.company_id.id), ('deprecated', '=', False)]) if account.internal_type == 'payable']

        domain = [
                ('partner_id', '=', self.env['res.partner']._find_accounting_partner(partner).id),
                ('reconciled', '=', False),
                '|',
                '&', ('amount_residual_currency', '!=', 0.0), ('currency_id','!=', None), 
                '&', ('amount_residual_currency', '=', 0.0),
                '&', ('currency_id','=', None), ('amount_residual', '!=', 0.0)
                ]
        if self.payment_date_to:domain.extend([('date', '<=', self.payment_date_to)])



        for payment in self.env['account.move.line'].search(domain + [('account_id', 'in', receivable_account_ids)], order='date').filtered(lambda l: l.journal_id.type not in ['sale','purchase']):
            amount = self.convert_rate(payment.amount_residual,payment.date,self.company_id.currency_id)
            info['content'] += [{
                'name': payment.move_id.name,
                'journal_name': payment.journal_id.name,
                'amount': amount,
                'amount_currency': abs(payment.amount_currency),
                'currency': payment.currency_id or False,
                'date': payment.date,
                'color': 'black',
            }]


        for payment in self.env['account.move.line'].search(domain + [('account_id', 'in', payable_account_ids)], order='date').filtered(lambda l: l.journal_id.type not in ['sale','purchase']):
            amount = self.convert_rate(payment.amount_residual,payment.date,self.company_id.currency_id)
            info['content'] += [{
                'name': payment.move_id.name,
                'journal_name': payment.journal_id.name,
                'amount': amount,
                'amount_currency': abs(payment.amount_currency),
                'currency': payment.currency_id or False,
                'date': payment.date,
                'color': 'black',
            }]


        payments_lines = info['content']
        return payments_lines



    def get_invoice_payments(self, payment_move_line_ids, invoice=None):
        payments_lines = False
        total_paid = 0
        total_actual_paid = 0
        required_currency_id = self.currency_id and self.currency_id or self.company_id.currency_id
        info = {'title': _('Payment'), 'outstanding': False, 'content': []}
        if self.payment_date_to:payment_move_line_ids = payment_move_line_ids.filtered(lambda l: l.date <= self.payment_date_to)

        for payment in sorted(payment_move_line_ids, key=lambda x: x.id, reverse=False):
            
            amount = 0
            amount_currency = 0
            currency_id = payment.currency_id or self.company_id.currency_id
            if self.partner_type == 'customer':
#                amount = payment.credit
                amount = sum([p.amount for p in payment.matched_debit_ids if p.debit_move_id in invoice.move_id.line_ids])
                amount_currency = sum([p.amount_currency for p in payment.matched_debit_ids if p.debit_move_id in invoice.move_id.line_ids])

            elif self.partner_type == 'supplier':
#                amount = payment.debit
                amount = sum([p.amount for p in payment.matched_credit_ids if p.credit_move_id in invoice.move_id.line_ids])
                amount_currency = sum([p.amount_currency for p in payment.matched_credit_ids if  p.credit_move_id in invoice.move_id.line_ids])

            if invoice and payment.currency_id:total_actual_paid += amount_currency
            else:total_actual_paid += amount

            if not payment.currency_id and payment.amount_currency == 0:
                amount_currency = amount
            amount = self.convert_rate(amount,payment.date,self.company_id.currency_id)

            info['content'] += [{
                'name': payment.move_id.name,
                'journal_name': payment.journal_id.name,
                'amount': amount,
                'amount_currency': amount_currency,
                'currency': currency_id,
                'date': payment.date,
                'color': 'black',
            }]
            total_paid += amount

        if invoice and invoice.amount_total == total_actual_paid and self.convert_rate(invoice.amount_total,invoice.date_invoice,invoice.currency_id) != total_paid:

            info['content'] += [{
                'name': "Auto Adjusted Exchange Gain/Loss (Only for report purpose)",
                'journal_name': "Exchange Difference",
                'amount': self.convert_rate(invoice.amount_total,invoice.date_invoice,invoice.currency_id) - total_paid,
                'amount_currency': self.convert_rate(invoice.amount_total,invoice.date_invoice,invoice.currency_id) - total_paid,
                'currency': currency_id,
                'date': False,
                'color': 'color:#ef0410',
            }]
            total_paid += self.convert_rate(invoice.amount_total,invoice.date_invoice,invoice.currency_id) - total_paid

        status = False
        if invoice and invoice.amount_total == total_actual_paid:status = 'Fully Paid'
        elif total_actual_paid <= 0:status = 'Not Paid'
        else:status = 'Partial Paid'

        payments_lines = info['content']
        return payments_lines, total_paid, status




    @api.multi
    def print_report(self):
        data = {}
        data['form'] = self.read(['currency_id', 'date_from', 'date_to', 'payment_date_to', 'partner_type', 'partner_ids', 'note', 'company_id', 'print_landscape'])[0]
        return self.env.ref('account_partner_statement.partner_statement_report').with_context(landscape=self.print_landscape).report_action(self, data=data)



     
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

