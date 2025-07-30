# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html)

from odoo import fields, models
from odoo.tools.safe_eval import safe_eval


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    print_document_type_ids = fields.Many2many(
        string="Reports",
        comodel_name="print_document_type",
        relation="rel_print_document_type_2_report",
        column1="report_id",
        column2="type_id",
        domain="[('model', '=', model)]",
        help="Select the print document types associated with this report.",
    )
    print_python_code = fields.Text(
        string="Condition",
        help="""Python code to determine if the report should be available.
The result of executing the expression must be a boolean.
Available locals: document (current recordset).""",
        default="""
# Available locals:\n#  - document: current recordset\nresult = True""",
    )
    print_multi = fields.Boolean(
        string="Multiple Records",
        default=False,
        help="Enable to allow printing for multiple records at once.",
    )

    def _get_print_localdict(self, document):
        self.ensure_one()
        return {
            "env": self.env,
            "document": document,
        }

    def _evaluate_print_python_code(self, document):
        self.ensure_one()
        result = False
        localdict = self._get_print_localdict(document)
        try:
            safe_eval(self.print_python_code, localdict, mode="exec", nocopy=True)
            result = localdict.get("result", False)
        except Exception:
            result = False
        return result
