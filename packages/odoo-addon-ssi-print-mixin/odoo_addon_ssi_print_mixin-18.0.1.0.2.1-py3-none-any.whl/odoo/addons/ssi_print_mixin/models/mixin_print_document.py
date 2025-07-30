# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html)

from lxml import etree, html

from odoo import api, models


class MixinPrintDocument(models.AbstractModel):
    _name = "mixin.print_document"
    _description = "Print Document Mixin"

    # Attributes related to automatically insert elemnt on form view
    _automatically_insert_print_button = False
    _print_button_xpath = "/form/header/field[@name='state']"
    _print_button_position = "before"

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        result = super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )
        View = self.env["ir.ui.view"]

        view_arch = etree.XML(result["arch"])

        if view_type == "form":
            view_arch = self._view_add_form_print_button(view_arch)
        elif view_type == "tree":
            view_arch = self._view_add_tree_print_button(view_arch)

        if view_id and result.get("base_model", self._name) != self._name:
            View = View.with_context(base_model_name=result["base_model"])
        new_arch, new_fields = View.postprocess_and_fields(view_arch, self._name)
        result["arch"] = new_arch
        new_fields.update(result["fields"])
        result["fields"] = new_fields

        return result

    @api.model
    def _add_view_element(
        self, view_arch, qweb_template_xml_id, xpath, position="after", order=False
    ):
        additional_element = self.env["ir.qweb"]._render(qweb_template_xml_id)
        if len(view_arch.xpath(xpath)) == 0:
            return view_arch
        node_xpath = view_arch.xpath(xpath)[0]
        for frag in html.fragments_fromstring(additional_element):
            if order:
                frag.set("order", str(order))
            if position == "after":
                node_xpath.addnext(frag)
            elif position == "before":
                node_xpath.addprevious(frag)
            elif position == "inside":
                node_xpath.insert(0, frag)
        return view_arch

    @api.model
    def _view_add_tree_print_button(self, view_arch):
        if self._automatically_insert_print_button:
            view_arch = self._add_view_element(
                view_arch,
                "ssi_print_mixin.tree_button_print",
                "/tree/header",
                "inside",
            )
        return view_arch

    @api.model
    def _view_add_form_print_button(self, view_arch):
        if self._automatically_insert_print_button:
            view_arch = self._add_view_element(
                view_arch,
                "ssi_print_mixin.button_ssi_print",
                self._print_button_xpath,
                self._print_button_position,
            )
        return view_arch
