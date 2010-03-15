# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import tools
from osv import fields,osv

class hr_holidays_report(osv.osv):
    _name = "hr.holidays.report"
    _description = "Leaves Statistics"
    _auto = False
    _rec_name = 'date'
    _columns = {
        'date': fields.date('Date', readonly=True),
        'year': fields.char('Year', size=4, readonly=True),
        'month':fields.selection([('01','January'), ('02','February'), ('03','March'), ('04','April'),
            ('05','May'), ('06','June'), ('07','July'), ('08','August'), ('09','September'),
            ('10','October'), ('11','November'), ('12','December')], 'Month',readonly=True),
        'date_from' : fields.datetime('Start Date', readonly=True),
        'date_to' : fields.datetime('End Date', readonly=True),
        'number_of_days_temp': fields.float('Number of Days', readonly=True),
        'employee_id' : fields.many2one('hr.employee', "Employee's Name",readonly=True),
        'user_id':fields.many2one('res.users', 'User', readonly=True),
        'state': fields.selection([('draft', 'Draft'),
                                   ('confirm', 'Waiting Validation'),
                                   ('refuse', 'Refused'),
                                   ('validate', 'Validated'),
                                   ('cancel', 'Cancelled')]
                                   ,'State', readonly=True),
    }
    _order = 'date desc'
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'hr_holidays_report')
        cr.execute("""
            create or replace view hr_holidays_report as (
                 select
                     min(s.id) as id,
                     s.create_date as date,
                     to_char(s.date_from,'YYYY/mm/dd') as date_from,
                     to_char(s.date_to,'YYYY/mm/dd') as date_to,
                     s.number_of_days_temp,
                     s.employee_id,
                     s.user_id as user_id,
                     to_char(s.create_date, 'YYYY') as year,
                     to_char(s.create_date, 'MM') as month,
                     s.state
                     from
                 hr_holidays s
                 group by
                     s.create_date,s.state,s.date_from,s.date_to,
                     s.number_of_days_temp,s.employee_id,s.user_id
            )
        """)
hr_holidays_report()

