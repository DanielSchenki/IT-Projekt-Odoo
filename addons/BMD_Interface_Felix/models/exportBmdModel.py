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
            #print(line)
            konto = line.account_id.code
            prozent = line.tax_ids.amount
            steuer = line.price_total - line.price_subtotal
            belegdatum = date_formatter(line.move_id.date)
            belegnr = line.move_id.name
            text = line.name
            '''steuercode_before_cut = line.tax_ids.name'''
            #Test String
            steuercode_before_cut = "UST_056 Tax invoiced accepted (§ 11 Abs. 12 und 14, § 16 Abs. 2 sowie gemäß Art. 7 Abs. 4) BMDSC043"
            print(steuercode_before_cut)
            code_digits = steuercode_before_cut[-3:]
            print(code_digits)
            steuercode = int(code_digits)
            print(steuercode)
            if line.debit > 0:
                buchcode = 1
            else:
                buchcode = 2


            #TODO: Add the correct values for the following fields
            satzart = 0
            gkonto = 4000
            buchsymbol = "AR"
            betrag = line.price_total
            kost = 10
            filiale = ""


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
                'Satzart': satzart,
                'Buchsymbol': buchsymbol,
                'Kost': kost,
                'Filiale': filiale
            })

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
