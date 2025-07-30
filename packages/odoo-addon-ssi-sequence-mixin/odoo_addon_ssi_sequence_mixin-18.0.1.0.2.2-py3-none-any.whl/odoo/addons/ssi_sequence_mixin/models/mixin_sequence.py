# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).
from odoo import _, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class MixingSequence(models.AbstractModel):
    _name = "mixin.sequence"
    _description = "Mixin Object for Sequence Policy"

    _fallback_sequence_field = "name"

    def _get_sequence_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    def _evaluate_sequence(self, template):
        self.ensure_one()
        if not template:
            return False
        try:
            method_name = "_evaluate_sequence_" + template.computation_method
            result = getattr(self, method_name)(template)
        except Exception as error:
            msg_err = _(f"Error evaluating conditions.\n {error}")
            raise UserError(msg_err) from error
        return result

    def _evaluate_sequence_use_python(self, template):
        self.ensure_one()
        res = False
        localdict = self._get_sequence_localdict()
        try:
            safe_eval(template.python_code, localdict, mode="exec", nocopy=True)
            res = localdict["result"]
        except Exception as error:
            raise UserError(_(f"Error evaluating conditions.\n {error}")) from error
        return res

    def _evaluate_sequence_use_domain(self, template):
        self.ensure_one()
        result = False
        domain = [("id", "=", self.id)] + safe_eval(template.domain, {})

        count_result = self.search_count(domain)
        if count_result > 0:
            result = True
        return result

    def _get_template_sequence(self):
        result = False
        obj_sequence_template = self.env["sequence.template"]
        criteria = [
            ("model_id.model", "=", str(self._name)),
        ]
        templates = obj_sequence_template.search(
            criteria,
            order="sequence desc",
        )
        for template in templates:
            if self._evaluate_sequence(template):
                result = template
                break
        return result

    def _create_sequence(self):
        self.ensure_one()
        template = self._get_template_sequence()
        if template:
            result = template.initial_string
            if getattr(self, template.sequence_field_id.name) == result:
                result = template.create_sequence(self)
            else:
                result = getattr(self, template.sequence_field_id.name)
            setattr(
                self,
                template.sequence_field_id.name,
                result,
            )
        else:
            error_message = f"""
            Document Type: {self._description.lower()}
            Context: Generate code or document number
            Database ID: {self.id}
            Problem: No sequence template found
            Solution: Create sequence template
            """
            raise UserError(_(error_message)) from None
