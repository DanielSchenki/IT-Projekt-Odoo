from odoo import models, api
import csv
import os


class CustomerExport(models.Model):
    _name = 'customer.export'
    _description = "Exportieren von Kunden"



    def export_bmd(self):
        print("==============> Generating csv Files for BMD export")
        pass
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
