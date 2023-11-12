from odoo import models, fields, api
import csv
import os

# This class handles the export of journal items to BMD in Odoo
class exportBmdModel(models.Model):
    _inherit = 'account.move.line'


    def export_bmd(self):
        print("==============> Generating csv Files for BMD export")
        pass

    @api.model
    def export_journal_items(self):
        # Get all journal items
        journal_items = self.env['account.move.line'].search([('move_id', '>', 0)])

        #save every needed field in a variable
        for line in journal_items:   #TODO Correct the fields
            konto = line.account_id.code
            gkonto = line.account_id.code
            belegnr = line.move_id.name
            belegdatum = line.move_id.date
            steuercode = line.tax_ids.name
            buchcode = line.move_id.name
            betrag = line.debit
            prozent = line.tax_ids.amount
            steuer = line.tax_ids.amount
            text = line.name
            zziel = line.move_id.name
            skontopz = line.move_id.name
            skontotage = line.move_id.name

        path = "/path/to/export.csv"

        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Write into a CSV file the following fields: konto, gkonto, belegnr, belegdatum, steuercode, buchcode, betrag, prozent, steuer, text, zziel, skontopz, skontotage





        return True

