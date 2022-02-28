from odoo import api, models, fields


class Customer(models.Model):
    _inherit = "res.partner"
    customer_discount_code = fields.Text(string="Discount code")
    code_valid = fields.Boolean(string="Check Code", readonly='1')

    # Check valid code
    @api.onchange('customer_discount_code')
    def _check_customer_valid(self):
        if not self.customer_discount_code:
            return {}
        else:
            first = self.customer_discount_code[0:4]
            last = self.customer_discount_code[4:len(self.customer_discount_code)]
            if first == "VIP_" and len(last) < 3 and last.isdigit():
                self.code_valid = True
            else:
                self.code_valid = False

    def update_selected_cus_code(self):
        customers = self.env['res.partner'].browse(self.env.context.get('active_ids', []))
        view_form_id = self.env.ref('ex1_discount_code.update_cus_code_view').id
        return {
            'name': 'Update Customer Discount Code',
            'view_mode': 'form',
            'res_model': 'update_cus_code',
            'views': [(view_form_id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_customer_ids': customers.ids
            }
        }



