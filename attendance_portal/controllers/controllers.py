# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

from datetime import datetime , timedelta
import time

from odoo import api, fields, models, exceptions, _


class AttendancePortal(http.Controller):

    @http.route('/attendance', auth='public', website=True)
    def list(self, **kw):
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])
        if employee:
            return http.request.render('website.page_attendance',
                                       {'status': employee.attendance_state})
        else:
            return 'This user is not linked with Employee.Please contact administrator.'

    @http.route('/attendance/checkin', type='json', auth='user')
    # @http.route('/attendance/checkin', type='http', auth='user')
    def attendance_checkin_record(self,**kwargs):
        checkin_time= fields.Datetime.now()
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])
        vals = {
                'employee_id': employee.id,
                'check_in': checkin_time,
            'check_in_latitude':request.jsonrequest['latitude'],
            'check_in_longitude':request.jsonrequest['longitude']
        }
        employee.attendance_state = 'checked_in'
        return request.env['hr.attendance'].sudo().create(vals)

    @http.route('/attendance/checkout', type='json', auth='user')
    def attendance_checkout_record(self):
        checkout_time = fields.Datetime.now()
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])
        attendance = request.env['hr.attendance'].sudo().search([('employee_id', '=', employee.id), ('check_out', '=', False)],
                                                      limit=1)
        if attendance:
            attendance.check_out = checkout_time
            attendance.check_out_latitude= request.jsonrequest.get('latitude')
            attendance.check_out_longitude=  request.jsonrequest.get('longitude')
            employee.attendance_state = 'checked_out'
            request.env['hr.work.entry'].sudo().create({
                'name': 'Portal Attendance',
                'contract_id': employee.contract_id.id,
                'work_entry_type_id': request.env['hr.work.entry.type'].sudo().search([('name', '=', 'Attendance')]).id,
                'employee_id': employee.id,
                'date_start': attendance.check_in,
                'date_stop': attendance.check_out
            })
        else:
            raise exceptions.UserError(
                _('Cannot perform check out on %(empl_name)s, could not find corresponding check in. '
                  'Your attendances have probably been modified manually by human resources.') % {
                    'empl_name': request.env.user.name, })



        return attendance

    @http.route(['/my/attendances','/my/attendances/<string:day>'], auth='user', website=True)
    def my_attendances(self, **kw):
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])
        date_now = datetime.now()
        date_quarter = date_now + timedelta(days=-90)
        date_year = date_now + timedelta(days=-365)
        date_month = date_now + timedelta(days=-30)
        date_fortnight = date_now + timedelta(days=-15)
        date_week = date_now + timedelta(days=-7)
        yesterday = date_now + timedelta(days=-1)
        if kw.get('day'):
            if kw.get('day') == '7':
                attendances = http.request.env['hr.attendance'].sudo().search([('employee_id','=',employee.id),('check_in','>=',date_week)])
                print('attendances,,,,,', attendances)
                length_of_attend = attendances.__len__()
                print('length_of_attend,,,,,', length_of_attend)

            if kw.get('day') == '15':
                attendances = http.request.env['hr.attendance'].sudo().search([('employee_id','=',employee.id),('check_in','>=',date_fortnight)])
                print('attendances,,,,,', attendances)
                length_of_attend = attendances.__len__()
                print('length_of_attend,,,,,', length_of_attend)
            if kw.get('day') == '30':
                attendances = http.request.env['hr.attendance'].sudo().search([('employee_id','=',employee.id),('check_in','>=',date_month)])
                print('attendances,,,,,', attendances)
                length_of_attend = attendances.__len__()
                print('length_of_attend,,,,,', length_of_attend)
            if kw.get('day') == '90':
                attendances = http.request.env['hr.attendance'].sudo().search([('employee_id','=',employee.id),('check_in','>=',date_quarter)])
                print('attendances,,,,,', attendances)
                length_of_attend = attendances.__len__()
                print('length_of_attend,,,,,', length_of_attend)
            if kw.get('day') == '365':
                attendances = http.request.env['hr.attendance'].sudo().search([('employee_id','=',employee.id),('check_in','>=',date_year)])
                print('attendances,,,,,', attendances)
                length_of_attend = attendances.__len__()
                print('length_of_attend,,,,,', length_of_attend)
        else:
            attendances = http.request.env['hr.attendance'].sudo().search([('employee_id', '=', employee.id)])
            length_of_attend = attendances.__len__()
            print('length_of_attend,,,,,', length_of_attend)
        return http.request.render('attendance_portal.my_attendance_template_id',
                                   {'attendances': attendances})

    # @http.route('/my/attendances-7', auth='user', website=True)
    # def my_attendances_filter(self, **kw):
    #     print('hellow im printed by kw', kw)
    #     employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])
    #     print('hellow im printed by employee', employee)
    #     attendances = http.request.env['hr.attendance'].sudo().search([('employee_id','=',employee.id)])
    #     date_now = datetime.datetime.now()
    #     print('date_now in', date_now)
    #     if attendances:
    #         for attendance in attendances:
    #             check_in = attendance.check_in
    #             print('check in', check_in)
    #     print('hellow im printed by attendances', attendances)
    #     return http.request.render('attendance_portal.my_attendance_7', {
    #         'attendances': attendances})

