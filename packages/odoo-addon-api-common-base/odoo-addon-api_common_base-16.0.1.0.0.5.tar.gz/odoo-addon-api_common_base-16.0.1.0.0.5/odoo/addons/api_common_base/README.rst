#################
 API COMMON BASE
#################

This module uses OCAs REST API modules for creating endpoints based on a
common controller called `/api/`. It allows you to expand all the
different API endpoints from this particular controller.

.. note::

   This module is made by and for developers.

**Table of contents**

.. contents::
   :local:

***************
 Configuration
***************

No configuration needed for this module.

*******
 Usage
*******

To use this module it just needs to be installed and (from your own
module) use this controller directly from your services. Like so:

.. note::

   The `api_common_base` module is a base module for creating API
   endpoints. It does not have any endpoints by itself.

.. code:: python

   # -*- coding: utf-8 -*-
   from odoo.addons.component.core import Component


   class YourServiceAPI(Component):
       _name = "your.model.api"
       _inherit = "base.rest.service"
       _usage = "yourEndpoint"
       _default_auth = "api_key"
       _collection = (
           "api_common_base.services"  #  <-- that's where you'd use this module as a base
       )
       _description = """
       Description of your endpoint
       """

       def get(self): ...

After that you will see your endpoint available at the route:
`{odoo_base_url}/api/yourEndpoint/get`

Also, the class `APICommonBaseRestCase` from `tests/common_service.py`
can be inherited in API tests classes from dependent modules in order to
use its basic common setup API methods (``http_get``, ``http_post``,
``http_get_content``).

************************
 Known issues / Roadmap
************************

There are no known issues for this module.

*************
 Bug Tracker
*************

Bugs are tracked on `GitLab Issues
<https://gitlab.com/somitcoop/erp-research/odoo-helpdesk/-/issues>`_. In
case of trouble, please check there if your issue has already been
reported. If you spotted it first, help us smashing it by providing a
detailed and welcomed feedback.

Do not contact contributors directly about support or help with
technical issues.

*********
 Credits
*********

Authors
=======

-  SomIT SCCL
-  Som Connexio SCCL

Contributors
============

-  `SomIT SCCL <https://somit.coop>`_:

      -  Álvaro García <alvaro.garcia@somit.coop>
      -  José Robles <jose.robles@somit.coop>
      -  Juan Manuel Regalado <juanmanuel.regalado@somit.coop>

-  `Som Connexio SCCL <https://somconnexio.coop>`_:

      -  Gerard Funosas <gerard.funosas@somconnexio.coop>

Maintainers
===========

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization
whose mission is to support the collaborative development of Odoo
features and promote its widespread use.

You are welcome to contribute. To learn how please visit
https://odoo-community.org/page/Contribute.
