import csv
import tkinter as tk
from tkinter import filedialog
import os
import subprocess

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
            for tax in acc.tax_ids:
                result_data.append({
                    'Konto-Nr': acc.code,
                    'Bezeichnung': acc.name,
                    'Ustcode': tax.tax_group_id.id if tax.tax_group_id else '',
                    'USTPz': tax.amount,
                })

        # Create a Tkinter window
        window = tk.Tk()


        #Angepasst von mir an die Allgemeine Directory!
        save_path = self.path + '/Konten.csv'
        directory = os.path.dirname(save_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Write the data to the CSV file
        with open(save_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Konto-Nr', 'Bezeichnung', 'Ustcode', 'USTPz']
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
        print(customers)

        path1= self.path + '/Kunden.csv'
        directory = os.path.dirname(path1)
        if not os.path.exists(directory):
            os.makedirs(directory)


        # Schreibe in die CSV-Datei
        with open(path1, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Name', 'E-Mail', 'Phone','Ort','Straße','PLZ']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

            writer.writeheader()
            for customer in customers:
                writer.writerow({
                    'Name': customer.name,
                    'E-Mail': customer.email,
                    'Phone': customer.phone,
                    'Ort': customer.city,
                    'Straße': customer.street,
                    'PLZ': customer.zip
                })

        return True

    def execute(self):
        self.selectPath()
        self.export_account()
        self.export_customers()
        return True
