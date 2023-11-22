from odoo import models, fields, api
import csv
import os


# This class handles the export of journal items to BMD in Odoo
class exportBmdModel(models.Model):
    _inherit = 'account.move.line'

    def export_bmd(self):
        print("==============> Generating csv Files for BMD export")

        # date formatter from yyyy-mm-dd to dd.mm.yyyy
        def date_formatter(date):
            #date = date.split("-")
            #return date[2] + "." + date[1] + "." + date[0]
            return date.strftime('%d.%m.%Y')

        journal_items = self.env['account.move.line'].search([])
        result_data = []
        for line in journal_items:
            print(line)
            konto = line.account_id.code
            prozent = line.tax_ids.amount
            steuer = line.price_total - line.price_subtotal
            belegdatum = date_formatter(line.move_id.date)
            belegnr = line.move_id.name
            text = line.name

            '''gkonto = line.account_id.code
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
            result_data.append({
                'Konto': konto,
                'GKonto': gkonto,
                'Belegnr': belegnr,
                'Belegdatum': belegdatum,
                'Steuercode': steuercode,
                'Buchcode': buchcode,
                'Betrag': betrag,
                'Prozent': prozent,
                'Steuer': steuer,
                'Text': text,
                'Zziel': zziel,
                'Skontopz': skontopz,
                'Skontotage': skontotage
            })
            '''
        pass

    @api.model
    def export_journal_items(self):
        # Get all journal items
        print("==============> Generating csv Files for BMD export")
        # journal_items = self.env['account.move.line'].search([('move_id', '>', 0)])

        result_data = []

        # save every needed field in a variable
        '''for line in journal_items:   #TODO Correct the fields
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

'''

        pass
