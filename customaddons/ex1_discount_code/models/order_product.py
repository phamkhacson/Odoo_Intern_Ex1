from odoo import fields, api, models


class OrderProduct(models.Model):
    _inherit = "sale.order"
    customer_discount_code = fields.Text(string="Discount code", readonly="1")
    sale_order_discount_estimated = fields.Float(string="Discount Estimated", readonly="1")
    code_valid = fields.Boolean(string="Check Code", readonly="1")

    @api.depends('partner_id', 'order_line.price_total')
    def _amount_all(self):
        self.customer_discount_code = self.partner_id.customer_discount_code
        if not self.customer_discount_code:
            self.customer_discount_code = "NULL"
            self.code_valid = False
            self.sale_order_discount_estimated = 0
            for order in self:
                amount_untaxed = amount_tax = 0.0
                for line in order.order_line:
                    amount_untaxed += line.price_subtotal
                    amount_tax += line.price_tax
                order.update({
                    'amount_untaxed': amount_untaxed,
                    'amount_tax': amount_tax,
                    'amount_total': amount_untaxed + amount_tax,
                })
        else:
            first = self.customer_discount_code[0:4]
            last = self.customer_discount_code[4:len(self.customer_discount_code)]
            if first == "VIP_" and len(last) < 3 and last.isdigit():
                self.code_valid = True
                discount = self.customer_discount_code[4:len(self.customer_discount_code)]
                discount = float(discount)
                for order in self:
                    amount_untaxed = amount_tax = 0.0
                    for line in order.order_line:
                        amount_untaxed += line.price_subtotal
                        amount_tax += line.price_tax
                    order.sale_order_discount_estimated = amount_untaxed * (discount / 100)
                    order.update({
                        'amount_untaxed': amount_untaxed,
                        'amount_tax': amount_tax,
                        'amount_total': amount_untaxed + amount_tax - order.sale_order_discount_estimated,
                    })
            else:
                self.code_valid = False
                self.sale_order_discount_estimated = 0
                for order in self:
                    amount_untaxed = amount_tax = 0.0
                    for line in order.order_line:
                        amount_untaxed += line.price_subtotal
                        amount_tax += line.price_tax
                    order.update({
                        'amount_untaxed': amount_untaxed,
                        'amount_tax': amount_tax,
                        'amount_total': amount_untaxed + amount_tax,
                    })
