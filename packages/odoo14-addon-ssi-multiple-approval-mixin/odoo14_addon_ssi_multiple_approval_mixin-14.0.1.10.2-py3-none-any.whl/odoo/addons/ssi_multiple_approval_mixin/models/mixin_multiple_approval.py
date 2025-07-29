# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from inspect import getmembers

from lxml import etree

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval


class MixinMultipleApproval(models.AbstractModel):
    _name = "mixin.multiple_approval"
    _inherit = [
        "mixin.decorator",
    ]
    _description = "Mixin Object for Multiple Approval"

    _approval_state_field = "state"
    _approval_from_state = "draft"
    _approval_to_state = "confirm"
    _approval_cancel_state = "cancel"
    _approval_reject_state = "reject"
    _approval_state = "confirm"
    _after_approved_method = False
    _automatically_insert_view_element = False
    _automatically_insert_multiple_approval_page = True
    _multiple_approval_xpath_reference = "//page[last()]"
    _automatically_insert_approve_button = True
    _automatically_insert_reject_button = True
    _automatically_insert_restart_approval_button = True

    approval_template_id = fields.Many2one(
        string="Approval Template",
        comodel_name="approval.template",
        copy=False,
        help="Approval Configuration",
    )
    approval_ids = fields.One2many(
        string="Approvals",
        comodel_name="approval.approval",
        inverse_name="res_id",
        domain=lambda self: [("model", "=", self._name)],
        auto_join=True,
    )
    approved = fields.Boolean(
        string="Approved",
        compute="_compute_approved_rejected",
        search="_search_approved",
    )
    rejected = fields.Boolean(
        string="Rejected",
        compute="_compute_approved_rejected",
    )
    need_validation = fields.Boolean(
        string="Need Validation",
        compute="_compute_need_validation",
        search="_search_need_validation",
    )
    next_approval_ids = fields.Many2many(
        string="Next Approvals",
        comodel_name="approval.approval",
        compute="_compute_next_approval_ids",
    )
    active_approval_ids = fields.Many2many(
        string="Active Approvals",
        comodel_name="approval.approval",
        compute="_compute_active_approval_ids",
    )
    active_approver_user_ids = fields.Many2many(
        string="Active Users",
        comodel_name="res.users",
        compute="_compute_approver_user_ids",
        search="_search_approver_user_ids",
        help="""Users that can approve/reject document""",
    )
    active_approver_partner_ids = fields.Many2many(
        string="Active Partners",
        comodel_name="res.partner",
        compute="_compute_active_approver_partner_ids",
    )

    @api.depends(
        "approval_ids",
    )
    def _compute_approver_user_ids(self):
        for rec in self:
            rec.active_approver_user_ids = rec.approval_ids.filtered(
                lambda r: r.status == "pending"
            ).mapped("approver_user_ids")

    @api.model
    def _search_approver_user_ids(self, operator, value):
        reviews = self.env["approval.approval"].search(
            [
                ("model", "=", self._name),
                ("approver_user_ids", operator, value),
                ("status", "=", "pending"),
            ]
        )
        return [("id", "in", list(set(reviews.mapped("res_id"))))]

    @api.depends(
        "approval_ids",
        "approval_template_id",
        "approval_template_id.validate_sequence",
    )
    def _compute_active_approver_partner_ids(self):
        for rec in self:
            if rec.approval_template_id.validate_sequence:
                rec.active_approver_partner_ids = (
                    rec._get_approver_partner_ids_by_sequence()
                )
            else:
                rec.active_approver_partner_ids = rec._get_approver_partner_ids()

    def _get_approver_partner_ids(self):
        self.ensure_one()
        partner = False
        if self.approval_ids:
            filter_approval_ids = self.approval_ids.filtered(
                lambda r: r.status in ("pending")
            )
            if filter_approval_ids:
                partner = filter_approval_ids.mapped("approver_user_ids").mapped(
                    "partner_id"
                )
        return partner

    def _get_approver_partner_ids_by_sequence(self):
        self.ensure_one()
        partner = False
        if self.approval_ids:
            filter_approval_ids = self.approval_ids.filtered(
                lambda r: r.status in ("pending")
            )
            if filter_approval_ids:
                sorted_approval_ids = filter_approval_ids.sorted(
                    key=lambda s: s.sequence
                )[0]
                partner = sorted_approval_ids.mapped("approver_user_ids").mapped(
                    "partner_id"
                )
        return partner

    def _compute_approved_rejected(self):
        for rec in self:
            rec.approved = self._get_approvals_approved(rec.approval_ids)
            if rec.state == self._approval_reject_state:
                rec.rejected = True
            else:
                rec.rejected = False

    @api.model
    def _get_approvals_approved(self, approvals):
        if not approvals:
            return False
        return not any([s != "approved" for s in approvals.mapped("status")])

    @api.model
    def _get_approvals_rejected(self, approvals):
        if not approvals:
            return False
        for rec in approvals:
            if rec.status == "rejected":
                return True

    def _prepare_domain_need_validation(self):
        self.ensure_one()
        domain = [
            ("model", "=", self._name),
        ]
        return domain

    def _compute_need_validation(self):
        for rec in self:
            result = False
            if rec.state == self._approval_state and not rec.approval_template_id:
                result = True
            rec.need_validation = result

    @api.depends(
        "approval_ids",
    )
    def _compute_next_approval_ids(self):
        for rec in self:
            rec.next_approval_ids = rec.approval_ids.filtered(
                lambda r: r.status == "draft"
            )
            if (
                rec.approval_template_id.validate_sequence
                and len(rec.next_approval_ids) > 0
            ):
                rec.next_approval_ids = rec.next_approval_ids[0]

    @api.depends(
        "approval_ids",
    )
    def _compute_active_approval_ids(self):
        for rec in self:
            rec.active_approval_ids = rec.approval_ids.filtered(
                lambda r: r.status == "pending"
            )

    @api.model
    def _search_approved(self, operator, value):
        rec = self.search([])
        if operator == "=":
            rec = rec.filtered(lambda r: r.approval_ids and r.rejected == value)
        else:
            rec = rec.filtered(lambda r: r.approval_ids and r.rejected != value)
        return [("id", "in", rec.ids)]

    @api.model
    def _search_validated(self, operator, value):
        assert operator in ("=", "!="), "Invalid domain operator"
        assert value in (True, False), "Invalid domain value"
        pos = self.search(
            [(self._approval_state_field, "in", self._approval_from_state)]
        ).filtered(lambda r: r.approval_ids and r.approved == value)
        return [("id", "in", pos.ids)]

    @api.model
    def _search_need_validation(self, operator, value):
        rec = self.search([])
        if operator == "=":
            rec = rec.filtered(lambda r: r.approval_ids and r.need_validation == value)
        else:
            rec = rec.filtered(lambda r: r.approval_ids and r.need_validation != value)
        return [("id", "in", rec.ids)]

    def _get_approval_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    def _evaluate_approval(self, template):
        self.ensure_one()
        if not template:
            return False
        try:
            method_name = "_evaluate_approval_" + template.computation_method
            result = getattr(self, method_name)(template)
        except Exception as error:
            msg_err = _("Error evaluating approval conditions.\n %s") % error
            raise UserError(msg_err)
        return result

    def _evaluate_approval_use_python(self, template):
        self.ensure_one()
        res = False
        localdict = self._get_approval_localdict()
        try:
            safe_eval(template.python_code, localdict, mode="exec", nocopy=True)
            res = localdict["result"]
        except Exception as error:
            raise UserError(_("Error evaluating conditions.\n %s") % error)
        return res

    def _evaluate_approval_use_domain(self, template):
        self.ensure_one()
        result = False
        domain = [("id", "=", self.id)] + safe_eval(template.domain, {})

        count_result = self.search_count(domain)
        if count_result > 0:
            result = True
        return result

    @api.model
    def _get_under_approval_exceptions(self):
        fields = [
            "message_last_post",
            "message_follower_ids",
        ]
        return fields

    def _check_allow_write_under_approval(self, vals):
        exceptions = self._get_under_approval_exceptions()
        for val in vals:
            if val not in exceptions:
                return False
        return True

    def set_active(self, approver):
        self.ensure_one()
        if approver and self.approval_template_id:
            approver_ids = approver.filtered(lambda r: r.status == "draft")
            if self.approval_template_id.validate_sequence and len(approver_ids) > 0:
                approver_ids = approver_ids[0]
            approver_ids.write({"status": "pending"})

    def _action_approval(self, state):
        self.ensure_one()
        approval_ids = self.active_approval_ids
        user_approves = approval_ids.filtered(
            lambda r: self.env.user.id in r.approver_user_ids.ids
        )
        if user_approves:
            user_approves.write(
                {
                    "status": state,
                    "date": fields.Datetime.now(),
                    "user_id": self.env.user.id,
                }
            )
            if state == "approved":
                self.set_active(self.next_approval_ids)
                self._notify_approve_action()
            elif state == "rejected":
                self.write({"state": "reject"})

    def _notify_approve_action(self):
        self.ensure_one()
        msg = self._prepare_approve_action_notification()
        self.message_post(
            body=_(msg), message_type="notification", subtype_xmlid="mail.mt_note"
        )

    def _prepare_approve_action_notification(self):
        self.ensure_one()
        msg = "%s %s approved" % (self._description, self.display_name)
        return msg

    def _check_all_approve(self):
        self.ensure_one()
        result = True
        for approval in self.approval_ids:
            if approval.status != "approved":
                result = False
                break
        return result

    def _run_pre_approve_check(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_pre_approve_check"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def _run_post_approve_check(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_post_approve_check"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def _run_pre_approve_action(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_pre_approve_action"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def _run_post_approve_action(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_post_approve_action"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def action_approve_approval(self):
        for rec in self.sudo():
            rec._check_approve_policy()
            rec._run_pre_approve_check()
            rec._run_pre_approve_action()
            rec._action_approval("approved")
            if rec._check_all_approve() and self._after_approved_method:
                getattr(
                    rec.with_context(bypass_policy_check=True),
                    self._after_approved_method,
                )()
            rec._run_post_approve_check()
            rec._run_post_approve_action()

    def _check_approve_policy(self):
        self.ensure_one()

        if not self._automatically_insert_approve_button:
            return True

        if self.env.context.get("bypass_policy_check", False):
            return True

        if not self.approve_ok:
            error_message = """
            Context: Approve %s
            Database ID: %s
            Problem: Document is not allowed to approve
            Solution: Check approve policy prerequisite
            """ % (
                self._description.lower(),
                self.id,
            )
            raise UserError(_(error_message))

    def _run_pre_reject_check(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_pre_reject_check"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def _run_post_reject_check(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_post_reject_check"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def _run_pre_reject_action(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_pre_reject_action"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def _run_post_reject_action(self):
        self.ensure_one()
        cls = type(self)
        methods = []
        for _attr, func in getmembers(cls):
            if self.is_decorator(func, "_post_reject_action"):
                methods.append(func)
        if methods:
            self.run_decorator_method(methods)

    def action_reject_approval(self):
        for rec in self.sudo():
            rec._check_reject_policy()
            rec._run_pre_reject_check()
            rec._run_pre_reject_action()
            rec._action_approval("rejected")
            rec._run_post_reject_check()
            rec._run_post_reject_action()
            rec._notify_reject_action()

    def _notify_reject_action(self):
        self.ensure_one()
        msg = self._prepare_reject_action_notification()
        self.message_post(
            body=_(msg), message_type="notification", subtype_xmlid="mail.mt_note"
        )

    def _prepare_reject_action_notification(self):
        self.ensure_one()
        msg = "%s %s rejected" % (self._description, self.display_name)
        return msg

    def _check_reject_policy(self):
        self.ensure_one()

        if not self._automatically_insert_reject_button:
            return True

        if self.env.context.get("bypass_policy_check", False):
            return True

        if not self.reject_ok:
            error_message = """
            Context: Reject %s
            Database ID: %s
            Problem: Document is not allowed to reject
            Solution: Check reject policy prerequisite
            """ % (
                self._description.lower(),
                self.id,
            )
            raise UserError(_(error_message))

    def _check_restart_approval_policy_policy(self):
        self.ensure_one()

        if not self._automatically_insert_restart_approval_button:
            return True

        if self.env.context.get("bypass_policy_check", False):
            return True

        if not self.restart_approval_ok:
            error_message = """
            Context: Restart approval %s
            Database ID: %s
            Problem: Document is not allowed to restart approval
            Solution: Check restart approval policy prerequisite
            """ % (
                self._description.lower(),
                self.id,
            )
            raise UserError(_(error_message))

    def action_reload_approval_template(self):
        for rec in self.sudo():
            rec._check_restart_approval_policy_policy()
            rec.mapped("approval_ids").unlink()
            rec.mapped("active_approver_partner_ids").unlink()
            rec.action_request_approval()

    def action_reload_approval(self):
        for rec in self.sudo():
            rec._reload_approval()

    def _reload_approval(self):
        self.ensure_one()
        if self.approval_template_id:
            template = self.approval_template_id
            allowed_details = template.detail_ids
            self.approval_ids.filtered(
                lambda r: r.template_detail_id.id not in allowed_details.ids
            ).unlink()
            to_be_added = template.detail_ids - self.approval_ids.mapped(
                "template_detail_id"
            )
            for detail in to_be_added:
                approver_ids = self.approval_ids.create(
                    {
                        "res_id": self.id,
                        "model": self._name,
                        "template_id": self.approval_template_id.id,
                        "template_detail_id": detail.id,
                        "sequence": detail.sequence,
                    }
                )
                self.set_active(approver_ids)
        else:
            self.approval_ids.unlink()

    def write(self, vals):
        for rec in self:
            if (
                vals.get(self._approval_state_field) == self._approval_state
                and getattr(rec, self._approval_state_field)
                == self._approval_from_state
            ):
                if rec.need_validation:
                    rec.action_request_approval()
            if (
                rec.approval_ids
                and getattr(rec, self._approval_state_field)
                in self._approval_from_state
                and not vals.get(self._approval_state_field)
                in (
                    [
                        self._approval_to_state,
                        self._approval_cancel_state,
                        self._approval_reject_state,
                    ]
                )
                and not self._check_allow_write_under_approval(vals)
            ):
                raise ValidationError(_("The operation is under approval process."))
        if vals.get(self._approval_state_field) == self._approval_from_state:
            self.mapped("approval_ids").unlink()
            self.mapped("active_approver_partner_ids").unlink()
            self.sudo().approval_template_id = False
        return super().write(vals)

    def action_request_approval(self):
        obj_approval_template = self.env["approval.template"]
        approver_ids = False
        for rec in self.sudo():
            if rec.approval_template_id:
                if self._evaluate_approval(rec.approval_template_id):
                    rec.write({"approval_template_id": rec.approval_template_id.id})
                else:
                    rec.write({"approval_template_id": False})
            if not rec.approval_template_id:
                criteria_definition = [
                    ("model", "=", self._name),
                ]
                template_ids = obj_approval_template.search(
                    criteria_definition,
                    order="sequence desc",
                )
                if template_ids:
                    for template in template_ids:
                        if self._evaluate_approval(template):
                            rec.write({"approval_template_id": template.id})
                            break
            approver_ids = rec.create_approver()
            rec.set_active(approver_ids)
        return approver_ids

    def create_approver(self):
        self.ensure_one()
        obj_approval_template_detail = self.env["approval.template_detail"]
        obj_approval_approval = created_trs = self.env["approval.approval"]
        sequence = 0

        criteria_approval = [("template_id", "=", self.approval_template_id.id)]
        approver_ids = obj_approval_template_detail.search(
            criteria_approval, order="sequence"
        )
        if approver_ids:
            for approver in approver_ids:
                sequence += 1
                created_trs += obj_approval_approval.create(
                    {
                        "model": self._name,
                        "res_id": self.id,
                        "template_id": self.approval_template_id.id,
                        "template_detail_id": approver.id,
                        "sequence": sequence,
                    }
                )
        return created_trs

    def unlink(self):
        for rec in self:
            rec.mapped("approval_ids").unlink()
        return super().unlink()

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        res = super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )
        if view_type == "form" and self._automatically_insert_multiple_approval_page:
            doc = etree.XML(res["arch"])
            node_xpath = doc.xpath(self._multiple_approval_xpath_reference)
            str_element = self.env["ir.qweb"]._render(
                "ssi_multiple_approval_mixin.multiple_approval"
            )
            for node in node_xpath:
                new_node = etree.fromstring(str_element)
                node.addnext(new_node)

            View = self.env["ir.ui.view"]

            if view_id and res.get("base_model", self._name) != self._name:
                View = View.with_context(base_model_name=res["base_model"])
            new_arch, new_fields = View.postprocess_and_fields(doc, self._name)
            res["arch"] = new_arch
            new_fields.update(res["fields"])
            res["fields"] = new_fields
        return res
