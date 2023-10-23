import csv
from odoo import api, models


class CustomerExport(models.TransientModel):
    _name = 'customer.export'

    @api.model
    def export_customers(self):
        # Get customer data
        customers = self.env['res.partner'].search([('customer', '=', True)])

        # Specify the path for CSV
        path = "/path/to/export.csv"

        # Write to CSV
        with open(path, 'w', newline='') as csvfile:
            fieldnames = ['name', 'email', 'phone']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for customer in customers:
                writer.writerow({'name': customer.name, 'email': customer.email, 'phone': customer.phone})
