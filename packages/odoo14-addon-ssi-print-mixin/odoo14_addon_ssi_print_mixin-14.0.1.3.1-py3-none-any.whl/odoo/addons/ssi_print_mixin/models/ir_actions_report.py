# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval, test_python_expr


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    print_document_type_ids = fields.Many2many(
        string="Reports",
        comodel_name="print_document_type",
        relation="rel_print_document_type_2_report",
        column1="report_id",
        column2="type_id",
        domain="[('model', '=', model)]",
    )
    print_python_code = fields.Text(
        string="Condition",
        help="The result of executing the expresion must be " "a boolean.",
        default="""# Available locals:\n#  - document: current recordset\nresult = True""",
    )
    print_multi = fields.Boolean(
        string="Multiple Records",
        default=False,
    )

    def _get_print_localdict(self, document):
        self.ensure_one()
        return {
            "env": self.env,
            "document": document,
        }

    def _evaluate_print_python_code(self, document):
        self.ensure_one()
        result = ""
        localdict = self._get_print_localdict(document)
        try:
            safe_eval(self.print_python_code, localdict, mode="exec", nocopy=True)
            result = localdict["result"]
        except:  # noqa: E722
            result = False
        return result

    @api.constrains(
        "print_python_code",
    )
    def _check_print_python_code(self):
        for action in self.sudo().filtered("print_python_code"):
            msg = test_python_expr(expr=action.print_python_code.strip(), mode="exec")
            if msg:
                raise ValidationError(msg)
