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

        # Prompt the user to choose the save path
        save_path = filedialog.asksaveasfilename(defaultextension='.csv')

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
    def export_customers(self):

        customers = self.env['res.partner'].search([('customer_rank', '>', 0)])

        path = "/path/to/export.csv"

        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Schreibe in die CSV-Datei
        with open(path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'email', 'phone']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for customer in customers:
                writer.writerow({
                    'name': customer.name,
                    'email': customer.email,
                    'phone': customer.phone
                })

        return True

    def execute(self):
        self.export_account()
        #self.export_customers()
        return True
