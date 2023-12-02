import csv
import tkinter as tk
from tkinter import filedialog
import os

from odoo import models, fields, api


class AccountBmdExport(models.TransientModel):
    _name = 'account.bmd'
    _description = 'BMD Export'

    period_date_from = fields.Date(string="Von:", required=True)
    period_date_to = fields.Date(string="Bis:", required=True)

    path = fields.Char(string="Pfad:", required=False)


    @api.model
    def export_account(self):
        accounts = self.env['account.account'].search([])

        result_data = []
        for acc in accounts:
            if not acc.tax_ids:
                kontoart_mapping = {
                    'asset': 1,
                    'equity': 2,
                    'liability': 2,
                    'expense': 3,
                    'income': 4
                }
                kontoart = kontoart_mapping.get(acc.internal_group, '')
                result_data.append({
                    'Konto-Nr': acc.code,
                    'Bezeichnung': acc.name,
                    'Ustcode': '',
                    'USTPz': '',
                    'Kontoart': kontoart
                })
            else:
                for tax in acc.tax_ids:
                    kontoart_mapping = {
                        'asset': 1,
                        'equity': 2,
                        'liability': 2,
                        'expense': 3,
                        'income': 4
                    }
                    kontoart = kontoart_mapping.get(acc.internal_group, '')
                    result_data.append({
                        'Konto-Nr': acc.code,
                        'Bezeichnung': acc.name,
                        'Ustcode': tax.tax_group_id.id if tax.tax_group_id else '',
                        'USTPz': tax.amount,
                        'Kontoart': kontoart
                    })

        # if len(accounts) != len(result_data):
        #     raise Warning('Steuerklassen sind nicht für alle Sachkonten gepflegt')
        #

        # Create a Tkinter window
        window = tk.Tk()


        #Angepasst von mir an die Allgemeine Directory!
        save_path = self.path + '/Sachkonten.csv'
        directory = os.path.dirname(save_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Write the data to the CSV file
        with open(save_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Konto-Nr', 'Bezeichnung', 'Ustcode', 'USTPz', 'Kontoart']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

            writer.writeheader()
            for row in result_data:
                writer.writerow(row)

        window.destroy()

        return True

    @api.model
    def selectPath(self):
        window = tk.Tk()
        print("selectPath")
        self.path = filedialog.askdirectory()
        window.destroy()


    @api.model
    def export_customers(self):

        customers = self.env['res.partner'].search([])
        #customers = self.env['res.partner'].search([('property_account_receivable_id', '!=', False)])

        print(customers)

        path1= self.path + '/Personenkonten.csv'
        directory = os.path.dirname(path1)
        if not os.path.exists(directory):
            os.makedirs(directory)


        # Schreibe in die CSV-Datei
        with open(path1, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Konto-Nr','Name','Straße','PLZ','Ort','Land','UID-Nummer', 'E-Mail','Webseite', 'Phone','IBAN','Zahlungsziel','Skonto','Skontotage']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

            writer.writeheader()
            for customer in customers:
                writer.writerow({
                    'Konto-Nr': customer.property_account_receivable_id.code if customer.property_account_receivable_id else '',
                    'Name': customer.name if customer.name else '',
                    'E-Mail': customer.email if customer.email else '',
                    'Phone': customer.phone if customer.phone else '',
                    'Ort': customer.city if customer.city else '',
                    'Straße': customer.street if customer.street else '',
                    'PLZ': customer.zip if customer.zip else '',
                    'Webseite': customer.website if customer.website else '',
                    'UID-Nummer': customer.vat if customer.vat else '',
                    'Land': customer.state_id.code if customer.state_id else '',



                })

        return True

    def export_buchungszeilen(self):
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

        save_path = self.path + '/Buchungszeilen.csv'
        directory = os.path.dirname(save_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(save_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Konto', 'GKonto', 'Belegnr', 'Belegdatum', 'Steuercode', 'Buchcode', 'Betrag', 'Prozent', 'Steuer', 'Text', 'Satzart', 'Buchsymbol', 'Kost', 'Filiale']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

            writer.writeheader()
            for row in result_data:
                writer.writerow(row)

        print("==============> Done")


    def execute(self):
        self.selectPath()
        self.export_account()
        self.export_customers()
        self.export_buchungszeilen()
        return True
