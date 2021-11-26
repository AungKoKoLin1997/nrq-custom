# -*- coding: utf-8 -*-
# Copyright 2016 Rooms For (Hong Kong) Limited T/A OSCG
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    delivery_note = fields.Boolean(string="Delivery Note",)
    doc_title = fields.Char(string="Doc Title",)
    salesman_id = fields.Many2one(
        comodel_name="res.users", string="Salesperson", track_visibility="onchange"
    )

    @api.onchange("partner_id")
    def onchange_partner(self):
        for invoice in self:
            invoice.delivery_note = invoice.partner_id.delivery_note

    @api.onchange("invoice_line_ids")
    def _onchange_origin(self):
        purchase_ids = self.invoice_line_ids.mapped("purchase_id")
        if purchase_ids:
            self.origin = ", ".join(purchase_ids.mapped("name"))
            self.doc_title = ""
            for title in purchase_ids.mapped("doc_title"):
                if title:
                    if self.doc_title == "":
                        self.doc_title += title
                    else:
                        self.doc_title += ", " + title
            for user_id in purchase_ids.mapped("user_id"):
                self.salesman_id = user_id
            for currency_id in purchase_ids.mapped("currency_id"):
                self.currency_id = currency_id
