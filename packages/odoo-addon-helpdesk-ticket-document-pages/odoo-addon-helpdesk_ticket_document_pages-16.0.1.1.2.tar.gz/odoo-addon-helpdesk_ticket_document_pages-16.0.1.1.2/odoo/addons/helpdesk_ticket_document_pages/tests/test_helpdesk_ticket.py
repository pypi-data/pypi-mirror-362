from odoo.tests import common, tagged


@tagged("post_install", "helpdesk_ticket_document_pages")
class TestHelpdeskTicket(common.TransactionCase):
    def test_open_related_document_pages(self):
        ticket = self.env.ref("helpdesk_mgmt.helpdesk_ticket_3")
        ticket_roaming_tag = self.env["helpdesk.ticket.tag"].create(
            {"name": "Roaming issue"}
        )
        document_page1 = self.env.ref("document_page.demo_page1")
        document_page3 = self.env.ref("document_page.demo_page3")
        custom_tree_view = self.env.ref(
            "helpdesk_ticket_document_pages.document_page_tree_new_target"
        )
        custom_form_view = self.env.ref(
            "helpdesk_ticket_document_pages.document_page_look_up_form_view"
        )

        # Assign ticket tag to ticket
        ticket.tag_ids = [(4, ticket_roaming_tag.id)]

        # Assign ticket tag to document pages
        document_page1.ticket_tag_ids = [(4, ticket_roaming_tag.id)]
        document_page3.ticket_tag_ids = [(4, ticket_roaming_tag.id)]

        action_result = ticket.open_related_document_pages()

        self.assertEqual(action_result["name"], "Document Pages")
        self.assertEqual(action_result["type"], "ir.actions.act_window")
        self.assertEqual(action_result["res_model"], "document.page")
        self.assertEqual(
            action_result["views"],
            [[custom_tree_view.id, "tree"], [custom_form_view.id, "form"]],
        )
        self.assertEqual(
            action_result["domain"],
            [("id", "in", [document_page1.id, document_page3.id])],
        )
