# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import test_python_expr


class ApprovalTemplateDetail(models.Model):
    _name = "approval.template_detail"
    _description = "Approval Template Detail"
    _order = "sequence"

    template_id = fields.Many2one(
        string="# Template",
        comodel_name="approval.template",
        ondelete="cascade",
    )
    company_id = fields.Many2one(
        related="template_id.company_id",
        store=True,
    )
    sequence = fields.Integer(
        default=1,
    )
    active = fields.Boolean(
        default=True,
    )
    approver_selection_method = fields.Selection(
        string="Approval Method",
        selection=[
            ("use_user", "Users"),
            ("use_group", "Groups"),
            ("use_both", "Both specific user and group."),
            ("use_python", "Python Code"),
        ],
        default="use_user",
        required=True,
    )
    approver_user_ids = fields.Many2many(
        string="Users",
        comodel_name="res.users",
        relation="rel_template_detail_2_user",
        column1="detail_id",
        column2="user_id",
    )
    approver_group_ids = fields.Many2many(
        string="Groups",
        comodel_name="res.groups",
        relation="rel_template_detail_2_group",
        column1="detail_id",
        column2="group_id",
    )
    python_code = fields.Text(
        string="Python Code",
        default="""# Available locals:\n#  - rec: current record""",
    )

    @api.constrains(
        "python_code",
    )
    def _check_python_code(self):
        for action in self.sudo().filtered("python_code"):
            msg = test_python_expr(expr=action.python_code.strip(), mode="exec")
            if msg:
                msg1 = "Template Detail:\n"
                raise ValidationError(msg1 + msg)
