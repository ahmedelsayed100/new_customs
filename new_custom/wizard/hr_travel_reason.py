# coding: utf-8
##################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)          #
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.                     #
# All Rights Reserved.                                                           #
#                                                                                #
# This program is copyright property of the author mentioned above.              #
# You can`t redistribute it and/or modify it.                                    #
#                                                                                #
##################################################################################

from odoo import models, fields, api
from datetime import date


class RejectReason(models.TransientModel):
    _name = 'hr.payment.request.reject'
    _rec_name = 'travel_request_id'
    _description = "Reason for Rejection"

    travel_request_id = fields.Many2one(comodel_name='emlpoyee.payment.register',required=True)
    reason = fields.Char(string="Reason", required=True)

    @api.multi
    def action_reject(self):
        self.travel_request_id.sudo().write({'reject_reason': self.reason,
                                             'state': 'rejected'})

