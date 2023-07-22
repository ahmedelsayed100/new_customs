# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountPayment(models.Model):
    _inherit = "account.payment"

    employee_payment_id = fields.Many2one('emlpoyee.payment.register', ondelete='set null', copy=False)

    def open_payment_register(self):
        return {
            'name': 'Employee Register Payment',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'emlpoyee.payment.register',
            'domain': [('id', '=', self.employee_payment_id.id)],
        }


class DealPaymentType(models.Model):
    _name = 'deal.payment.type'
    _description = 'Deal Payment Type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char('نوع المعاملة', )

    @api.multi
    def unlink(self):
        for record in self:
            raise UserError(_("لا يمكنك الحذف ."))
        return super(EmployeeRegisterPayment, self).unlink()


class PaymentSuper(models.Model):
    _name = 'payment.super'
    _description = 'payment Super'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('الاسم', required=True, copy=False)
    line_ids = fields.One2many('payment.super.line', 'payment_super_id')

    @api.multi
    def unlink(self):
        for record in self:
            raise UserError(_("لا يمكنك الحذف ."))
        return super(EmployeeRegisterPayment, self).unlink()


class PaymentSuperLine(models.Model):
    _name = 'payment.super.line'
    _description = 'payment Super Line'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    payment_super_id = fields.Many2one('payment.super')
    payment_date = fields.Date('التاريخ')
    payment_amount = fields.Float('المبلغ')
    note = fields.Char('ملاحظات')
    is_paid = fields.Boolean('تم الدفع')


class EmployeeRegisterPayment(models.Model):
    _name = 'emlpoyee.payment.register'
    _description = 'payment register'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.multi
    def unlink(self):
        for record in self:
            raise UserError(_("لا يمكنك الحذف ."))
        return super(EmployeeRegisterPayment, self).unlink()

    name = fields.Char('الاسم', required=True, )
    reject_reason = fields.Char('Reason', readonly=1, copy=False)
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', )
    state = fields.Selection([
        ('employee', 'Employee'),
        ('manager', 'Manager'),
        ('accountant', 'Accountant'),
        ('ceo', 'CEO'),
        ('confirm', 'Accountant Confirm'),
        ('done', 'Done'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled')], track_visibility=True, readonly=True, default='employee', copy=False,
        string="Status")

    # Dictionary to map keys to labels
    STATE_LABELS = {
        'employee': 'Employee',
        'manager': 'Manager',
        'accountant': 'Accountant',
        'ceo': 'CEO',
        'confirm': 'Accountant Confirm',
        'done': 'Done',
        'rejected': 'Rejected',
        'cancelled': 'Cancelled'
    }

    # Previous state attribute
    previous_state = fields.Char(string='Previous State', store=True)
    # previous_states = fields.Char(string='Previous States', store=True)

    # Override write method to update previous_states
    # def write(self, vals):
    #     if 'state' in vals:
    #         # Add the current state to the stack of previous states
    #         previous_states = self.previous_states.split(',') if self.previous_states else []
    #         previous_states.append(self.state)
    #         self.previous_states = ','.join(previous_states)
    #         self.previous_state = previous_states[-1] if previous_states else ''
    #     return super().write(vals)
    partner_id = fields.Many2one('res.partner', 'Partner', )
    amount = fields.Float('Payment Amount')
    journal_id = fields.Many2one(string="Journal", comodel_name="account.journal",
                                 domain="[('type','in',['bank','cash'])]")
    payment_date = fields.Date('Payment Date')
    memo = fields.Char('Memo')
    payment_method_id = fields.Many2one(comodel_name='account.payment.method', string='Payment Method', required=True,
                                        help="The payment method used by the payments in this batch.")
    payment_deal_id = fields.Many2one(comodel_name='deal.payment.type', string='نوع المعاملة', )
    payment_template_id = fields.Many2one(comodel_name='payment.super', string=' الدفعات', )

    is_signed_by_employee = fields.Boolean()
    is_signed_by_accountant = fields.Boolean()
    is_signed_by_manager = fields.Boolean()
    is_signed_by_ceo = fields.Boolean()

    group_id = fields.Many2one('res.groups')

    # user_id=fields.Many2one('res.users',lambda self:self.env.user)

    def get_group_id_by_name(self, group_name):
        group = self.env['res.groups'].search([('name', '=', group_name)], limit=1)
        if group:
            return group
        else:
            return False

    @api.onchange('state')
    def _onchange_state_to_get_signature(self):
        if self.state:
            if self.state == 'employee':
                self.is_signed_by_employee = True
                self.group_id = self.get_group_id_by_name(group_name="صلاحية موظف")
            if self.state == 'accountant':
                self.is_signed_by_accountant = True
                self.group_id = self.get_group_id_by_name(group_name="accountant_group")
            if self.state == 'manager':
                self.is_signed_by_manager = True
                self.group_id = self.get_group_id_by_name(group_name="manager_group")
            if self.state == 'ceo':
                self.is_signed_by_ceo = True
                self.group_id = self.get_group_id_by_name(group_name="ceo_group")
        else:
            self.is_signed_by_employee = True
            self.group_id = self.get_group_id_by_name(group_name="employee_group")

    def action_reject(self):
        view_id = self.env.ref("new_custom.aspl_reason_payment_reject_wizard")
        # previous_states = self.previous_states.split(',') if self.previous_states else []
        # previous_state = previous_states.pop() if previous_states else None
        # self.previous_states = ','.join(previous_states)
        # self.write({'previous_states': self.previous_states})
        # print("updated: ",self.previous_states)
        previous_state = self.state
        return {
            'name': 'Reason for Rejected',
            'res_model': 'hr.payment.request.reject',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id.id,
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_travel_request_id': self.id,
                'previous_state': previous_state,
            },
        }

    def action_to_manager(self):
        self.write({'state': 'manager'})

    def action_to_accountant(self):
        self.write({'state': 'accountant'})

    def action_to_ceo(self):
        self.write({'state': 'ceo'})

    def action_to_accountant_confirmation(self):
        self.write({'state': 'confirm'})

    def action_to_confirmed(self):
        vals = {
            'payment_type': 'outbound',
            'partner_type': 'supplier',
            'partner_id': self.partner_id.id,
            'amount': self.amount,
            'payment_date': self.payment_date,
            'payment_method_id': self.payment_method_id.id,
            'journal_id': self.journal_id.id,
            'communication': self.memo,
            'employee_payment_id': self.id,
        }

        payment = self.env['account.payment']
        payment_id = payment.create(vals)
        payment_id.employee_payment_id = self.id
        payment_id.post()

        self.write({'state': 'done'})

    def action_to_cancelled(self):
        self.write({'state': 'cancelled'})

    def open_payment(self):
        return {
            'name': 'Employee Register Payment',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'account.payment',
            'domain': [('employee_payment_id', '=', self.id)],
        }


class UserSignature(models.Model):
    _name = 'user.signature'
    _description = 'user signature'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    partner_id = fields.Many2one('res.partner', string="User")
    partner_signature = fields.Binary('Signature')


class ResGroups(models.Model):
    _inherit = 'res.groups'

    group_image = fields.Binary('Group Image')
