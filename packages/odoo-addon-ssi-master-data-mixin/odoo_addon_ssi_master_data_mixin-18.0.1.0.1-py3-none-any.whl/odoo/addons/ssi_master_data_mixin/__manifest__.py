# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html)
{
    "name": "Master Data Mixin",
    "version": "18.0.1.0.1",
    "website": "https://github.com/open-synergy/ssi-mixin",
    "author": "PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "mail",
        "ssi_print_mixin",
        "ssi_sequence_mixin",
    ],
    "data": [
        "views/mixin_master_data_views.xml",
    ],
}
