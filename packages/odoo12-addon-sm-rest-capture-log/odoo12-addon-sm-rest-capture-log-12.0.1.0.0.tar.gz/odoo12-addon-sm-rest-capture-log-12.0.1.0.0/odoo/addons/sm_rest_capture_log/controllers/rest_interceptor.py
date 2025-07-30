# -*- coding: utf-8 -*-
import json
import logging
import time
import uuid
from functools import wraps

import odoo
from odoo import http
from odoo.http import request

try:
    from odoo.addons.base_rest.controllers.main import RestController
except ImportError:
    RestController = None

_logger = logging.getLogger(__name__)


class RestRequestInterceptor:
    """Interceptor to capture REST API requests and responses"""

    def __init__(self):
        self._setup_interception()

    def _setup_interception(self):
        """Setup monkey patching for base_rest controller"""
        _logger.info("SM_REST_LOG: Starting interception setup...")
        if not RestController:
            _logger.warning("SM_REST_LOG: base_rest.controllers.main.RestController not found. Logging disabled.")
            return

        _logger.info("SM_REST_LOG: Found RestController: {}".format(RestController))
        _logger.info("SM_REST_LOG: Attempting to patch _process_method.")

        if not hasattr(RestController, '_process_method'):
            _logger.error("SM_REST_LOG: Critical - RestController has no '_process_method'. This module cannot work.")
            _logger.info("SM_REST_LOG: Available methods are: {}".format(dir(RestController)))
            return

        if hasattr(RestController, '_original_process_method_sm_log'):
            _logger.info("SM_REST_LOG: Patch for _process_method already applied.")
            return

        # Store original _process_method
        RestController._original_process_method_sm_log = RestController._process_method

        # This wrapper will replace _process_method
        @wraps(RestController._original_process_method_sm_log)
        def intercepted_process_method(controller_self, service_name, method_name, *args, **kwargs):
            _logger.info("SM_REST_LOG: Intercepting _process_method for service '{}', method '{}'".format(service_name, method_name))
            
            start_time = time.time()
            request_id = str(uuid.uuid4())
            
            # In old versions, params might be in kwargs
            params = kwargs.get('params', {})

            # Capture request data
            _logger.info("SM_REST_LOG: Capturing request data for request ID: {}".format(request_id))
            request_data = RestRequestInterceptor._capture_request_data_static(service_name, method_name, params, request_id, args)

            # Log the incoming request
            _logger.info("SM_REST_LOG: Logging request for request ID: {}".format(request_id))
            RestRequestInterceptor._log_request_static(request_data)

            try:
                # Call original _process_method
                response = RestController._original_process_method_sm_log(controller_self, service_name, method_name, *args, **kwargs)
                _logger.info("SM_REST_LOG: Original method executed for request ID: {}".format(request_id))

                # Calculate response time
                response_time_ms = (time.time() - start_time) * 1000

                # Capture response data
                response_data = RestRequestInterceptor._capture_response_data_static(response, response_time_ms)

                # Update log with response data
                _logger.info("SM_REST_LOG: Logging response for request ID: {}".format(request_id))
                RestRequestInterceptor._log_response_static(request_id, response_data)

                return response

            except Exception as e:
                _logger.error("SM_REST_LOG: Exception in wrapped method for request ID: {}. Error: {}".format(request_id, e), exc_info=True)
                # Log error response
                response_time_ms = (time.time() - start_time) * 1000
                status_code = getattr(e, 'code', 500)
                body = str(e)
                if hasattr(e, 'get_body'):
                    body = e.get_body(request.httprequest.environ)

                error_response = {
                    'status_code': status_code,
                    'body': body,
                    'headers': '{}',
                    'response_time_ms': response_time_ms,
                }
                _logger.info("SM_REST_LOG: Logging error response for request ID: {}".format(request_id))
                RestRequestInterceptor._log_response_static(request_id, error_response, error=True)
                raise

        RestController._process_method = intercepted_process_method
        _logger.info("SM_REST_LOG: REST request interception enabled (using _process_method)")

    @staticmethod
    def _capture_request_data_static(service_name, method_name, params, request_id, args):
        """Capture all relevant request data"""
        try:
            httprequest = request.httprequest if request else None
            request_url = httprequest.url if httprequest else ''
            headers = dict(httprequest.headers) if httprequest else {}
            body = ''
            if httprequest and hasattr(httprequest, 'get_data'):
                try:
                    body_data = httprequest.get_data(as_text=True)
                    body = body_data if body_data else ''
                except Exception:
                    body = ''
            
            query_params = dict(httprequest.args) if httprequest else {}
            method_params = params or {}
            
            _id = args[0] if args else None
            endpoint = "{}/{}".format(service_name, method_name)
            if _id:
                endpoint = "{}/{}/{}".format(service_name, _id, method_name)

            client_ip = httprequest.environ.get('HTTP_X_FORWARDED_FOR', httprequest.environ.get('REMOTE_ADDR', '')) if httprequest else ''
            user_agent = headers.get('User-Agent', '')

            return {
                'request_id': request_id,
                'http_method': httprequest.method if httprequest else 'UNKNOWN',
                'method_name': method_name,
                'url': request_url,
                'endpoint_name': endpoint,
                'service_name': service_name,
                'headers': json.dumps(headers, default=str),
                'request_body': body,
                'query_params': json.dumps(query_params, default=str),
                'method_params': json.dumps(method_params, default=str),
                'client_ip': client_ip,
                'user_agent': user_agent,
            }
        except Exception as e:
            _logger.error("SM_REST_LOG: Error capturing request data: {}".format(e), exc_info=True)
            return {
                'request_id': request_id,
                'http_method': 'UNKNOWN',
                'method_name': method_name,
                'url': 'Error capturing URL',
                'endpoint_name': service_name,
                'service_name': service_name,
                'headers': '{}',
                'request_body': "Error: {}".format(e),
                'query_params': '{}',
                'method_params': '{}',
                'client_ip': '',
                'user_agent': '',
            }

    @staticmethod
    def _capture_response_data_static(response, response_time_ms):
        """Capture response data"""
        try:
            status_code = 200
            response_headers = {}
            response_body = ''

            if isinstance(response, http.Response):
                status_code = response.status_code
                response_headers = dict(response.headers)
                try:
                    response_body = response.get_data(as_text=True)
                except Exception:
                    response_body = str(response.data)
            elif isinstance(response, (dict, list)):
                response_body = json.dumps(response, default=str)
            else:
                response_body = str(response)

            return {
                'status_code': status_code,
                'headers': json.dumps(response_headers, default=str),
                'body': response_body,
                'response_time_ms': response_time_ms,
            }
        except Exception as e:
            _logger.error("SM_REST_LOG: Error capturing response data: {}".format(e), exc_info=True)
            return {
                'status_code': 500,
                'headers': '{}',
                'body': "Error capturing response: {}".format(e),
                'response_time_ms': response_time_ms,
            }

    @staticmethod
    def _log_request_static(request_data):
        """Log the request data to database"""
        try:
            if not request or not hasattr(request, 'env'):
                return
            with odoo.api.Environment.manage():
                with odoo.registry(request.env.cr.dbname).cursor() as new_cr:
                    _logger.info("SM_REST_LOG: Creating log entry in new cursor.")
                    new_env = odoo.api.Environment(new_cr, odoo.SUPERUSER_ID, {})
                    new_env['rest.request.log'].create_log_entry(request_data)
                    new_cr.commit()
                    _logger.info("SM_REST_LOG: Committed log entry for request ID: {}".format(request_data.get('request_id')))
        except Exception as e:
            _logger.error("SM_REST_LOG: Error logging request: {}".format(str(e)), exc_info=True)

    @staticmethod
    def _log_response_static(request_id, response_data, error=False):
        """Update the log entry with response data"""
        try:
            if not request or not hasattr(request, 'env'):
                return
            with odoo.api.Environment.manage():
                with odoo.registry(request.env.cr.dbname).cursor() as new_cr:
                    _logger.info("SM_REST_LOG: Updating log entry for request ID: {}".format(request_id))
                    new_env = odoo.api.Environment(new_cr, odoo.SUPERUSER_ID, {})
                    log_entry = new_env['rest.request.log'].search([('request_id', '=', request_id)], limit=1)
                    if log_entry:
                        update_vals = {
                            'response_status_code': response_data.get('status_code', 0),
                            'response_headers': response_data.get('headers', '{}'),
                            'response_body': response_data.get('body', ''),
                            'response_time_ms': response_data.get('response_time_ms', 0),
                            'processing_status': 'error' if error else 'processed',
                        }
                        if error:
                            update_vals['error_message'] = response_data.get('body', '')
                        log_entry.write(update_vals)
                        new_cr.commit()
                        _logger.info("SM_REST_LOG: Committed response for request ID: {}".format(request_id))
                    else:
                        _logger.warning("SM_REST_LOG: Could not find log entry to update for request ID: {}".format(request_id))
        except Exception as e:
            _logger.error("SM_REST_LOG: Error logging response for request ID {}: {}".format(request_id, str(e)), exc_info=True)

# Initialize the interceptor when the module is loaded
_interceptor = RestRequestInterceptor()