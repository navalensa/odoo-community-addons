# Copyright 2026 NuoBiT Solutions SL - Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo.tests import TransactionCase
from odoo.tools.misc import file_path
from odoo.tools.template_inheritance import apply_inheritance_specs

POINT_OF_SALE = (
    "point_of_sale/static/src/app/screens/receipt_screen/receipt/receipt_header/"
    "receipt_header.xml"
)
L10N_ES_POS = (
    "l10n_es_pos/static/src/overrides/components/receipt_header/receipt_header.xml"
)
OURS = (
    "l10n_es_pos_simplified_invoice_customer/static/src/overrides/components/"
    "receipt_header/receipt_header.xml"
)


class TestReceiptHeaderAnchor(TransactionCase):
    def _template(self, path):
        # The one template of the file
        (template,) = etree.parse(file_path(path)).getroot().iterchildren("t")
        return template

    def test_rule_holds_over_another_extension(self):
        # A module that changes the customer block's condition, whichever way,
        # leaves the block inside this module's own
        for added in (" and another_condition", " or another_condition"):
            header = apply_inheritance_specs(
                self._template(POINT_OF_SALE), list(self._template(L10N_ES_POS))
            )
            (block,) = header.xpath("//t[contains(@t-if, 'simplified_partner_id')]")
            block.set("t-if", block.get("t-if") + added)
            header = apply_inheritance_specs(header, list(self._template(OURS)))
            (block,) = header.xpath("//t[contains(@t-if, 'another_condition')]")
            self.assertNotIn("is_l10n_es_simplified_invoice", block.get("t-if"))
            self.assertIn(
                "is_l10n_es_simplified_invoice", block.getparent().get("t-if", "")
            )
