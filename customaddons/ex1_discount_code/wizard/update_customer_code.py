from odoo import api, models, fields
from odoo.exceptions import AccessError

class UpdateCustomerCode(models.TransientModel):
    _name = "update_cus_code"
    update_code = fields.Text(string="Update Code")
    customer_ids = fields.Many2many('res.partner', string="customer")

    def update_selected_cus_code(self):
        for customer in self.customer_ids:
            customer.customer_discount_code = self.update_code
            if not customer.customer_discount_code:
                return {}
            else:
                first = customer.customer_discount_code[0:4]
                last = customer.customer_discount_code[4:len(customer.customer_discount_code)]
                if first == "VIP_" and len(last) < 3 and last.isdigit():
                    customer.code_valid = True
                else:
                    raise AccessError("Invalid discount code")
                    customer.code_valid = False