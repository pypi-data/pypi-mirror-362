#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration Helper Script for REST Capture Log Module

This script provides utilities to export captured REST requests
and prepare them for replay in Odoo 17.

Usage:
    python migration_helper.py --export --output requests.json
    python migration_helper.py --stats
    python migration_helper.py --mark-migrated --request-ids 1,2,3
"""

import argparse
import json
import sys
from datetime import datetime, timedelta

try:
    import odoo
    from odoo import api, SUPERUSER_ID
except ImportError:
    print("Error: This script must be run in an Odoo environment")
    sys.exit(1)


class MigrationHelper:
    """Helper class for REST request migration"""
    
    def __init__(self, database):
        self.database = database
        self.env = None
        self._setup_environment()
    
    def _setup_environment(self):
        """Setup Odoo environment"""
        try:
            registry = odoo.registry(self.database)
            with registry.cursor() as cr:
                self.env = api.Environment(cr, SUPERUSER_ID, {})
        except Exception as e:
            print("Error setting up environment: {}".format(e))
            sys.exit(1)
    
    def export_requests(self, output_file, filters=None):
        """Export REST requests to JSON file"""
        try:
            domain = []
            if filters:
                if filters.get('date_from'):
                    domain.append(('request_datetime', '>=', filters['date_from']))
                if filters.get('date_to'):
                    domain.append(('request_datetime', '<=', filters['date_to']))
                if filters.get('methods'):
                    domain.append(('http_method', 'in', filters['methods']))
                if filters.get('not_migrated'):
                    domain.append(('migrated_to_odoo17', '=', False))
                if filters.get('status'):
                    domain.append(('processing_status', 'in', filters['status']))
            
            with odoo.registry(self.database).cursor() as cr:
                env = api.Environment(cr, SUPERUSER_ID, {})
                logs = env['rest.request.log'].search(domain, order='request_datetime asc')
                
                export_data = []
                for log in logs:
                    export_data.append({
                        'id': log.id,
                        'request_datetime': log.request_datetime.isoformat() if log.request_datetime else None,
                        'http_method': log.http_method,
                        'request_url': log.request_url,
                        'endpoint_name': log.endpoint_name,
                        'service_name': log.service_name,
                        'request_headers': log.request_headers,
                        'request_body': log.request_body,
                        'query_params': log.query_params,
                        'client_ip': log.client_ip,
                        'user_agent': log.user_agent,
                        'response_status_code': log.response_status_code,
                        'response_headers': log.response_headers,
                        'response_body': log.response_body,
                        'response_time_ms': log.response_time_ms,
                        'processing_status': log.processing_status,
                        'migrated_to_odoo17': log.migrated_to_odoo17,
                    })
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        'export_datetime': datetime.now().isoformat(),
                        'total_requests': len(export_data),
                        'filters': filters or {},
                        'requests': export_data
                    }, f, indent=2, ensure_ascii=False)
                
                print("Exported {} requests to {}".format(len(export_data), output_file))
                
        except Exception as e:
            print("Error exporting requests: {}".format(e))
            return False
        
        return True
    
    def show_statistics(self):
        """Show statistics about captured requests"""
        try:
            with odoo.registry(self.database).cursor() as cr:
                env = api.Environment(cr, SUPERUSER_ID, {})
                
                total = env['rest.request.log'].search_count([])
                migrated = env['rest.request.log'].search_count([('migrated_to_odoo17', '=', True)])
                pending = env['rest.request.log'].search_count([('migrated_to_odoo17', '=', False)])
                
                # By method
                methods = env['rest.request.log'].read_group(
                    [], ['http_method'], ['http_method']
                )
                
                # By status
                statuses = env['rest.request.log'].read_group(
                    [], ['processing_status'], ['processing_status']
                )
                
                # By date (last 7 days)
                week_ago = datetime.now() - timedelta(days=7)
                recent = env['rest.request.log'].search_count([
                    ('request_datetime', '>=', week_ago)
                ])
                
                print("\n=== REST Request Capture Statistics ===")
                print("Total requests captured: {}".format(total))
                print("Migrated to Odoo 17: {}".format(migrated))
                print("Pending migration: {}".format(pending))
                print("Requests in last 7 days: {}".format(recent))
                
                print("\n--- By HTTP Method ---")
                for method in methods:
                    print("{}: {}".format(method['http_method'], method['http_method_count']))
                
                print("\n--- By Processing Status ---")
                for status in statuses:
                    print("{}: {}".format(status['processing_status'], status['processing_status_count']))
                
                # Top endpoints
                print("\n--- Top Endpoints ---")
                endpoints = env['rest.request.log'].read_group(
                    [('endpoint_name', '!=', False)], 
                    ['endpoint_name'], ['endpoint_name'], 
                    limit=10, orderby='endpoint_name_count desc'
                )
                for endpoint in endpoints:
                    print("{}: {}".format(endpoint['endpoint_name'], endpoint['endpoint_name_count']))
                
        except Exception as e:
            print("Error getting statistics: {}".format(e))
    
    def mark_as_migrated(self, request_ids, notes=None):
        """Mark specific requests as migrated"""
        try:
            with odoo.registry(self.database).cursor() as cr:
                env = api.Environment(cr, SUPERUSER_ID, {})
                logs = env['rest.request.log'].browse(request_ids)
                
                if not logs:
                    print("No requests found with the specified IDs")
                    return False
                
                migration_notes = notes or "Marked as migrated on {}".format(datetime.now().isoformat())
                logs.mark_as_migrated(migration_notes)
                cr.commit()
                
                print("Marked {} requests as migrated".format(len(logs)))
                
        except Exception as e:
            print("Error marking requests as migrated: {}".format(e))
            return False
        
        return True
    
    def cleanup_old_requests(self, days_old=30):
        """Clean up old migrated requests"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_old)
            
            with odoo.registry(self.database).cursor() as cr:
                env = api.Environment(cr, SUPERUSER_ID, {})
                old_logs = env['rest.request.log'].search([
                    ('migrated_to_odoo17', '=', True),
                    ('request_datetime', '<', cutoff_date)
                ])
                
                count = len(old_logs)
                if count > 0:
                    old_logs.unlink()
                    cr.commit()
                    print("Cleaned up {} old migrated requests".format(count))
                else:
                    print("No old requests to clean up")
                
        except Exception as e:
            print("Error cleaning up old requests: {}".format(e))


def main():
    parser = argparse.ArgumentParser(description='REST Capture Log Migration Helper')
    parser.add_argument('--database', '-d', required=True, help='Odoo database name')
    
    # Actions
    parser.add_argument('--export', action='store_true', help='Export requests to JSON')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--mark-migrated', action='store_true', help='Mark requests as migrated')
    parser.add_argument('--cleanup', action='store_true', help='Clean up old migrated requests')
    
    # Export options
    parser.add_argument('--output', '-o', help='Output file for export')
    parser.add_argument('--date-from', help='Filter from date (YYYY-MM-DD)')
    parser.add_argument('--date-to', help='Filter to date (YYYY-MM-DD)')
    parser.add_argument('--methods', help='Filter by HTTP methods (comma-separated)')
    parser.add_argument('--not-migrated', action='store_true', help='Only non-migrated requests')
    parser.add_argument('--status', help='Filter by processing status (comma-separated)')
    
    # Mark migrated options
    parser.add_argument('--request-ids', help='Request IDs to mark as migrated (comma-separated)')
    parser.add_argument('--notes', help='Migration notes')
    
    # Cleanup options
    parser.add_argument('--days-old', type=int, default=30, help='Days old for cleanup (default: 30)')
    
    args = parser.parse_args()
    
    if not any([args.export, args.stats, args.mark_migrated, args.cleanup]):
        parser.error('Must specify an action: --export, --stats, --mark-migrated, or --cleanup')
    
    helper = MigrationHelper(args.database)
    
    if args.export:
        if not args.output:
            parser.error('--output is required for export')
        
        filters = {}
        if args.date_from:
            filters['date_from'] = args.date_from
        if args.date_to:
            filters['date_to'] = args.date_to
        if args.methods:
            filters['methods'] = [m.strip().upper() for m in args.methods.split(',')]
        if args.not_migrated:
            filters['not_migrated'] = True
        if args.status:
            filters['status'] = [s.strip() for s in args.status.split(',')]
        
        helper.export_requests(args.output, filters)
    
    elif args.stats:
        helper.show_statistics()
    
    elif args.mark_migrated:
        if not args.request_ids:
            parser.error('--request-ids is required for mark-migrated')
        
        request_ids = [int(id.strip()) for id in args.request_ids.split(',')]
        helper.mark_as_migrated(request_ids, args.notes)
    
    elif args.cleanup:
        helper.cleanup_old_requests(args.days_old)


if __name__ == '__main__':
    main()