from odoo import models,api,fields


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    is_work_entry = fields.Boolean()

    @api.model
    def set_work_time(self):
        attendances = self.browse(self._context.get('active_ids'))
        for rec in attendances:
            if not rec.is_work_entry:
                if rec.check_in and rec.check_out:
                    self.env['hr.work.entry'].sudo().create({'employee_id': rec.employee_id.id,
                                                             'date_start': rec.check_in,
                                                             'date_stop': rec.check_out,
                                                             'work_entry_type_id': 1,
                                                             'name': 'Attendance: '+ rec.employee_id.name})
                rec.write({
                    'is_work_entry':True
                })