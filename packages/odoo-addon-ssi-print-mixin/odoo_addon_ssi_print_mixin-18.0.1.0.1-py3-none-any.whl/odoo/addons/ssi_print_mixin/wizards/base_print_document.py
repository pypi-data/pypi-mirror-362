# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html)

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class BasePrintDocument(models.TransientModel):
    _name = "base.print_document"
    _description = "Select Report To Print"

    @api.model
    def _compute_allowed_type_ids(self):
        result = []
        print_multi = self.env.context.get("print_multi")
        obj_print_document_type = self.env["print_document_type"]
        active_model = self.env.context.get("active_model", "")
        criteria = [("model_id.model", "=", active_model)]
        type_ids = obj_print_document_type.search(criteria)
        if type_ids:
            if not print_multi:
                result = type_ids.filtered(lambda x: x.report_ids).ids
            else:
                result = type_ids.filtered(
                    lambda x: x.report_ids.filtered(lambda x: x.print_multi)
                ).ids
        return result

    allowed_type_ids = fields.Many2many(
        string="Allowed Print Types",
        comodel_name="print_document_type",
        default=lambda self: self._compute_allowed_type_ids(),
        relation="rel_print_document_2_print_type",
        column1="wizard_id",
        column2="type_id",
    )

    @api.model
    def _default_type_id(self):
        result = self._compute_allowed_type_ids()
        return result and result[0] or False

    type_id = fields.Many2one(
        string="Type",
        comodel_name="print_document_type",
        default=lambda self: self._default_type_id(),
    )

    @api.depends(
        "type_id",
    )
    def _compute_allowed_print_action_ids(self):
        result = []
        report_ids = []
        obj_action_report = self.env["ir.actions.report"]
        active_model = self.env.context.get("active_model", "")
        print_multi = self.env.context.get("print_multi")
        for record in self:
            if record.type_id:
                report_ids = record.type_id.report_ids
                if report_ids:
                    report_ids = report_ids.filtered(
                        lambda x: x.model_id.model == active_model
                    )
            else:
                criteria = [("model_id.model", "=", active_model)]
                report_ids = obj_action_report.search(criteria)

            if report_ids:
                if print_multi:
                    report_ids = report_ids.filtered(lambda x: x.print_multi)
                recordset = record._get_recordset()
                for report in report_ids:
                    allowed_print = record._check_allowed_print(report)
                    policy = report._evaluate_print_python_code(recordset)
                    if allowed_print and policy:
                        result.append(report.id)
            record.allowed_print_action_ids = result

    allowed_print_action_ids = fields.Many2many(
        string="Allowed Print Action",
        comodel_name="ir.actions.report",
        compute="_compute_allowed_print_action_ids",
        relation="rel_print_document_2_action_report",
        column1="wizard_id",
        column2="report_action_id",
    )

    report_action_id = fields.Many2one(
        string="Report Template",
        comodel_name="ir.actions.report",
    )

    def _check_allowed_print(self, recordset):
        result = False
        user = self.env.user
        is_superuser = self.env.is_superuser()
        if is_superuser:
            result = True
        if recordset.groups_id:
            user_group_ids = user.groups_id.ids
            if set(recordset.groups_id.ids) & set(user_group_ids):
                result = True
        else:
            result = True
        return result

    def _get_recordset(self):
        self.env.context.get("active_id", False)
        active_ids = self.env.context.get("active_ids", False)
        active_model = self.env.context.get("active_model", "")
        self.env.context.get("print_multi")
        # TODO: Assert when invalid active_id or active_model
        result = self.env[active_model].browse(active_ids)
        return result

    def action_print(self):
        if self.report_action_id:
            recordset = self._get_recordset()
            report_action = self.report_action_id.report_action(recordset)
            report_action.update({"close_on_report_download": True})
            return report_action
        else:
            raise UserError(_("No Report Selected"))
