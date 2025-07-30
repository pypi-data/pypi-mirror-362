# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html)

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MixinMasterData(models.AbstractModel):
    _name = "mixin.master_data"
    _inherit = [
        "mail.activity.mixin",
        "mail.thread",
        "mixin.print_document",
        "mixin.sequence",
    ]
    _description = "Mixin for Master Data"
    _field_name_string = "Name"
    _show_code_on_display_name = False
    _automatically_insert_print_button = True
    _print_button_xpath = "/form/header"
    _print_button_position = "inside"

    @api.model
    def _get_field_name_string(self):
        return self._field_name_string

    name = fields.Char(
        string="Document Name",
        required=True,
        help="Master data name. Fill with the name of the master data record.",
    )
    code = fields.Char(
        string="Document Code",
        required=True,
        help="""Master data unique identifier.

* Fill with '/' if You do not need unique identifier
* Click 'Generate Code' button to automatically assign code.
  Sequence template mush be set to perform this action
  Only master data with '/' code will be assign automatic code""",
    )
    active = fields.Boolean(
        string="Active Document",
        default=True,
        help="""Master data status

* Inactive data can not be selected when creating new transaction
* Transaction with inactive master data can still be viewed
* Set master data as inactive if master data no longger needed,
but master data already used on transaction""",
    )
    note = fields.Text(
        string="Additional Note",
        help="Additional notes or remarks for this master data record.",
    )

    @api.returns("self", lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        if "code" not in default:
            default["code"] = _(f"{self.code} (copy)")
        return super().copy(default=default)

    @api.constrains("code")
    def _check_duplicate_code(self):
        for record in self:
            criteria = [
                ("code", "=", record.code),
                ("id", "!=", record.id),
                ("code", "!=", "/"),
            ]
            count_duplicate = self.search_count(criteria)
            if count_duplicate > 0:
                error_message = f"""
                Document Type: {self._description.lower()}
                Context: Create or update document
                Database ID: {self.id}
                Problem: Dupilicate code
                Solution: Change code
                """
                raise UserError(error_message)

    def action_generate_code(self):
        for record in self.sudo():
            record._create_sequence()

    def action_reset_code(self):
        for record in self.sudo():
            record.write(
                {
                    "code": "/",
                }
            )

    def name_get(self):
        result = []
        for record in self:
            if self._show_code_on_display_name:
                name = f"[{record.code}] {record.name}"
            else:
                name = record.name
            result.append((record.id, name))
        return result
