# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import io
import logging
from base64 import b64encode

from odoo import fields, models

from odoo.addons.ssi_decorator import ssi_decorator

_logger = logging.getLogger(__name__)

try:
    import qrcode
except (ImportError, IOError) as err:
    _logger.debug(err)


class MixinQRCode(models.AbstractModel):
    _name = "mixin.qr_code"
    _inherit = [
        "mixin.decorator",
    ]
    _description = "QR Code Mixin"

    _qr_code_create_page = False
    _qr_code_page_xpath = "//page[last()]"

    def _compute_qr_image(self):
        for document in self:
            qrcode_content = document._get_qr_code_content()
            img = qrcode.make(qrcode_content)
            result = io.BytesIO()
            img.save(result, format="PNG")
            result.seek(0)
            img_bytes = result.read()
            base64_encoded_result_bytes = b64encode(img_bytes)
            qr_image = base64_encoded_result_bytes.decode("ascii")
            document.qr_image = qr_image

    qr_image = fields.Binary(
        string="QR Code",
        compute="_compute_qr_image",
        store=False,
    )

    @ssi_decorator.insert_on_form_view()
    def _qr_code_insert_form_element(self, view_arch):
        if self._qr_code_create_page:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id="ssi_qr_code_mixin.qr_code_page",
                xpath=self._qr_code_page_xpath,
                position="after",
            )
        return view_arch

    def _get_qr_code_content(self):
        self.ensure_one()
        criteria = [
            ("model", "=", self._name),
        ]
        obj_ir_model = self.env["ir.model"]
        content_policy = obj_ir_model.search(criteria)
        if len(content_policy) > 0:
            content = content_policy[0]._get_qr_content(self)
        else:
            content = self._get_qr_standard_content()
        return content

    def _get_qr_standard_content(self):
        self.ensure_one()
        odoo_url = self.env["ir.config_parameter"].get_param("web.base.url")
        document_url = "/web?#id=%d&view_type=form&model=%s" % (
            self.id,
            self._name,
        )
        full_url = odoo_url + document_url
        return full_url
