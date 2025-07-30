.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/agpl-3.0.html
   :alt: License: AGPL-3

==================
📝 **Description**
==================

Sequence Mixin is an Odoo module that provides a flexible and reusable sequence management mixin for your business models. It allows you to easily add automatic numbering and sequence logic to any model in Odoo.

It is ideal for companies that require consistent and customizable document numbering across different business processes.

==========================
💡 **Use Cases / Context**
==========================

- Companies that need unique document numbers for various models (e.g., invoices, orders, custom records).
- Developers who want to add sequence logic to custom modules without rewriting boilerplate code.
- Organizations that require configurable sequence formats and rules.

===================
🚀 **Installation**
===================

To install this module:

1.  Clone the branch **18.0** of the repository: https://github.com/open-synergy/ssi-mixin
2.  Add the path to this repository in your Odoo configuration (`addons-path`)
3.  Update the module list (ensure you are in developer mode)
4.  Go to menu *Apps → Apps → Main Apps*
5.  Search for *Sequence Mixin*
6.  Install the module

=================
🛠️ **How To Use**
=================

1. Install this module and its dependencies.
2. Add the mixin to your custom model by inheriting from `mixin.sequence`.
3. Configure the sequence template as needed for your model.
4. Create or update records to see automatic numbering in action.
5. Adjust sequence settings for advanced use cases.

==================
🐞 **Bug Tracker**
==================

Bugs are tracked on `GitHub Issues <https://github.com/open-synergy/ssi-mixin/issues>`_.
If you encounter any issues, please check if it has already been reported. If not, help us improve by providing detailed feedback.

==============
🙌 **Credits**
==============

**Contributors:**

- Michael Viriyananda <viriyananda.michael@gmail.com>
- Andhitia Rama <andhitia.r@gmail.com>
- Nur Azmi <azmimr67@gmail.com>

===============
**Maintainer:**
===============

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by PT. Simetri Sinergi Indonesia.
