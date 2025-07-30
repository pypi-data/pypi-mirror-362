# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html)

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PrintDcoumentType(models.Model):
    _name = "print_document_type"
    _inherit = [
        "mail.activity.mixin",
        "mail.thread",
    ]
    _description = "Print Document Type"

    name = fields.Char(
        string="Document Name",
        required=True,
        help="Name of the print document type.",
    )
    code = fields.Char(
        string="Document Code",
        default="/",
        required=True,
        help="Unique code for the print document type."
        "Use '/' for auto-generated code.",
    )
    model_id = fields.Many2one(
        string="Referenced Model",
        comodel_name="ir.model",
        index=True,
        required=True,
        ondelete="cascade",
        help="Model to which this print document type refers.",
    )
    model = fields.Char(
        string="Model Technical Name",
        related="model_id.model",
        index=True,
        store=True,
        help="Technical name of the referenced model.",
    )
    report_ids = fields.Many2many(
        string="Reports",
        comodel_name="ir.actions.report",
        relation="rel_print_document_type_2_report",
        column1="type_id",
        column2="report_id",
        domain="[('model', '=', model)]",
        help="Reports associated with this print document type.",
    )
    active = fields.Boolean(
        string="Active Document",
        default=True,
        help="Set inactive to hide this print document type from selection.",
    )
    note = fields.Text(
        string="Additional Note",
        help="Additional notes or remarks.",
    )

    @api.returns("self", lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        if "code" not in default:
            default["code"] = _(f"{self.code} (copy)")
        return super().copy(default=default)

    @api.constrains("code")
    def _check_duplicate_code(self):
        for record in self:
            criteria = [
                ("code", "=", record.code),
                ("id", "!=", record.id),
                ("code", "!=", "/"),
            ]
            count_duplicate = self.search_count(criteria)
            if count_duplicate > 0:
                error_message = (
                    f"Document Type: {self._description.lower()}\n"
                    f"Context: Create or update document\n"
                    f"Database ID: {self.id}\n"
                    "Problem: Dupilicate code\n"
                    "Solution: Change code"
                )
                raise UserError(error_message) from None

    def action_generate_code(self):
        for record in self.sudo():
            record._create_sequence()

    def action_reset_code(self):
        for record in self.sudo():
            record.write(
                {
                    "code": "/",
                }
            )
