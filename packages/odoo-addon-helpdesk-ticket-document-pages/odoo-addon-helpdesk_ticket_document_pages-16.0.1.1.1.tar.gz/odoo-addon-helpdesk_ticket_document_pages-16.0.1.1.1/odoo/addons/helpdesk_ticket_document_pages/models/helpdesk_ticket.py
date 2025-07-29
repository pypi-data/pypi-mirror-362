from odoo import models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    def open_related_document_pages(self):
        document_page_ids = self.env["document.page"].search(
            [
                ("ticket_tag_ids", "in", self.tag_ids.ids),
            ]
        )
        return (
            self.env["document.page"]
            .with_context(document_page_ids=document_page_ids.ids)
            .open_tree_view_target_new()
        )
