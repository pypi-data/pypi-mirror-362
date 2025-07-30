from odoo import models, fields, api, exceptions


class EditorialPurchaseOrder(models.Model):
    """ Extend purchase.order template for editorial management """
    _description = "Editorial Purchase Order"
    _inherit = 'purchase.order'  # odoo/addons/purchase/models/purchase.py

    available_products = fields.Many2many('product.product', string='Productos disponibles', compute='_compute_available_products')
    is_ddaa_order = fields.Boolean(string='Es albarán de autoría', default=False)

    # Calculates the products that can be added to the purchase order according to the provider.
    @api.onchange('partner_id')
    def _compute_available_products(self):
        if self.partner_id:
            domain = [
                        '|',
                        ('seller_ids.partner_id', '=', self.partner_id.id),
                        ('limited_visibility_by_provider', '=', False)
                    ]
        else:
            domain = [('limited_visibility_by_provider', '=', False)]
        self.available_products = self.env['product.product'].search(domain)

    @api.onchange('partner_id')
    def _set_default_purchase_type(self):
        if self.partner_id.default_purchase_type.id:
            self.picking_type_id = self.partner_id.default_purchase_type
        else:
            self.picking_type_id = self._default_picking_type()

    # Prevents products with type "Service" from being purchased by "Compra en depósito" 
    def button_confirm(self):
        if self.picking_type_id.id == self.env.company.stock_picking_type_compra_deposito_id.id:
            service_products = []
            for line in self.order_line:
                product = line.product_id
                if product.type == 'service':
                    service_products.append(product.name)

            if len(service_products) > 0:
                msg = "Los productos con tipo 'Servicio' no pueden ser vendidos mediante compra en depósito. Por favor, selecciona compra en firme o elimina de tu pedido los siguientes productos:"
                for product in service_products:
                    msg += "\n* " + str(product)
                raise exceptions.UserError(msg)

        return super().button_confirm()

    def update_ddaa_order_book_line(self, product, action, value, transfer_name=None):
        """
        Updates the line of books delivered to authorship according to the specified action.

        :param product: (product.template)
        :param action: ('update_price' or 'update_qty')
        :param value: New price or qty to update
        :param transfer_name: (optional, only for qty update from op "Deliver books to authorship")
        """
        ddaa_product = product.derecho_autoria.product_variant_id
        ddaa_product_line = self.order_line.filtered(lambda line: line.product_id.id == ddaa_product.id)
        if not ddaa_product_line:
            raise exceptions.UserError(
                f"No se encuentra la línea de libros entregados autoría para: {product.name}. \
                \nDebes crear el albarán de autoría para este producto primero."
            )

        sequence_for_books_delivered_to_authorship = ddaa_product_line.sequence + 1
        books_delivered_to_authorship_line = self.order_line.filtered(
            lambda line: line.sequence == sequence_for_books_delivered_to_authorship
        )
        if not books_delivered_to_authorship_line:
            raise exceptions.UserError(
                f"No se encuentra la línea de libros entregados autoría para: {product.name}. \
                \nDebes crear el albarán de autoría para este producto primero."
            )

        if action == 'update_price':
            books_delivered_to_authorship_line.price_unit = value
            self.message_post(
                body=f"Se ha modificado el precio del producto: {product.name} para esta autoría. "
                    f"Su nuevo precio es: {value}",
                message_type='comment',
                subtype_xmlid='mail.mt_note'
            )
        elif action == 'update_qty':
            books_delivered_to_authorship_line.product_qty += value
            self.message_post(
                body=f"Se han entregado a autoría {value} unidades de {product.name}. "
                    f"Referencia de la transferencia: {transfer_name}",
                message_type='comment',
                subtype_xmlid='mail.mt_note'
            )

class EditorialPurchaseOrderLine(models.Model):
    """ Extend purchase.order.line template for editorial management """

    _description = "Editorial Purchase Order Line"
    _inherit = 'purchase.order.line' # odoo/addons/purchase/models/purchase.py

    product_barcode = fields.Char(string='Código de barras / ISBN', related='product_id.barcode', readonly=True)
    liquidated_qty = fields.Float(string='Liquidated', default=0.0)
    is_liquidated = fields.Boolean(string='Esta liquidado', default=False)

    @api.onchange('sequence')
    def _on_change_sequence_ddaa_order_line(self):
        if self.env.company.module_editorial_ddaa and self.order_id.is_ddaa_order:
            if self.product_id.product_tmpl_id.categ_id == self.env.company.product_category_ddaa_id:
                raise exceptions.UserError(
                    "No puedes modificar el orden de las líneas del albarán de autoría. Descarta los cambios."
                )

    @api.constrains('qty_received')
    def _onchange_qty_received(self):
        for record in self:
            if record.order_id.picking_type_id.id == self.env.company.stock_picking_type_compra_deposito_id.id:
                record.update({'is_liquidated': record.liquidated_qty >= record.qty_received})

            # liquidated_qty siempre sera igual a qty_received si es una compra en firme
            else:
                if record.qty_received != record.liquidated_qty:
                    record.write({'liquidated_qty': record.qty_received})
                record.write({'is_liquidated': True})

    @api.constrains('liquidated_qty')
    def _update_liquidated_qty(self):
        for record in self:
            record.write({'is_liquidated': record.liquidated_qty >= record.qty_received})
