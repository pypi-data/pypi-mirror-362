#!/usr/bin/env python3
"""
Command-line interface for Alpha Vantage Client.
"""

import argparse
import json
import os
import sys
from typing import Optional

from .client import AlphaVantageClient


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Alpha Vantage Client - A comprehensive Python client for Alpha Vantage API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all available endpoints
  alpha-vantage list

  # List economic endpoints
  alpha-vantage list --category economic

  # Get stock data
  alpha-vantage query time_series_daily --symbol AAPL

  # Get technical indicator
  alpha-vantage query sma --symbol AAPL --interval daily --series-type close --time-period 20

  # Get economic data
  alpha-vantage query real_gdp --interval quarterly
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List available endpoints')
    list_parser.add_argument('--category', help='Filter by category')
    list_parser.add_argument('--filter', help='Filter by name (partial match)')
    list_parser.add_argument('--detailed', action='store_true', help='Show detailed information')
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Query an endpoint')
    query_parser.add_argument('endpoint', help='Endpoint name to query')
    query_parser.add_argument('--api-key', help='Alpha Vantage API key')
    query_parser.add_argument('--symbol', help='Symbol/ticker')
    query_parser.add_argument('--interval', help='Time interval')
    query_parser.add_argument('--series-type', help='Series type (open, high, low, close)')
    query_parser.add_argument('--time-period', type=int, help='Time period')
    query_parser.add_argument('--outputsize', help='Output size (compact, full)')
    query_parser.add_argument('--datatype', help='Data type (json, csv)')
    query_parser.add_argument('--pretty', action='store_true', help='Pretty print JSON output')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'list':
            # For list command, we don't need an API key
            client = AlphaVantageClient(api_key="demo")  # Use demo key for listing
            endpoints = client.get_available_endpoints(
                detailed=args.detailed,
                category=args.category,
                filter_by=args.filter
            )
            print(endpoints)
            
        elif args.command == 'query':
            # Get API key for query command
            api_key = args.api_key or os.getenv('ALPHA_VANTAGE_API_KEY')
            if not api_key:
                print("Error: API key required. Set ALPHA_VANTAGE_API_KEY environment variable or use --api-key")
                sys.exit(1)
            
            client = AlphaVantageClient(api_key=api_key)
            
            # Build kwargs from arguments
            kwargs = {}
            for key, value in vars(args).items():
                if key not in ['command', 'endpoint', 'api_key', 'pretty'] and value is not None:
                    kwargs[key] = value
            
            # Remove None values
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            
            result = client.query(args.endpoint, **kwargs)
            
            if args.pretty and isinstance(result, dict):
                print(json.dumps(result, indent=2))
            else:
                print(result)
                
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 