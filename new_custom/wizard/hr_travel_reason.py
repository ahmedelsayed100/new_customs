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
        stat = self.env.context.get('previous_state')
        previous_statee = stat
        if stat == 'employee':
            previous_statee = 'employee'
        elif stat == 'manager':
            previous_statee = 'employee'
        elif stat == 'accountant':
            previous_statee = 'manager'
        elif stat == 'ceo':
            previous_statee = 'accountant'
        elif stat == 'confirm':
            previous_statee = 'ceo'
        elif stat == 'done':
            previous_statee = 'confirm'
        elif stat == 'cancelled':
            previous_statee = 'employee'
        # previous_statee = self.env.context.get('previous_state')                #retrieve previous state from context
        self.travel_request_id.sudo().write({'reject_reason': self.reason,
                                             'state': previous_statee})

