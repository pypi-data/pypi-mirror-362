import uuid

from odoo import fields, models


class AuthApiKey(models.Model):
    _inherit = "auth.api.key"

    def _default_key(self):
        return uuid.uuid4()

    key = fields.Char(default=_default_key)
