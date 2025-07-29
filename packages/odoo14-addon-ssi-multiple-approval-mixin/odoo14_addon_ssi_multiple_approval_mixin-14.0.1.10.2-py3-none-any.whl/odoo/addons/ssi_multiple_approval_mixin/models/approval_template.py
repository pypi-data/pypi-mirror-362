# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import test_python_expr


class ApprovalTemplate(models.Model):
    _name = "approval.template"
    _description = "Approval Template"
    _order = "sequence"

    DEFAULT_PYTHON_CODE = """# Available variables:
#  - env: Odoo Environment on which the action is triggered.
#  - document: record on which the action is triggered; may be void."""

    @api.model
    def _default_company_id(self):
        return self.env["res.company"]._company_default_get("approval.template")

    name = fields.Char(
        string="Name",
        required=True,
    )
    model_id = fields.Many2one(
        string="Referenced Model",
        comodel_name="ir.model",
        index=True,
        required=True,
        ondelete="cascade",
    )
    model = fields.Char(
        related="model_id.model",
        index=True,
        store=True,
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        default=lambda self: self._default_company_id(),
    )
    sequence = fields.Integer(
        default=1,
    )
    active = fields.Boolean(
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
    validate_sequence = fields.Boolean(
        string="Approval by Sequence",
        help="Approval by reviewer must be done by sequence.",
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="approval.template_detail",
        inverse_name="template_id",
        copy=True,
    )
    computation_method = fields.Selection(
        string="Computation Method",
        selection=[
            ("use_domain", "Domain"),
            ("use_python", "Python Code"),
        ],
        default="use_python",
        required=True,
    )
    domain = fields.Char(
        string="Domain",
    )
    python_code = fields.Text(
        string="Python Code",
        default=DEFAULT_PYTHON_CODE
        + "\n#  - result: Return result, the value is boolean.",
        copy=True,
    )

    def name_get(self):
        result = []
        for record in self:
            name = "[{}] {}".format(record.model, record.name)
            result.append((record.id, name))
        return result

    @api.constrains(
        "python_code",
    )
    def _check_python_code(self):
        for action in self.sudo().filtered("python_code"):
            msg = test_python_expr(expr=action.python_code.strip(), mode="exec")
            if msg:
                msg1 = "Template:\n"
                raise ValidationError(msg1 + msg)
