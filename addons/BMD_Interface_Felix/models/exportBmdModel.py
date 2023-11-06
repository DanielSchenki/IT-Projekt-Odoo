from odoo import models, fields, api


class exportBmdModel(models.Model):
    _inherit = 'account.move.line'


    def export_bmd(self):
        print("==============> Generating csv Files for BMD export")
        pass
