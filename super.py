# Imports
import argparse
import csv
from datetime import datetime
from src.functions import buy_product, sell_product
from src.time_manager import set_current_date, advance_date, handle_time_command, reset_date
from src.report_generator import get_inventory_report, get_revenue_report, get_profit_report, get_transactions_report


# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"



# Your code below this line.
def main():
    parser = argparse.ArgumentParser(description='SuperPy - Supermarket Inventory Management')

    subparsers = parser.add_subparsers(title='subcommands', dest='subcommand')

# Subparser for 'buy' command
    buy_parser = subparsers.add_parser('buy', help='Buy a product')
    buy_parser.add_argument('--product-name', required=True, help='Name of the product to buy')
    buy_parser.add_argument('--price', type=float, required=True, help='Price of the product')
    buy_parser.add_argument('--expiration-date', required=True, help='Expiration date of the product (format: YYYY-MM-DD)')
    buy_parser.set_defaults(func=buy_product)

    # Subparser for 'sell' command
    sell_parser = subparsers.add_parser('sell', help='Sell a product')
    sell_parser.add_argument('--product-name', required=True, help='Name of the product to sell')
    sell_parser.add_argument('--price', type=float, required=True, help='Price at which the product is sold')
    sell_parser.set_defaults(func=sell_product)

    # Subparser for 'report' command
    report_parser = subparsers.add_parser('report', help='Generate reports')
    report_subparsers = report_parser.add_subparsers(title='report_subcommands', dest='report_subcommand')

    # Subparser for 'inventory' report
    inventory_parser = report_subparsers.add_parser('inventory', help='Generate an inventory report')
    inventory_parser.add_argument('-v', '--verbose', action='store_true', help='Display detailed information in the report')
    inventory_parser.set_defaults(func=get_inventory_report)

    # Subparser for 'revenue' report
    revenue_parser = report_subparsers.add_parser('revenue', help='Generate a revenue report')
    revenue_parser.add_argument('-v', '--verbose', action='store_true', help='Display detailed information in the report')
    revenue_parser.add_argument('--date', type=lambda s: datetime.strptime(s, '%Y-%m-%d').date(), help='The date for the revenue report (format: YYYY-MM-DD)')
    revenue_parser.set_defaults(func=get_revenue_report)

    # Subparser for 'profit' report
    profit_parser = report_subparsers.add_parser('profit', help='Generate a profit report')
    profit_parser.add_argument('-v', '--verbose', action='store_true', help='Display detailed information in the report')
    profit_parser.add_argument('--date', type=str, help='The date for which to generate the profit report')
    profit_parser.set_defaults(func=get_profit_report)

    # Subparser for 'transactions' report
    transactions_parser = report_subparsers.add_parser('transactions', help='Generate a transactions report')
    transactions_parser.add_argument('--date', required=True, help='Date of the transactions (format: YYYY-MM-DD)')
    transactions_parser.add_argument('--transaction-type', required=True, choices=['buying', 'selling'], help='Type of the transactions (buying or selling)')
    transactions_parser.set_defaults(func=get_transactions_report)

    # Subparser for 'time' command
    time_parser = subparsers.add_parser('time', help='Manage application time')
    time_subparsers = time_parser.add_subparsers(title='time_subcommands', dest='time_subcommand')

    # Subparser for 'advance_date' command
    advance_date_parser = time_subparsers.add_parser('advance_date', help='Advance the current date by a specified number of days')
    advance_date_parser.add_argument('days', type=int, help='Number of days to advance', nargs='?')  # Make days optional
    advance_date_parser.set_defaults(func=advance_date)


    # Subparser for 'set_current_date' command
    set_current_date_parser = time_subparsers.add_parser('set_current_date', help='Set the current date (format: YYYY-MM-DD)')
    set_current_date_parser.add_argument('date', help='Date to set as the current date (format: YYYY-MM-DD)')
    set_current_date_parser.set_defaults(func=set_current_date)


    # Subparser for 'get_current_date' command
    current_date_parser = time_subparsers.add_parser('get_current_date', help='Get the current date of the application')
    current_date_parser.set_defaults(func=handle_time_command)

    # Subparser for 'reset_date' command
    reset_date_parser = time_subparsers.add_parser('reset_date', help='Reset the current date to real-life time')
    reset_date_parser.set_defaults(func=reset_date)

    args = parser.parse_args()
    if args.subcommand is None:
        parser.print_help()
    elif args.subcommand == 'time':
        if args.time_subcommand is None:
            time_parser.print_help()
        else:
            result = args.func(args)
            if result is not None:
                print(result)
    else:
        result = args.func(args)
        if result is not None:
            print(result)

if __name__ == "__main__":
    main()