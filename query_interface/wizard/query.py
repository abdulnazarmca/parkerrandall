# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError


class QueryInterface(models.TransientModel):
    _name = "query.interface"

    name = fields.Text(string='Query', required=True)

    @api.multi
    def query_execute(self):
        return self.env.cr.execute(self.name)






