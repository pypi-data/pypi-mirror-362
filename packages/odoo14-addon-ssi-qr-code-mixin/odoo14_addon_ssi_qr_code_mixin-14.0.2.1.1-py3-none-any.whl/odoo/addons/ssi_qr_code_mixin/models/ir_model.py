# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval, test_python_expr


class IrModel(models.Model):
    _name = "ir.model"
    _inherit = "ir.model"

    qr_use_standard_content = fields.Boolean(
        string="Use Standard Content",
        default=True,
    )
    qr_python_code = fields.Text(
        string="Python Code for Custom Content",
        default="result = True",
    )

    def _get_qr_localdict(self, document):
        self.ensure_one()
        return {
            "env": self.env,
            "document": document,
        }

    def _get_qr_content(self, document):
        self.ensure_one()
        if self.qr_use_standard_content:
            content = document._get_qr_standard_content()
        else:
            content = self._get_qr_custom_content(document)
        return content

    def _get_qr_custom_content(self, document):
        self.ensure_one()
        result = ""
        localdict = self._get_qr_localdict(document)
        try:
            safe_eval(self.qr_python_code, localdict, mode="exec", nocopy=True)
            result = localdict["result"]
        except:  # noqa: E722
            result = ""
        return result

    @api.constrains(
        "qr_python_code",
    )
    def _check_qr_python_code(self):
        for action in self.sudo().filtered("qr_python_code"):
            msg = test_python_expr(expr=action.qr_python_code.strip(), mode="exec")
            if msg:
                raise ValidationError(msg)
