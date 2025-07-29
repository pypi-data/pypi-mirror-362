from odoo import models, fields, _


class DocumentPage(models.Model):
    _inherit = "document.page"

    ticket_tag_ids = fields.Many2many(
        comodel_name="helpdesk.ticket.tag",
        string="Related ticket tags",
    )

    def look_up_view(self):
        custom_form_view = self.env.ref(
            "helpdesk_ticket_document_pages.document_page_look_up_form_view"
        )
        return {
            "name": _("Document Page"),
            "type": "ir.actions.act_window",
            "res_model": "document.page",
            "res_id": self.id,
            "view_mode": "form",
            "views": [[custom_form_view.id, "form"]],
            "target": "new",
            "flags": {"mode": "readonly"},
            "context": {
                "document_page_ids": self.env.context.get("document_page_ids", [])
            },
        }

    def open_tree_view_target_new(self):
        custom_tree_view = self.env.ref(
            "helpdesk_ticket_document_pages.document_page_tree_new_target"
        )
        custom_form_view = self.env.ref(
            "helpdesk_ticket_document_pages.document_page_look_up_form_view"
        )

        return {
            "name": _("Document Pages"),
            "type": "ir.actions.act_window",
            "res_model": "document.page",
            "view_mode": "tree,form",
            "views": [[custom_tree_view.id, "tree"], [custom_form_view.id, "form"]],
            "target": "new",
            "domain": [("id", "in", self.env.context.get("document_page_ids", []))],
            "context": {
                "document_page_ids": self.env.context.get("document_page_ids", [])
            },
        }
