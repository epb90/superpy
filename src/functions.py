import csv
from datetime import date, datetime
from src.csv_manager import create_bought_csv_if_not_exists, append_row_to_bought_csv, append_row_to_sold_csv, get_bought_product_info
from src.csv_manager import generate_unique_sold_id

# Function to handle 'buy' command
def buy_product(args):
    product_name = args.product_name
    price = args.price
    expiration_date = args.expiration_date

    # Get today's date
    today = date.today().strftime('%Y-%m-%d')

    # Ensure that the bought.csv file exists with the correct structure
    create_bought_csv_if_not_exists()

    # Append bought product information to bought.csv
    row = [product_name, today, price, expiration_date]
    append_row_to_bought_csv(row)


# Function to handle 'sell' command
def sell_product(args):
    product_name = args.product_name
    price = args.price

    # Get today's date
    today = date.today().strftime('%Y-%m-%d')

    # Get product information from bought.csv
    product_info = get_bought_product_info(product_name)

    if product_info:
        # Product found in inventory
        bought_id, expiration_date = product_info

        # Generate a unique sold_id for the sale
        sold_id = generate_unique_sold_id()

        # Append sold product information to sold.csv
        row = [sold_id, bought_id, product_name, today, price]
        append_row_to_sold_csv(row)

        print("Product sold successfully.")
    else:
        print("Product not found in inventory.")

# Function to handle 'report' command
def generate_report(args):
    report_type = args.report_type
    date = args.date if hasattr(args, 'date') else None
    transaction_type = args.transaction_type if hasattr(args, 'transaction_type') else None
    report = report_generator.get_report(report_type, date, transaction_type)

    if report:
        print(f"{report_type.capitalize()} Report:")
        print(report)
    else:
        print(f"No {report_type} data available.")