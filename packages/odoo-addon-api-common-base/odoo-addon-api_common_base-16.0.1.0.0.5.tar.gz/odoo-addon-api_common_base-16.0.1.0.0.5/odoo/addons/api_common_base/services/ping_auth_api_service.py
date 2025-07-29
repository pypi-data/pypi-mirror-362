from odoo import _
from odoo.addons.base_rest import restapi
from odoo.addons.component.core import Component


class PingAuthAPIService(Component):
    _name = "ping.auth.api.service"
    _inherit = "base.rest.service"
    _collection = "sc.api.key.services"
    _usage = "ping"  # service_name
    _description = """
        Ping services (test the api-key api)
    """

    @restapi.method(
        [(["/search"], "GET")],
        output_param=restapi.CerberusValidator({"message": {"type": "string"}}),
    )
    def search(self):
        return {"message": _("Called search on auth ping API")}

    @restapi.method(
        [(["/create"], "POST")],
        input_param=restapi.CerberusValidator({"id": {"type": "string"}}),
        output_param=restapi.CerberusValidator({"message": {"type": "string"}}),
    )
    def create(self, **params):
        return {"message": _("Called auth create with id {}").format(params["id"])}
