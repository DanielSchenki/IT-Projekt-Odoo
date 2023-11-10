from odoo import models, fields, api


class AccountBmdExport(models.TransientModel):
    _name = 'account.bmd'
    _description = 'BMD Export'

    company_id = fields.Many2one(comodel_name='res.company', string="Company",
                                 required=True)
    period_date = fields.Date(string="Period Date", required=True)

    def execute(self):
        self.write('BMD_Export')