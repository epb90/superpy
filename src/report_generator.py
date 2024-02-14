import csv
import os
from prettytable import PrettyTable
from datetime import datetime

def get_report(report_type, date=None, transaction_type=None):
    if report_type == 'inventory':
        return get_inventory_report()
    elif report_type == 'revenue':
        return get_revenue_report()
    elif report_type == 'profit':
        return get_profit_report()
    elif report_type == 'transactions':
        if date and transaction_type:
            return get_transactions_report(date, transaction_type)
        else:
            print("Please specify a date and a transaction type (buying or selling) for the transactions report.")
            return None
    else:
        print("Invalid report type. Please specify 'inventory', 'revenue', 'profit', or 'transactions'.")
        return None

def get_inventory_report(args):
    try:
        # Create a PrettyTable
        table = PrettyTable()
        table.field_names = ['id', 'product_name', 'buy_date', 'buy_price', 'expiration_date']

        with open('data/bought.csv', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                table.add_row(list(row.values()))

        # Convert the PrettyTable to a string and return it
        return str(table)

    except FileNotFoundError:
        # If the file is not found, return None
        return None

def get_revenue_report(args):
    # File path for the sold.csv file
    file_path = os.path.join('data', 'sold.csv')

    # The date provided by the user
    date = args.date

    try:
        # Create a PrettyTable
        table = PrettyTable()
        table.field_names = ['id', 'bought_id', 'product_name', 'sell_date', 'sell_price']

        # Initialize total revenue
        total_revenue = 0.0

        # Open the sold.csv file for reading
        with open(file_path, newline='') as file:
            reader = csv.DictReader(file)

            # Iterate through each row in the CSV file
            for row in reader:
                # Parse the sell date of the transaction
                sell_date = datetime.strptime(row['sell_date'], '%Y-%m-%d').date()

                # If the sell date matches the date provided by the user, add the transaction to the total revenue
                if not date or sell_date == date:
                    # Get the sell price from the row and convert it to float
                    sell_price = float(row['sell_price'])

                    # Add the sell price to the total revenue
                    total_revenue += sell_price

                    # Add the row to the table
                    table.add_row(list(row.values()))

        # Add the total revenue to the table
        table.add_row(['-', '-', '-', '-', f"Total: ${total_revenue:.2f}"])

        # Convert the PrettyTable to a string and return it
        return str(table)

    except FileNotFoundError:
        # If the file is not found, return None
        return None
    
def get_profit_report(args):
    # File paths for the bought.csv and sold.csv files
    bought_file_path = os.path.join('data', 'bought.csv')
    sold_file_path = os.path.join('data', 'sold.csv')

    # The date provided by the user, converted to a datetime.date object
    date = datetime.strptime(args.date, '%Y-%m-%d').date() if args.date else None

    # Load the bought items into a dictionary
    bought_items = {}
    with open(bought_file_path, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            bought_date = datetime.strptime(row['buy_date'], '%Y-%m-%d').date()
            if bought_date == date:
                bought_items[row['id']] = row

    # Load the sold items into a dictionary
    sold_items = {}
    with open(sold_file_path, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            sold_date = datetime.strptime(row['sell_date'], '%Y-%m-%d').date()
            if sold_date == date:
                sold_items[row['id']] = row

    # Initialize the total profit and the PrettyTable
    total_profit = 0.0
    table = PrettyTable(['id', 'bought_id', 'product_name', 'date', 'profit'])

    # After calculating the profit for sold items, calculate the expenses for bought items
    for item in bought_items.values():
        buy_price = float(item['buy_price'])
        total_profit -= buy_price
        table.add_row([item['id'], '-', item['product_name'], item['buy_date'], f"-${buy_price:.2f}"])

    # Add the profit for sold items to the table and the total profit
    for item in sold_items.values():
        sell_price = float(item['sell_price'])
        total_profit += sell_price
        table.add_row([item['id'], item['bought_id'], item['product_name'], item['sell_date'], f"${sell_price:.2f}"])

    # Add the total profit to the table
    table.add_row(['-', '-', '-', '-', f"Total: ${total_profit:.2f}"])

    # Convert the PrettyTable to a string and return it
    return str(table)

def get_transactions_report(args):
    # Parse the date provided by the user
    date = datetime.strptime(args.date, '%Y-%m-%d').date()

    # Determine the file to read from and the fields to display based on the transaction type
    if args.transaction_type == 'buying':
        file_name = 'data/bought.csv'
        date_field = 'buy_date'
        table_field_names = ['id', 'product_name', 'buy_date', 'buy_price']
    else:  # args.transaction_type == 'selling'
        file_name = 'data/sold.csv'
        date_field = 'sell_date'
        table_field_names = ['id', 'bought_id', 'product_name', 'sell_date', 'sell_price']

    try:
        # Create a PrettyTable
        table = PrettyTable()
        table.field_names = table_field_names

        # Read data from the appropriate file
        with open(file_name, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Parse the date of the transaction
                transaction_date = datetime.strptime(row[date_field], '%Y-%m-%d').date()

                # If the transaction date matches the date provided by the user, add the transaction to the table
                if transaction_date == date:
                    table.add_row([row[field] for field in table_field_names])

        # Convert the PrettyTable to a string and return it
        return str(table)

    except FileNotFoundError:
        return f"No {args.transaction_type} transactions data available."