# -*- coding: utf-8 -*-
from odoo import models, fields, api
import time
from datetime import datetime, timedelta
from odoo.exceptions import except_orm, Warning, RedirectWarning, UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class PartnerStatementReport(models.AbstractModel):
    _name = 'report.account_partner_statement.partner_statement_report_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form') or not self.env.context.get('active_model') or not self.env.context.get('active_id'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))

#        invoice_list = self.get_invoice(partner, data)
        return {
            'doc_ids': self.ids,
            'doc_model': model,
            'data': data['form'],
            'docs': docs,
            'time': time,
#            'invoice_value': invoice_value,

        }





