# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)
from datetime import datetime

import pytz

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class SequenceTemplate(models.Model):
    _name = "sequence.template"
    _description = "Sequence Template"
    _order = "sequence, id"

    DEFAULT_PYTHON_CODE = """# Available variables:
#  - env: Odoo Environment on which the action is triggered.
#  - document: record on which the action is triggered; may be void."""

    @api.model
    def _default_company_id(self):
        return self.env["res.company"]._company_default_get("sequence.template")

    name = fields.Char(
        string="Document Name",
        required=True,
        copy=True,
        help="Name of the sequence template.",
    )
    model_id = fields.Many2one(
        string="Referenced Model",
        comodel_name="ir.model",
        index=True,
        required=True,
        copy=True,
        ondelete="cascade",
        help="Model to which this sequence template refers.",
    )
    model = fields.Char(
        string="Model Technical Name",
        related="model_id.model",
        index=True,
        store=True,
        help="Technical name of the referenced model.",
    )
    company_id = fields.Many2one(
        string="Company Name",
        comodel_name="res.company",
        default=lambda self: self._default_company_id(),
        copy=True,
        help="Company for which this sequence template is applicable.",
    )
    sequence = fields.Integer(
        string="Sequence Order",
        default=5,
        required=True,
        copy=True,
        help="Sequence order for template selection.",
    )
    initial_string = fields.Char(
        string="Initial Sequence String",
        required=True,
        default="/",
        help="Initial string value for the sequence field.",
    )
    sequence_field_id = fields.Many2one(
        string="Sequence Field Name",
        comodel_name="ir.model.fields",
        ondelete="cascade",
        required=True,
        domain="[('model_id', '=', model_id),('ttype','=','char')]",
        help="Field to store the generated sequence value.",
    )
    date_field_id = fields.Many2one(
        string="Sequence Date Field",
        comodel_name="ir.model.fields",
        ondelete="cascade",
        required=True,
        domain="[('model_id', '=', model_id),('ttype','in',['date','datetime'])]",
        help="Date field used for sequence generation.",
    )
    state = fields.Selection(
        string="Sequence State",
        selection=[
            ("draft", "Draft"),
            ("apply", "Sequence Applied"),
        ],
        default="draft",
        help="Status of the sequence template.",
    )
    computation_method = fields.Selection(
        string="Method",
        selection=[
            ("use_domain", "Domain"),
            ("use_python", "Python Code"),
        ],
        default="use_python",
        required=True,
        copy=True,
        help="Method to determine if this template should be applied.",
    )
    domain = fields.Char(
        string="Domain Expression",
        copy=True,
        help="Domain expression to filter applicable records.",
    )
    python_code = fields.Text(
        string="Python Condition Code",
        default=DEFAULT_PYTHON_CODE
        + "\n#  - result: Return result, the value is boolean."
        + "\nresult = True",
        copy=True,
        help="Python code to determine if this template should be applied.",
    )
    sequence_selection_method = fields.Selection(
        string="Selection Method",
        selection=[
            ("use_sequence", "Sequence"),
            ("use_python", "Python Code"),
        ],
        default="use_python",
        required=True,
        copy=True,
        help="Method to select the sequence to use.",
    )
    sequence_id = fields.Many2one(
        string="Sequence Reference",
        comodel_name="ir.sequence",
        help="Sequence to use for generating values.",
    )
    sequence_python_code = fields.Text(
        string="Python Sequence Code",
        default=DEFAULT_PYTHON_CODE
        + "\n#  - sequence: Return sequence, the value is recordset of sequence.",
        copy=True,
        help="Python code to select the sequence to use.",
    )
    add_custom_prefix = fields.Boolean(
        string="Enable Custom Prefix",
        default=False,
        help="Enable to add a custom prefix to the generated sequence.",
    )
    prefix_python_code = fields.Text(
        string="Python Prefix Code",
        default=DEFAULT_PYTHON_CODE
        + "\n#  - result: Return prefix, the value is string.",
        copy=True,
        help="Python code to compute the custom prefix.",
    )
    add_custom_suffix = fields.Boolean(
        string="Enable Custom Suffix",
        default=False,
        help="Enable to add a custom suffix to the generated sequence.",
    )
    suffix_python_code = fields.Text(
        string="Python Suffix Code",
        default=DEFAULT_PYTHON_CODE
        + "\n#  - result: Return suffix, the value is string.",
        copy=True,
        help="Python code to compute the custom suffix.",
    )
    active = fields.Boolean(
        string="Active Document",
        default=True,
        copy=True,
        help="Set inactive to hide this sequence template from selection.",
    )
    note = fields.Text(
        string="Additional Note",
        copy=True,
        help="Additional notes or remarks.",
    )

    @api.onchange(
        "model_id",
    )
    def onchange_sequence_field_id(self):
        self.sequence_field_id = False

    @api.onchange(
        "model_id",
    )
    def onchange_date_field_id(self):
        self.date_field_id = False

    @api.model
    def create_sequence(self, document):
        self.ensure_one()
        result = False
        sequence_date = False
        sequence = self._evaluate_sequence(document)
        if sequence:
            if self.date_field_id:
                sequence_date = getattr(document, self.date_field_id.name)
            result = sequence.with_context(ir_sequence_date=sequence_date).next_by_id()

            if self.add_custom_prefix:
                prefix = self._get_prefix_computation(document, sequence_date)
                result = prefix + result
            if self.add_custom_suffix:
                suffix = self._get_suffix_computation(document, sequence_date)
                result = result + suffix

        return result

    def _get_localdict(self, document):
        self.ensure_one()
        return {
            "env": self.env,
            "document": document,
        }

    def _evaluate_sequence(self, document):
        self.ensure_one()
        if not document:
            return False
        try:
            method_name = "_evaluate_sequence_" + self.sequence_selection_method
            result = getattr(self, method_name)(document)
        except Exception as error:
            msg_err = _(f"Error evaluating conditions.\n {error}")
            raise UserError(msg_err) from error
        return result

    def _evaluate_sequence_use_python(self, document):
        self.ensure_one()
        res = False
        localdict = self._get_localdict(document)
        try:
            safe_eval(self.sequence_python_code, localdict, mode="exec", nocopy=True)
            res = localdict["sequence"]
        except Exception as error:
            raise UserError(_(f"Error evaluating conditions.\n {error}")) from error
        return res

    def _evaluate_sequence_use_sequence(self, document):
        self.ensure_one()
        result = False
        if self.sequence_id:
            result = self.sequence_id
        return result

    def _get_prefix(self, document):
        self.ensure_one()
        res = False
        localdict = self._get_localdict(document)
        try:
            safe_eval(self.prefix_python_code, localdict, mode="exec", nocopy=True)
            res = localdict["result"]
        except Exception as error:
            raise UserError(_(f"Error on get prefix.\n {error}")) from error
        return res

    def _get_suffix(self, document):
        self.ensure_one()
        result = False
        localdict = self._get_localdict(document)
        try:
            safe_eval(self.suffix_python_code, localdict, mode="exec", nocopy=True)
            result = localdict["result"]
        except Exception as error:
            raise UserError(_(f"Error on get suffix.\n {error}")) from error
        return result

    def _interpolate(self, s, d):
        return (s % d) if s else ""

    def _interpolation_dict(self, date=None, date_range=None):
        self.ensure_one()
        now = range_date = effective_date = datetime.now(
            pytz.timezone(self._context.get("tz") or "UTC")
        )
        if date or self._context.get("ir_sequence_date"):
            effective_date = fields.Datetime.to_datetime(
                date or self._context.get("ir_sequence_date")
            )
        if date_range or self._context.get("ir_sequence_date_range"):
            range_date = fields.Datetime.to_datetime(
                date_range or self._context.get("ir_sequence_date_range")
            )

        sequences = {
            "year": "%Y",
            "month": "%m",
            "day": "%d",
            "y": "%y",
            "doy": "%j",
            "woy": "%W",
            "weekday": "%w",
            "h24": "%H",
            "h12": "%I",
            "min": "%M",
            "sec": "%S",
        }
        res = {}
        for key, format_pattern in sequences.items():
            res[key] = effective_date.strftime(format_pattern)
            res["range_" + key] = range_date.strftime(format_pattern)
            res["current_" + key] = now.strftime(format_pattern)

        return res

    def _get_prefix_computation(self, document, date):
        self.ensure_one()
        result = False
        prefix = self._get_prefix(document)

        d = self._interpolation_dict(date_range=date)

        try:
            interpolated_prefix = self._interpolate(prefix, d)
        except Exception as error:
            raise UserError(_(f"Error on convert prefix.\n {error}")) from error

        result = interpolated_prefix
        return result

    def _get_suffix_computation(self, document, date):
        self.ensure_one()
        result = False
        suffix = self._get_suffix(document)

        d = self._interpolation_dict(date_range=date)

        try:
            interpolated_suffix = self._interpolate(suffix, d)
        except Exception as error:
            raise UserError(_(f"Error on convert suffix.\n {error}")) from error

        result = interpolated_suffix
        return result

    def _register_hook(self):
        return True
