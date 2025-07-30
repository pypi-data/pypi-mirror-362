# -*- coding: utf-8 -*-
{
    'name': "sm_rest_capture_log",

    'summary': """
    Temporary module to capture and log all REST API requests during Odoo 12 to 17 migration""",

    'description': """
    This module intercepts all incoming REST API requests made through base_rest
    and stores them in a persistent model for later replay in Odoo 17.
    
    Features:
    - Captures all HTTP methods (GET, POST, PUT, DELETE, etc.)
    - Stores request details: URL, headers, body, timestamp, client IP
    - Records response data for complete audit trail
    - Non-intrusive design compatible with base_rest architecture
    
    WARNING: This is a temporary module for migration purposes only.
    """,

    'author': "Som Mobilitat",
    'website': "https://www.sommobilitat.coop",
    'maintainers': ["nicolasramos"],

    'category': 'Technical',
    'version': '12.0.1.0.0',

    # Dependencies
    'depends': [
        'base',
        'base_rest',
    ],

    # Data files
    'data': [
        'security/ir.model.access.csv',
        'views/rest_request_log_views.xml',
        'views/rest_replay_config_views.xml',
        'wizards/replay_requests_wizard_views.xml',
    ],

    # Installation
    'installable': True,
    'auto_install': False,
    'application': False,

    # This module is temporary and should not be used in production long-term
    'development_status': 'Alpha',
}