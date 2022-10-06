from odoo import  models, fields

class HrContract(models.Model):
    _inherit = "hr.contract"
    _description = "Allowance Page"



    houserent =fields.Float(string="House Rent")
    medical =fields.Float(string="Medical / Utilities")
    conveyance =fields.Float(string="Conveyance ")

