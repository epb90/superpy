import csv
import os

DATA_FOLDER = 'data'

def create_bought_csv_if_not_exists():
    file_path = os.path.join(DATA_FOLDER, 'bought.csv')
    headers = ['id', 'product_name', 'buy_date', 'buy_price', 'expiration_date']
    create_csv_file_if_not_exists(file_path, headers)

def create_sold_csv_if_not_exists():
    file_path = os.path.join(DATA_FOLDER, 'sold.csv')
    headers = ['id', 'bought_id', 'product_name', 'sell_date', 'sell_price']
    create_csv_file_if_not_exists(file_path, headers)

def create_csv_file_if_not_exists(file_path, headers):
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

def append_row_to_bought_csv(row):
    file_path = os.path.join(DATA_FOLDER, 'bought.csv')
    append_row_to_csv(file_path, row)

def append_row_to_sold_csv(row):
    file_path = os.path.join(DATA_FOLDER, 'sold.csv')
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)

def append_row_to_csv(file_path, row):
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)

def get_bought_product_info(product_name):
    file_path = os.path.join(DATA_FOLDER, 'bought.csv')
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['product_name'] == product_name:
                return row['id'], row['expiration_date']
    return None, None

def generate_unique_sold_id():
    file_path = os.path.join(DATA_FOLDER, 'sold.csv')
    if not os.path.exists(file_path):
        create_sold_csv_if_not_exists()
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        sold_ids = [int(row[0]) for row in reader if row]
    return max(sold_ids) + 1 if sold_ids else 1