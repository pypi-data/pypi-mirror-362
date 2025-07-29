# Copyright 2017 Tecnativa - Carlos Dauden
# Copyright 2018 Tecnativa - David Vidal
# Copyright 2019 Tecnativa - Pedro M. Baeza
# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import html

from odoo import fields
from odoo.tests import Form, tagged
from odoo.tools import mute_logger

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestAccountInvoiceGroupPicking(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls._create_product(
            name="Product for test",
            type="consu",
            invoice_policy="delivery",
            lst_price=100,
        )
        cls.service = cls._create_product(
            name="Test service product",
            type="service",
            invoice_policy="order",
            lst_price=50,
        )
        order_form = Form(cls.env["sale.order"])
        order_form.partner_id = cls.partner_a
        with order_form.order_line.new() as line_form:
            line_form.product_id = cls.product
            line_form.product_uom_qty = 2
        with order_form.order_line.new() as line_form:
            line_form.product_id = cls.service
            line_form.product_uom_qty = 3
        cls.sale = order_form.save()

    def get_return_picking_wizard(self, picking):
        stock_return_picking_form = Form(
            self.env["stock.return.picking"].with_context(
                active_ids=picking.ids,
                active_id=picking.ids[0],
                active_model="stock.picking",
            )
        )
        return stock_return_picking_form.save()

    def test_account_invoice_group_picking(self):
        # confirm quotation
        self.sale.action_confirm()
        # deliver lines2
        self.sale.picking_ids[:1].action_confirm()
        self.sale.picking_ids[:1].move_line_ids.write({"quantity": 1})
        wiz_act = self.sale.picking_ids[:1].button_validate()
        wiz = Form(
            self.env[wiz_act["res_model"]].with_context(**wiz_act["context"])
        ).save()
        wiz.process()
        # create another sale
        self.sale2 = self.sale.copy()
        self.sale2.order_line[:1].product_uom_qty = 4
        self.sale2.order_line[:1].price_unit = 50.0
        # confirm new quotation
        self.sale2.action_confirm()
        self.sale2.picking_ids[:1].action_confirm()
        self.sale2.picking_ids[:1].move_line_ids.write({"quantity": 1})
        wiz_act = self.sale2.picking_ids[:1].button_validate()
        wiz = Form(
            self.env[wiz_act["res_model"]].with_context(**wiz_act["context"])
        ).save()
        wiz.process()
        sales = self.sale | self.sale2
        # invoice sales
        invoice = sales._create_invoices()
        # Test directly grouping method
        groups = invoice.lines_grouped_by_picking()
        self.assertEqual(len(groups), 4)
        self.assertEqual(groups[0]["picking"], groups[1]["picking"])
        self.assertEqual(groups[2]["picking"], groups[3]["picking"])
        # mix with invoice line that doesn't have neither move_line_ids
        # nor sale_line_ids
        vals = [
            {
                "name": "test invoice line",
                "move_id": invoice.id,
                "price_unit": 10.0,
                "account_id": invoice.invoice_line_ids[0].account_id.id,
            }
        ]
        invoice.invoice_line_ids.create(vals)
        # Test report
        content = html.document_fromstring(
            self.env["ir.actions.report"]._render_qweb_html(
                "account.account_invoices", invoice.id
            )[0]
        )
        tbody = content.xpath("//tbody[@class='invoice_tbody']")
        tbody = [html.tostring(line, encoding="utf-8").strip() for line in tbody][
            0
        ].decode()
        # information about sales is printed
        self.assertEqual(tbody.count(self.sale.name), 1)
        self.assertEqual(tbody.count(self.sale2.name), 1)
        # information about pickings is printed
        self.assertTrue(self.sale.invoice_ids.picking_ids[:1].name in tbody)
        self.assertTrue(self.sale2.invoice_ids.picking_ids[:1].name in tbody)

    @mute_logger("odoo.models.unlink")
    def test_account_invoice_group_picking_return(self):
        self.sale.action_confirm()
        # deliver lines2
        picking = self.sale.picking_ids[:1]
        picking.action_confirm()
        picking.move_line_ids.write({"quantity": 1})
        wiz_act = picking.button_validate()
        wiz = Form(
            self.env[wiz_act["res_model"]].with_context(**wiz_act["context"])
        ).save()
        wiz.process()
        self.sale._create_invoices()
        # Return one picking from sale1
        wiz_return = self.get_return_picking_wizard(picking)
        wiz_return.product_return_moves.quantity = 1
        res = wiz_return.action_create_returns()
        picking_return = self.env["stock.picking"].browse(res["res_id"])
        picking_return.move_line_ids.write({"quantity": 1})
        picking_return.button_validate()
        # Test directly grouping method
        invoice = self.sale._create_invoices(final=True)
        groups = invoice.lines_grouped_by_picking()
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0]["picking"], picking_return)

    @mute_logger("odoo.models.unlink")
    def test_account_invoice_return_without_returned_good(self):
        self.sale.action_confirm()
        picking = self.sale.picking_ids[:1]
        picking.action_confirm()
        picking.move_line_ids.write({"quantity": 1})
        wiz_act = picking.button_validate()
        wiz = Form(
            self.env[wiz_act["res_model"]].with_context(**wiz_act["context"])
        ).save()
        wiz.process()
        invoice = self.sale._create_invoices()
        invoice.action_post()
        # Refund invoice without return picking
        move_reversal = (
            self.env["account.move.reversal"]
            .with_context(active_model="account.move", active_ids=invoice.ids)
            .create(
                {
                    "date": fields.Date.today(),
                    "reason": "no reason",
                    "journal_id": invoice.journal_id.id,
                }
            )
        )
        reversal = move_reversal.refund_moves()
        refund_invoice = self.env["account.move"].browse(reversal["res_id"])
        groups = refund_invoice.lines_grouped_by_picking()
        self.assertEqual(len(groups), 2)

    @mute_logger("odoo.models.unlink")
    def test_account_invoice_group_picking_refund(self):
        # confirm quotation
        self.sale.action_confirm()
        # deliver lines2
        picking = self.sale.picking_ids[:1]
        picking.action_confirm()
        picking.move_line_ids.write({"quantity": 1})
        wiz_act = picking.button_validate()
        wiz = Form(
            self.env[wiz_act["res_model"]].with_context(**wiz_act["context"])
        ).save()
        wiz.process()
        # invoice sales
        invoice = self.sale._create_invoices()
        invoice._post()
        # Test directly grouping method
        # invoice = self.env["account.move"].browse(inv_id)
        groups = invoice.lines_grouped_by_picking()
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0]["picking"], groups[1]["picking"])
        # Test report
        content = html.document_fromstring(
            self.env["ir.actions.report"]._render_qweb_html(
                "account.account_invoices", invoice.id
            )[0]
        )
        tbody = content.xpath("//tbody[@class='invoice_tbody']")
        tbody = [html.tostring(line, encoding="utf-8").strip() for line in tbody][
            0
        ].decode()
        # information about sales is printed
        self.assertEqual(tbody.count(self.sale.name), 1)
        # information about pickings is printed
        self.assertTrue(picking.name in tbody)
        # Return picking
        wiz_return = self.get_return_picking_wizard(picking)
        wiz_return.product_return_moves.quantity = 1
        res = wiz_return.action_create_returns()
        picking_return = self.env["stock.picking"].browse(res["res_id"])
        picking_return.move_line_ids.write({"quantity": 1})
        picking_return.button_validate()
        # Refund invoice
        wiz_invoice_refund = (
            self.env["account.move.reversal"]
            .with_context(active_model="account.move", active_ids=invoice.ids)
            .create(
                {
                    "reason": "test",
                    "journal_id": invoice.journal_id.id,
                }
            )
        )
        wiz_invoice_refund.refund_moves()
        new_invoice = self.sale.invoice_ids.filtered(
            lambda i: i.move_type == "out_refund"
        )
        # Test directly grouping method
        # invoice = self.env["account.move"].browse(inv_id)
        groups = new_invoice.lines_grouped_by_picking()
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0]["picking"], groups[1]["picking"])
        # Test report
        content = html.document_fromstring(
            self.env["ir.actions.report"]._render_qweb_html(
                "account.account_invoices", new_invoice.id
            )[0]
        )
        tbody = content.xpath("//tbody[@class='invoice_tbody']")
        tbody = [html.tostring(line, encoding="utf-8").strip() for line in tbody][
            0
        ].decode()
        # information about sales is printed
        self.assertEqual(tbody.count(self.sale.name), 1)
        # information about pickings is printed
        self.assertTrue(picking_return.name in tbody)

    @mute_logger("odoo.models.unlink")
    def test_account_invoice_group_picking_refund_without_return(self):
        # confirm quotation
        self.sale.action_confirm()
        # deliver lines2
        picking = self.sale.picking_ids[:1]
        picking.action_confirm()
        picking.move_line_ids.write({"quantity": 1})
        wiz_act = picking.button_validate()
        wiz = Form(
            self.env[wiz_act["res_model"]].with_context(**wiz_act["context"])
        ).save()
        wiz.process()
        # invoice sales
        invoice = self.sale._create_invoices()
        invoice._post()
        # Test directly grouping method
        # invoice = self.env["account.move"].browse(inv_id)
        groups = invoice.lines_grouped_by_picking()
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0]["picking"], groups[1]["picking"])
        # Test report
        content = html.document_fromstring(
            self.env["ir.actions.report"]._render_qweb_html(
                "account.account_invoices", invoice.id
            )[0]
        )
        tbody = content.xpath("//tbody[@class='invoice_tbody']")
        tbody = [html.tostring(line, encoding="utf-8").strip() for line in tbody][
            0
        ].decode()
        # information about sales is printed
        self.assertEqual(tbody.count(self.sale.name), 1)
        # information about pickings is printed
        self.assertTrue(picking.name in tbody)
        # Refund invoice
        wiz_invoice_refund = (
            self.env["account.move.reversal"]
            .with_context(active_model="account.move", active_ids=invoice.ids)
            .create(
                {
                    "reason": "test",
                    "journal_id": invoice.journal_id.id,
                }
            )
        )
        wiz_invoice_refund.refund_moves()
        new_invoice = self.sale.invoice_ids.filtered(
            lambda i: i.move_type == "out_refund"
        )
        # Test directly grouping method
        # invoice = self.env["account.move"].browse(inv_id)
        groups = new_invoice.lines_grouped_by_picking()
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0]["picking"], groups[1]["picking"])
        # Test report
        content = html.document_fromstring(
            self.env["ir.actions.report"]._render_qweb_html(
                "account.account_invoices", new_invoice.id
            )[0]
        )
        tbody = content.xpath("//tbody[@class='invoice_tbody']")
        tbody = [html.tostring(line, encoding="utf-8").strip() for line in tbody][
            0
        ].decode()
        # information about sales is printed
        self.assertEqual(tbody.count(self.sale.name), 1)
        # information about pickings is printed
        self.assertTrue(picking.name in tbody)
