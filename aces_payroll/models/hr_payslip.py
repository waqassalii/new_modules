# -*- coding: utf-8 -*-
import calendar
from datetime import datetime
from datetime import timedelta

import pytz
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    _description = 'payroll_calculation'

    bonus_label = fields.Char('Bonus level')
    bonus_type = fields.Selection([
        ('fixed', 'Fixed Amount'),
        ('percentage', 'Percentage')
    ], String='Bonus Type')
    bonus_amount = fields.Float('Bonus')
    total_bonus_amount = fields.Float('Bonus Amount')
    late_attendances_ids = fields.One2many('late.attendances.line', 'payslip_id', ondelete='cascade',
                                           string='Late Attendances')

    monday_line_ids = fields.One2many('monday.line', 'payslip_id', ondelete='cascade', string='Monday Off')

    @api.onchange('bonus_type', 'bonus_amount')
    def onchange_bonus(self):
        if self.bonus_amount and self.bonus_type:
            if self.bonus_type =='fixed':
                self.total_bonus_amount = self.bonus_amount
            else:
                self.total_bonus_amount = self.contract_id.wage * (self.bonus_amount/100)

    @api.onchange('employee_id', 'struct_id', 'contract_id', 'date_from', 'date_to')
    def _onchange_employee(self):
        result = super(HrPayslip, self)._onchange_employee()
        self.input_line_ids = False
        inputs = self.env['hr.payslip.input.type'].search([('struct_ids', '=', self.struct_id.id)])
        update = []
        for rec in inputs:
            if rec.code == 'CY':
                if self.contract_id.houserent > 0:
                    update.append((0, 0, {
                        'input_type_id': rec.id,
                        'contract_id': self.contract_id.id,
                        'sequence': '8',
                        'amount': self.contract_id.houserent
                    }))
            elif rec.code == 'MD':
                if self.contract_id.medical > 0:
                    update.append((0, 0, {
                        'input_type_id': rec.id,
                        'contract_id': self.contract_id.id,
                        'sequence': '8',
                        'amount': self.contract_id.medical
                    }))
            elif rec.code == 'HR':
                if self.contract_id.conveyance > 0:
                    update.append((0, 0, {
                        'input_type_id': rec.id,
                        'contract_id': self.contract_id.id,
                        'sequence': '9',
                        'amount': self.contract_id.conveyance
                    }))
        self.update({'input_line_ids': update})
        self.late_attendances_ids = False
        attendance_list = []
        attendances = self.env['hr.attendance'].search(
            [('employee_id', '=', self.employee_id.id), ('check_in', '>=', self.date_from),
             ('check_in', '<=', self.date_to)])
        res_calendar = self.env['resource.calendar'].search([('id', '=', self.employee_id.resource_calendar_id.id)])
        if res_calendar:
            for days in res_calendar.attendance_ids:
                day = days.dayofweek
                name_of_day = dict(days.fields_get(allfields=['dayofweek'])['dayofweek']['selection'])[days.dayofweek]

                for attendance in attendances:
                    at_day = attendance.check_in.strftime("%A")
                    if at_day == name_of_day:
                        similar = at_day
                        user_tz = pytz.timezone(self.env.get('tz') or self.env.user.tz)
                        pak_time = pytz.utc.localize(attendance.check_in).astimezone(user_tz)

                        user_hour = pak_time.hour
                        user_min = pak_time.minute
                        user_float_time = user_hour + (user_min / 60)
                        grace = (res_calendar.grace_time) * 60 / 100
                        user_time = round(user_float_time, 2)
                        schedule = (days.hour_from + grace)
                        if user_time > schedule:
                            attendance_list.append((0, 0, {
                                'check_in': attendance.check_in,
                                'check_out': attendance.check_out,
                                'hours': attendance.worked_hours,
                                'date': attendance.check_in,
                                'payslip_id': self.id,
                            }))
        self.update({
            'late_attendances_ids': attendance_list
        })
        monday_list = []
        self.monday_line_ids = False
        num_of_days = (self.date_to - self.date_from).days + 1
        for i in range(0, num_of_days):
            date_from = self.date_from + timedelta(days=i)
            month_days = calendar.day_name[date_from.weekday()]
            if month_days == 'Monday':
                date_time_from = datetime.strptime(date_from.strftime('%Y%m%d'), '%Y%m%d')
                monday_min = datetime.combine(date_time_from, date_time_from.time().min)
                monday_max = datetime.combine(date_time_from, date_time_from.time().max)
                user_tz = pytz.timezone(self.env.get('tz') or self.env.user.tz)
                monday_attendances = self.env['hr.attendance'].search([('employee_id', '=', self.employee_id.id),
                                                                       ('check_in', '>=', monday_min),
                                                                       ('check_in', '<=', monday_max)])
                if not monday_attendances:
                    print('im not absent today')
                    monday_list.append((0, 0, {
                        'monday_date': date_time_from
                    }))
        self.update({
            'monday_line_ids': monday_list,
        })
        return
    def add_bonus_amount_other_input(self):
        self.input_line_ids=False
        input_type = self.env['hr.payslip.input.type'].search([('code', '=', 'BO')])
        for rec in self:
            my_list = []
            my_list.append((0, 0, {
                'amount': rec.total_bonus_amount,
                'input_type_id': input_type.id
            }))
            self.write({
                'input_line_ids': my_list
            })

    def _get_worked_day_lines(self, domain=None, check_out_of_contract=True):
        """
        :returns: a list of dict containing the worked days values that should be applied for the given payslip
        """
        res = []
        # super(WorkedDayOvertime,self)._get_worked_day_lines()

        def day_name_cal(day):
            if day == '0':
                return "Monday"
            elif day == '1':
                return 'Tuesday'
            elif day == '2':
                return 'Wednesday'
            elif day == '3':
                return 'Thursday'
            elif day == '4':
                return 'Friday'
            elif day == '5':
                return 'Saturday'
            elif day == '6':
                return 'Sunday'

        total_time=0
        attendance_duration=0
        attendance_days=0
        day_count = 0
        date_from_cont = fields.Datetime.from_string(self.contract_id.date_start)
        date_from_cont = str(date_from_cont)
        date_to_cont = fields.Datetime.from_string(self.contract_id.date_end)
        date_to_cont = str(date_to_cont)
        days_of_schedule = []

        for days in self.contract_id.resource_calendar_id.attendance_ids:
            days_of_schedule.append(str(day_name_cal(days.dayofweek)))


        for attn in self.env['hr.work.entry'].search([('date_start', '>=', self.date_from),
                                                      ('date_stop', '<=', self.date_to),
                                                      ('employee_id', '=', self.employee_id.id),
                                                      ('work_entry_type_id', '=', 1)]):
            day_from = datetime.strptime(str(self.date_from), "%Y-%m-%d")
            day_to = datetime.strptime(str(self.date_to), "%Y-%m-%d")
            nb_of_days = (day_to - day_from).days + 1
            for day in range(0, nb_of_days):
                current_date = calendar.day_name[day_from.weekday()]
                if attn.date_start.date() == day_from.date():
                    for hours in self.contract_id.resource_calendar_id.attendance_ids:
                        time = hours.hour_to - hours.hour_from
                        time_over = attn.duration - time
                        if str(current_date) == str(day_name_cal(hours.dayofweek)):
                            if time_over > 0:
                                total_time += time_over
                                day_count += 1
                                attendance_duration += attn.duration - time_over
                                attendance_days += 1
                            else:
                                attendance_duration += attn.duration
                                attendance_days += 1
                        elif current_date not in days_of_schedule:
                            total_time += attn.duration
                            day_count += 1
                            break
                day_from = day_from + relativedelta(days=1)

        upaid_leaves_hours = 0
        for leave in self.env['hr.work.entry'].search([('date_start', '>=', self.date_from),
                                                      ('date_stop', '<=', self.date_to),
                                                      ('employee_id', '=', self.employee_id.id),
                                                      ('work_entry_type_id', '=', 5)]):
            upaid_leaves_hours += leave.duration
        res.append({
            'sequence': 6,
            'work_entry_type_id': self.env['hr.work.entry.type'].search([('id', '=', 5)]).id,
            'number_of_days': upaid_leaves_hours/8,
            'number_of_hours': upaid_leaves_hours,
            'code':'LEAVE90'
        })
        sick_leaves_hours = 0
        for leave in self.env['hr.work.entry'].search([('date_start', '>=', self.date_from),
                                                      ('date_stop', '<=', self.date_to),
                                                      ('employee_id', '=', self.employee_id.id),
                                                      ('work_entry_type_id', '=', 6)]):
            sick_leaves_hours += leave.duration
        res.append({
            'sequence': 6,
            'work_entry_type_id': self.env['hr.work.entry.type'].search([('id', '=', 6)]).id,
            'number_of_days': sick_leaves_hours/8,
            'number_of_hours': sick_leaves_hours,
            'code':'LEAVE110'
        })
        paid_leaves_hours = 0
        for leave in self.env['hr.work.entry'].search([('date_start', '>=', self.date_from),
                                                       ('date_stop', '<=', self.date_to),
                                                       ('employee_id', '=', self.employee_id.id),
                                                       ('work_entry_type_id', '=', 7)]):
            paid_leaves_hours += leave.duration
        res.append({
            'sequence': 6,
            'work_entry_type_id': self.env['hr.work.entry.type'].search([('id', '=', 7)]).id,
            'number_of_days': paid_leaves_hours / 8,
            'number_of_hours': paid_leaves_hours,
            'code': 'LEAVE120'
        })
        res.append({
            'sequence': 5,
            'work_entry_type_id': self.env['hr.work.entry.type'].search([('name', '=', 'Attendance')]).id,
            'number_of_days': attendance_days,
            'number_of_hours': attendance_duration,
        })

        # self.ensure_one()
        contract = self.contract_id
        if contract.resource_calendar_id:
            # res = self._get_worked_day_lines_values(domain=domain)
            if not check_out_of_contract:
                return res

            # If the contract doesn't cover the whole month, create
            # worked_days lines to adapt the wage accordingly
            out_days, out_hours = 0, 0
            reference_calendar = self._get_out_of_contract_calendar()
            if self.date_from < contract.date_start:
                start = fields.Datetime.to_datetime(self.date_from)
                stop = fields.Datetime.to_datetime(contract.date_start) + relativedelta(days=-1, hour=23, minute=59)
                out_time = reference_calendar.get_work_duration_data(start, stop, compute_leaves=False)
                out_days += out_time['days']
                out_hours += out_time['hours']
            if contract.date_end and contract.date_end < self.date_to:
                start = fields.Datetime.to_datetime(contract.date_end) + relativedelta(days=1)
                stop = fields.Datetime.to_datetime(self.date_to) + relativedelta(hour=23, minute=59)
                out_time = reference_calendar.get_work_duration_data(start, stop, compute_leaves=False)
                out_days += out_time['days']
                out_hours += out_time['hours']

            if out_days or out_hours:
                work_entry_type = self.env.ref('hr_payroll.hr_work_entry_type_out_of_contract')
                res.append({
                    'sequence': work_entry_type.sequence,
                    'work_entry_type_id': work_entry_type.id,
                    'number_of_days': out_days,
                    'number_of_hours': out_hours,
                })
        return res

class AmountPayslipLines(models.Model):
    _inherit = 'hr.payslip.worked_days'

    @api.depends('is_paid', 'number_of_hours', 'payslip_id', 'payslip_id.normal_wage', 'payslip_id.sum_worked_hours')
    def _compute_amount(self):

        for worked_days in self:
            if not worked_days.contract_id:
                worked_days.amount = 0
                continue
            day_from = datetime.strptime(str(worked_days.payslip_id.date_from), "%Y-%m-%d")
            day_to = datetime.strptime(str(worked_days.payslip_id.date_to), "%Y-%m-%d")
            nb_of_days = (day_to - day_from).days + 1
            calendar_time = nb_of_days*8
            if calendar_time:
                hourly_wages = worked_days.payslip_id.normal_wage / calendar_time
                worked_days.amount = worked_days.number_of_hours * hourly_wages
            else:
                worked_days.amount = 0



class LateAttendancesLine(models.Model):
    _name = 'late.attendances.line'
    _description = 'LateAttendancesLine'

    date = fields.Datetime('Date')
    check_in = fields.Datetime('Check In')
    check_in_float = fields.Float('Float In')
    check_out = fields.Datetime('Check Out')
    hours = fields.Float('Hours')

    payslip_id = fields.Many2one('hr.payslip', string='Payslip_id')


class MondayOffLine(models.Model):
    _name = 'monday.line'

    monday_date = fields.Date(string='Monday Off Date')
    payslip_id = fields.Many2one('hr.payslip', string='Payslip_id')
