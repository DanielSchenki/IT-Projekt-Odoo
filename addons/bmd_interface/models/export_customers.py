from odoo import models, api
import csv
import os


class CustomerExport(models.TransientModel):
    _name = 'customer.export'
    _description = 'Export Customers to CSV'

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
