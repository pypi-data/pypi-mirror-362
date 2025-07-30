#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Replay Helper Script for REST Capture Log Module

This script reads a JSON file of captured REST requests (exported by
migration_helper.py) and replays them against a target Odoo 17 server.

Usage:
    # Dry run: show what would be done without sending requests
    python replay_to_odoo17.py \\
        --input-file requests.json \\
        --target-url http://odoo17.local:8069 \\
        --dry-run

    # Actual run: send requests to Odoo 17
    python replay_to_odoo17.py \\
        --input-file requests.json \\
        --target-url https://odoo17.mycompany.com \\
        --header "Authorization: Bearer my-secret-token" \\
        --delay 0.2

"""

import argparse
import json
import sys
import time
from urllib.parse import urlparse, urlunparse

try:
    import requests
except ImportError:
    print("Error: 'requests' library is not installed.")
    print("Please install it using: pip install requests")
    sys.exit(1)


def replay_requests(input_file, target_url, custom_headers, delay, dry_run=False):
    """
    Reads requests from the input file and replays them to the target URL.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        all_requests = data.get('requests', [])
        if not all_requests:
            print("No requests found in the input file.")
            return

    except (IOError, json.JSONDecodeError) as e:
        print("Error reading or parsing input file '{}': {}".format(input_file, e))
        return

    print("Found {} requests to process.".format(len(all_requests)))

    successful_ids = []
    failed_count = 0
    success_count = 0
    
    target_base = urlparse(target_url)

    for i, log in enumerate(all_requests):
        try:
            method = log['http_method']
            original_url = urlparse(log['request_url'])
            body = log.get('request_body')
            log_id = log['id']
            
            # Reconstruct URL for the new target
            new_url_parts = (
                target_base.scheme,
                target_base.netloc,
                original_url.path,
                original_url.params,
                original_url.query,
                original_url.fragment,
            )
            final_url = urlunparse(new_url_parts)

            # Prepare headers
            headers = json.loads(log['request_headers']) if log.get('request_headers') else {}
            # Remove headers that are managed by the `requests` library
            for h_key in ['Host', 'Content-Length', 'Connection', 'User-Agent']:
                headers.pop(h_key, None)
            
            # Apply custom headers from command line, overwriting existing ones
            if custom_headers:
                headers.update(custom_headers)
            
            print("\n--- [ {}/{} ] ---".format(i + 1, len(all_requests)))
            print("Replaying request ID: {}".format(log_id))
            print("{} {}".format(method, final_url))

            if dry_run:
                print("-> DRY RUN: Request not sent.")
                success_count += 1 # In dry-run we assume success for planning
                successful_ids.append(log_id)
                continue

            # Make the actual request
            response = requests.request(
                method,
                final_url,
                headers=headers,
                data=body.encode('utf-8') if body else None,
                timeout=30 # 30 seconds timeout
            )

            print("-> Status: {} {}".format(response.status_code, response.reason))

            if response.ok:
                success_count += 1
                successful_ids.append(log_id)
            else:
                failed_count += 1
                print("-> Response Body: {}".format(response.text[:200])) # Print first 200 chars of error

            time.sleep(delay)

        except requests.RequestException as e:
            failed_count += 1
            print("-> ERROR: Request failed: {}".format(e))
        except Exception as e:
            failed_count += 1
            print("-> ERROR: An unexpected error occurred: {}".format(e))

    print("\n" + "="*30)
    print("      Replay Summary")
    print("="*30)
    print("Total Requests Processed: {}".format(len(all_requests)))
    print("Successful: {}".format(success_count))
    print("Failed:     {}".format(failed_count))
    print("="*30)

    if successful_ids:
        print("\nTo mark successful requests as migrated in Odoo 12, run the following command:")
        print("You will need to replace YOUR_O12_DB with your Odoo 12 database name.")
        
        # Format IDs for easy copy-pasting
        ids_str = ",".join(map(str, successful_ids))
        
        print("\npython /path/to/migration_helper.py --database YOUR_O12_DB --mark-migrated --request-ids '{}'".format(ids_str))


def main():
    parser = argparse.ArgumentParser(
        description='Replay captured Odoo 12 REST requests to an Odoo 17 instance.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        '--input-file', '-i',
        required=True,
        help='JSON file with captured requests (exported from migration_helper.py).'
    )
    parser.add_argument(
        '--target-url', '-t',
        required=True,
        help='Base URL of the target Odoo 17 server (e.g., http://localhost:8069).'
    )
    parser.add_argument(
        '--header', '-H',
        action='append',
        help='Custom header to add to requests (e.g., -H "Authorization: Bearer <token>"). Can be used multiple times.'
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=0.1,
        help='Delay in seconds between requests (default: 0.1).'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate the run without sending any actual HTTP requests.'
    )
    
    args = parser.parse_args()
    
    custom_headers = {}
    if args.header:
        for h in args.header:
            try:
                key, value = h.split(':', 1)
                custom_headers[key.strip()] = value.strip()
            except ValueError:
                print("Error: Invalid header format '{}'. Use 'Key: Value'.".format(h))
                sys.exit(1)

    replay_requests(args.input_file, args.target_url, custom_headers, args.delay, args.dry_run)


if __name__ == '__main__':
    main() 