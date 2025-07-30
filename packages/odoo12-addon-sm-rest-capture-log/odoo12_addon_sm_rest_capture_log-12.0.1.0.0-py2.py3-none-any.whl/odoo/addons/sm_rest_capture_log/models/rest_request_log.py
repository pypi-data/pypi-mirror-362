# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class RestRequestLog(models.Model):
    """Model to store REST API request logs for migration purposes"""
    _name = 'rest.request.log'
    _description = 'REST API Request Log'
    _order = 'request_datetime desc'
    _rec_name = 'display_name'

    # Request identification
    display_name = fields.Char(
        string='Request Summary',
        compute='_compute_display_name'
    )
    request_datetime = fields.Datetime(
        string='Request DateTime',
        required=True,
        default=fields.Datetime.now,
        help="Timestamp when the request was received"
    )
    request_id = fields.Char(
        string='Request ID',
        help="Unique identifier for this request"
    )

    # HTTP Request details
    http_method = fields.Selection([
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('PATCH', 'PATCH'),
        ('DELETE', 'DELETE'),
        ('HEAD', 'HEAD'),
        ('OPTIONS', 'OPTIONS'),
    ], string='HTTP Method', required=True)
    
    request_url = fields.Text(
        string='Request URL',
        required=True,
        help="Complete URL including query parameters"
    )
    endpoint_name = fields.Char(
        string='Endpoint Name',
        help="Name of the REST endpoint if available"
    )
    service_name = fields.Char(
        string='Service Name',
        help="Name of the base_rest service"
    )
    method_name = fields.Char(
        string='Method Name',
        help="Name of the service method called"
    )
    
    # Request data
    request_headers = fields.Text(
        string='Request Headers',
        help="Complete HTTP headers as JSON"
    )
    request_body = fields.Text(
        string='Request Body',
        help="Request payload/body content"
    )
    query_params = fields.Text(
        string='Query Parameters',
        help="URL query parameters as JSON"
    )
    method_params = fields.Text(
        string='Method Parameters',
        help="Parameters passed to the service method as JSON"
    )
    
    # Client information
    client_ip = fields.Char(
        string='Client IP',
        help="IP address of the client making the request"
    )
    user_agent = fields.Text(
        string='User Agent',
        help="Client user agent string"
    )
    
    # Response data
    response_status_code = fields.Integer(
        string='Response Status Code',
        help="HTTP response status code"
    )
    response_headers = fields.Text(
        string='Response Headers',
        help="HTTP response headers as JSON"
    )
    response_body = fields.Text(
        string='Response Body',
        help="Response content/body"
    )
    response_time_ms = fields.Float(
        string='Response Time (ms)',
        help="Time taken to process the request in milliseconds"
    )
    
    # Processing status
    processing_status = fields.Selection([
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('error', 'Error'),
        ('replayed', 'Replayed in Odoo 17'),
    ], string='Processing Status', default='pending')
    
    error_message = fields.Text(
        string='Error Message',
        help="Error message if request processing failed"
    )
    
    # Migration tracking
    migrated_to_odoo17 = fields.Boolean(
        string='Migrated to Odoo 17',
        default=False,
        help="Indicates if this request has been replayed in Odoo 17"
    )
    migration_notes = fields.Text(
        string='Migration Notes',
        help="Notes about the migration process"
    )
    
    @api.depends('http_method', 'request_url', 'request_datetime')
    def _compute_display_name(self):
        """Compute a readable display name for the request"""
        for record in self:
            if record.request_url:
                # Extract the path from URL for display
                url_parts = record.request_url.split('?')[0].split('/')
                path = '/'.join(url_parts[-3:]) if len(url_parts) > 3 else record.request_url
                record.display_name = "{} {}".format(record.http_method, path)
            else:
                record.display_name = "{} - {}".format(record.http_method, record.request_datetime)
    
    @api.model
    def create_log_entry(self, request_data, response_data=None):
        """Create a new log entry from request and response data"""
        try:
            vals = {
                'http_method': request_data.get('http_method', 'UNKNOWN'),
                'request_url': request_data.get('url', ''),
                'endpoint_name': request_data.get('endpoint_name', ''),
                'service_name': request_data.get('service_name', ''),
                'method_name': request_data.get('method_name', ''),
                'request_headers': request_data.get('headers', ''),
                'request_body': request_data.get('request_body', ''),
                'query_params': request_data.get('query_params', ''),
                'method_params': request_data.get('method_params', ''),
                'client_ip': request_data.get('client_ip', ''),
                'user_agent': request_data.get('user_agent', ''),
                'request_id': request_data.get('request_id', ''),
            }
            
            if response_data:
                vals.update({
                    'response_status_code': response_data.get('status_code', 0),
                    'response_headers': response_data.get('headers', ''),
                    'response_body': response_data.get('body', ''),
                    'response_time_ms': response_data.get('response_time_ms', 0),
                    'processing_status': 'processed',
                })
            
            return self.create(vals)
            
        except Exception as e:
            _logger.error("Error creating REST request log: {}".format(str(e)))
            return False
    
    def mark_as_migrated(self, notes=None):
        """Mark this request as migrated to Odoo 17"""
        self.write({
            'migrated_to_odoo17': True,
            'processing_status': 'replayed',
            'migration_notes': notes or 'Migrated to Odoo 17',
        })
    
    def get_replay_data(self):
        """Get the data needed to replay this request in Odoo 17"""
        self.ensure_one()
        return {
            'method': self.http_method,
            'url': self.request_url,
            'headers': self.request_headers,
            'body': self.request_body,
            'query_params': self.query_params,
            'original_timestamp': self.request_datetime,
            'client_ip': self.client_ip,
        }