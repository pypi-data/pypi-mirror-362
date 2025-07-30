.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/agpl-3.0.html
   :alt: License: AGPL-3

==================
📝 **Description**
==================

Master Data Mixin is an Odoo module that provides a reusable mixin for managing master data models. It helps you standardize, extend, and maintain master data (such as categories, types, or reference tables) across your Odoo modules.

It is ideal for companies and developers who want to ensure consistency and best practices in master data management.

==========================
💡 **Use Cases / Context**
==========================

- Companies that need to manage reference/master data (e.g., product categories, business types) in a consistent way.
- Developers who want to add master data logic to custom modules without rewriting boilerplate code.
- Organizations that require standardized master data structures across multiple modules.

===================
🚀 **Installation**
===================

To install this module:

1.  Clone the branch **18.0** of the repository: https://github.com/open-synergy/ssi-mixin
2.  Add the path to this repository in your Odoo configuration (`addons-path`)
3.  Update the module list (ensure you are in developer mode)
4.  Go to menu *Apps → Apps → Main Apps*
5.  Search for *Master Data Mixin*
6.  Install the module

=================
🛠️ **How To Use**
=================

1. Install this module and its dependencies.
2. Add the mixin to your custom model by inheriting from `mixin.master_data`.
3. Create or configure master data records as needed.
4. Use the provided actions, buttons, or fields to manage and maintain master data.
5. Integrate master data with other business processes for consistency.

==================
🐞 **Bug Tracker**
==================

Bugs are tracked on `GitHub Issues <https://github.com/open-synergy/ssi-mixin/issues>`_.
If you encounter any issues, please check if it has already been reported. If not, help us improve by providing detailed feedback.

==============
🙌 **Credits**
==============

**Contributors:**

- Andhitia Rama <andhitia.r@gmail.com>
- Asrul Bastian Yunas <asrulbastianyunas@gmail.com>
- Michael Viriyananda <viriyananda.michael@gmail.com>

===============
**Maintainer:**
===============

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by PT. Simetri Sinergi Indonesia.
