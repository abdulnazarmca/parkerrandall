# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools



class SaleOrderLine(models.Model):
    
    _inherit = 'sale.order.line'

    sale_order_id = fields.Many2one(related="order_id", string="Sale Order ID")

