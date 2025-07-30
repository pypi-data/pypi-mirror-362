# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RestReplayConfig(models.Model):
    """Model to store the configuration for replaying requests to Odoo 17."""
    _name = 'rest.replay.config'
    _description = 'Odoo 17 Replay Configuration'
    _rec_name = 'name'

    name = fields.Char(
        required=True,
        default='Odoo 17 Target Connection'
    )
    target_url = fields.Char(
        string='Target Odoo 17 URL',
        required=True,
        help="The base URL of the Odoo 17 instance (e.g., https://my-odoo17.com)"
    )
    auth_header = fields.Char(
        string='Authorization Header Value',
        help="The full value for the Authorization header. E.g., 'Bearer your-secret-token'",
        widget='password',
        copy=False
    )
    active = fields.Boolean(
        default=True,
        help="Only active configurations can be used."
    )
    notes = fields.Text(string='Notes')

    @api.constrains('target_url')
    def _check_target_url(self):
        """Ensure the URL is valid."""
        for record in self:
            if record.target_url and not (record.target_url.startswith('http://') or record.target_url.startswith('https://')):
                raise ValidationError("The URL must start with 'http://' or 'https://'.") 