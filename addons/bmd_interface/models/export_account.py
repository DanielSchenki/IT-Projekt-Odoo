from odoo import models


class ExportAccount(models.Model):

    def export_account(self):

        accounts = self.env['account.account'].search([])  # Fetch all account.account records

        result_data = []
        for acc in accounts:
            for tax in acc.tax_ids:
                result_data.append({
                    'code': acc.code,
                    'name': acc.name,
                    'tax_group_id': tax.tax_group_id.id if tax.tax_group_id else '',
                    'amount': tax.amount,
                })

        import csv

        with open('output.csv', 'w', newline='') as csvfile:
            fieldnames = ['code', 'name', 'tax_group_id', 'amount']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in result_data:
                writer.writerow(row)
