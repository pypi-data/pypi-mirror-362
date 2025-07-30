from odoo import models, fields


class EditorialProductPricelist(models.Model):
    """ Extend product pricelist model for editorial management """

    _description = "Editorial Product Pricelist"
    _inherit = 'product.pricelist'

    route_id = fields.Many2one('stock.route', string='Ruta')
    genera_ddaa = fields.Boolean(
        string="Genera derechos de autoría",
        default=lambda self: self.env.company.pricelists_generate_ddaa
    )

    def is_deposit_pricelist(self):
        return self in self.get_deposit_pricelists()

    def get_deposit_pricelists(self):
        # Search for the deposit routes
        # deposit -> customers
        deposit_rules = self.env['stock.rule'].search([
            ('location_src_id', '=', self.env.company.location_venta_deposito_id.id),
            ('location_dest_id', '=', self.env.ref("stock.stock_location_customers").id)
        ])

        if deposit_rules:
            routes = self.env['stock.route'].search([
                ('rule_ids', 'in', deposit_rules.ids)
            ])
            if routes:
                # Search for all the pricelist with deposit route
                pricelists = self.env['product.pricelist'].search([
                    ('route_id', 'in', routes.ids)
                ])
                return pricelists
        return []
