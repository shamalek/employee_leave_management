from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from datetime import date


class LeaveRequest(models.Model):
    _name = 'leave.request'
    _description = 'Leave Request'

    emp_name_two = fields.Many2one('hr.employee', string="Employee")
    leave_type = fields.Selection(
        [('casual', 'CASUAL'), ('sick', 'SICK'), ('unpaid', 'UNPAID'), ('paid', 'PAID')],
        string="Leave Type"
    )
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    leave_status = fields.Selection(
        [('draft', 'DRAFT'), ('approved', 'APPROVED'), ('reject', 'REJECT')],
        string="Status", default='draft'
    )

    # Approve leave (Admin only)
    def action_approve(self):
        for rec in self:
            if not self.env.user.has_group('base.group_system'):
                raise UserError("Only Administrator can approve leave requests.")
            if rec.leave_status != 'draft':
                continue
            rec.leave_status = 'approved'

    # Reject leave (Admin only)
    def action_reject(self):
        for rec in self:
            if not self.env.user.has_group('base.group_system'):
                raise UserError("Only Administrator can reject leave requests.")
            if rec.leave_status not in ('draft', 'approved'):
                continue
            rec.leave_status = 'reject'

    # Reset rejected leave to draft (Employee only)
    def action_reset_to_draft(self):
        for rec in self:
            if rec.emp_name_two.user_id != self.env.user:
                raise UserError("You can only reset your own rejected leave requests.")
            if rec.leave_status != 'reject':
                continue
            rec.leave_status = 'draft'


@api.constrains('start_date', 'end_date')


def _check_leave_dates(self):
    for rec in self:
        if not rec.start_date or not rec.end_date:
            continue

        if rec.end_date < rec.start_date:
            raise ValidationError(
                "End Date cannot be earlier than Start Date."
            )
        if rec.start_date < date.today():
            raise ValidationError(
                "You cannot request leave in the past."
            )
