# -*- coding: utf-8 -*-
import json
import logging
from urllib.parse import urlparse, urlunparse

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

try:
    import requests
except ImportError:
    _logger.warning("The 'requests' library is not available. Please install it with 'pip install requests'")
    requests = None


class ReplayRequestsWizard(models.TransientModel):
    _name = 'replay.requests.wizard'
    _description = 'Wizard to Replay REST Requests'

    config_id = fields.Many2one(
        'rest.replay.config',
        string='Replay Configuration',
        required=True,
        domain="[('active', '=', True)]",
        help="Select the active Odoo 17 target configuration to use for replaying."
    )
    request_log_ids = fields.Many2many(
        'rest.request.log',
        string='Requests to Replay',
        readonly=True,
    )
    total_requests = fields.Integer(
        string="Total Requests",
        compute='_compute_total_requests',
        readonly=True
    )

    @api.depends('request_log_ids')
    def _compute_total_requests(self):
        for wizard in self:
            wizard.total_requests = len(wizard.request_log_ids)

    @api.model
    def default_get(self, fields_list):
        """Pre-populate the wizard with the selected log requests."""
        res = super(ReplayRequestsWizard, self).default_get(fields_list)
        if self.env.context.get('active_model') == 'rest.request.log' and self.env.context.get('active_ids'):
            res['request_log_ids'] = [(6, 0, self.env.context['active_ids'])]
        return res

    def action_replay_requests(self):
        """
        The main action to replay the selected requests against the target Odoo 17 instance.
        """
        self.ensure_one()
        if not requests:
            raise UserError(_("The 'requests' Python library is required. Please ask your system administrator to install it."))
        if not self.request_log_ids:
            raise UserError(_("There are no requests selected to be replayed."))

        target_base = urlparse(self.config_id.target_url)
        success_count = 0
        fail_count = 0

        for log in self.request_log_ids:
            try:
                # 1. Reconstruct the target URL
                original_url = urlparse(log.request_url)
                new_url_parts = (
                    target_base.scheme,
                    target_base.netloc,
                    original_url.path,
                    original_url.params,
                    original_url.query,
                    original_url.fragment,
                )
                final_url = urlunparse(new_url_parts)

                # 2. Prepare headers
                headers = json.loads(log.request_headers) if log.request_headers else {}
                headers.pop('Host', None)
                if self.config_id.auth_header:
                    headers['Authorization'] = self.config_id.auth_header
                
                # 3. Prepare body
                body = log.request_body.encode('utf-8') if log.request_body else None

                # 4. Make the request
                response = requests.request(
                    method=log.http_method,
                    url=final_url,
                    headers=headers,
                    data=body,
                    timeout=30
                )

                # 5. Update the log with the result
                log.write({
                    'response_status_code': response.status_code,
                    'response_body': response.text,
                    'migrated_to_odoo17': response.ok,
                    'processing_status': 'replayed' if response.ok else 'error',
                    'migration_notes': "Replayed to {} on {}. Status: {}.".format(
                        self.config_id.target_url,
                        fields.Datetime.now(),
                        response.status_code
                    )
                })
                if response.ok:
                    success_count += 1
                else:
                    fail_count += 1
            
            except requests.RequestException as e:
                fail_count += 1
                log.write({
                    'processing_status': 'error',
                    'migrated_to_odoo17': False,
                    'migration_notes': "Failed to replay: RequestException - {}".format(e),
                })
            except Exception as e:
                fail_count += 1
                _logger.error("Unexpected error replaying request ID %s: %s", log.id, e, exc_info=True)
                log.write({
                    'processing_status': 'error',
                    'migrated_to_odoo17': False,
                    'migration_notes': "Failed to replay: Unexpected error - {}".format(e),
                })
        
        # We need to commit the changes on the logs here, because the wizard will be closed.
        self.env.cr.commit()

        # Return a notification to the user
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Replay Process Finished'),
                'message': _('Successfully replayed: %s\nFailed: %s') % (success_count, fail_count),
                'sticky': True, # User has to close it manually
                'type': 'success' if fail_count == 0 else 'warning',
            }
        } 