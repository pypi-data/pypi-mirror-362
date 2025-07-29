# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=W0622
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class ApprovalApproval(models.Model):
    _name = "approval.approval"
    _description = "Workflow Policy"

    status = fields.Selection(
        string="Status",
        selection=[
            ("draft", "Draft"),
            ("pending", "Active"),
            ("rejected", "Rejected"),
            ("approved", "Approved"),
        ],
        default="draft",
        help="""Approval status

* Draft: Approval tier still no active
* Active: Approval tier is active
* Rejected: Approval tier is rejected
* Approved: Approval tier is approve""",
    )
    model = fields.Char(
        string="Related Document Model",
        index=True,
    )
    res_id = fields.Integer(
        string="Related Document ID",
        index=True,
    )
    template_id = fields.Many2one(
        string="# Template",
        comodel_name="approval.template",
    )
    template_detail_id = fields.Many2one(
        string="# Template Detail",
        comodel_name="approval.template_detail",
    )
    approver_selection_method = fields.Selection(
        related="template_detail_id.approver_selection_method",
        readonly=True,
    )

    @api.depends(
        "template_detail_id",
    )
    def _compute_approver_user_ids(self):
        for rec in self:
            list_user = []
            if rec.template_detail_id:
                selection_method = rec.approver_selection_method
                user_ids = rec.template_detail_id.approver_user_ids
                if user_ids:
                    list_user += user_ids.ids

                group_ids = rec.template_detail_id.approver_group_ids
                if group_ids:
                    for group in group_ids:
                        list_user += group.users.ids

                if selection_method == "use_python":
                    python_code = rec.template_detail_id.python_code
                    result = rec._evaluate_python_code(python_code)
                    if result:
                        if "user" in result:
                            list_user += result["user"]
                        else:
                            msg_err = "No User defines on python code"
                            raise UserError(_(msg_err))
                rec.approver_user_ids = list(set(list_user))

    approver_user_ids = fields.Many2many(
        string="Users",
        comodel_name="res.users",
        compute="_compute_approver_user_ids",
        store=True,
        help="""Users that can approve/reject document""",
    )

    @api.depends(
        "approver_user_ids",
    )
    def _compute_approver_group_ids(self):
        for rec in self:
            rec.approver_group_ids = rec._get_approver_group_ids()

    def _get_approver_group_ids(self):
        self.ensure_one()
        partner_ids = False
        if self.approver_user_ids:
            partner_ids = self.approver_user_ids.mapped("partner_id")
        return partner_ids.ids

    approver_group_ids = fields.Many2many(
        string="Groups",
        comodel_name="res.groups",
        compute="_compute_approver_group_ids",
    )
    sequence = fields.Integer(
        string="Approval Tier",
    )
    date = fields.Datetime(
        string="Date",
        readonly=True,
        help="Date approve/reject",
    )
    user_id = fields.Many2one(
        string="Approved/Rejected By",
        comodel_name="res.users",
        readonly=True,
    )

    def _get_record(self):
        document_id = self.res_id
        document_model = self.model

        object = self.env[document_model].browse([document_id])[0]
        return object

    def _get_localdict(self):
        return {
            "rec": self._get_record(),
            "env": self.env,
        }

    def _evaluate_python_code(self, python_condition):
        localdict = self._get_localdict()
        result = False
        try:
            safe_eval(
                python_condition, globals_dict=localdict, mode="exec", nocopy=True
            )
            result = localdict
        except Exception:
            msg_err = "Error when execute python code"
            raise UserError(_(msg_err))

        return result

    def get_context(self):
        self.ensure_one()
        result = {}
        return result
