import csv
import os
import datetime

DATA_FOLDER = 'data'
CURRENT_DATE_FILE = os.path.join(DATA_FOLDER, 'current_date.csv')

def create_data_folder_if_not_exists():
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

def create_current_date_file_if_not_exists():
    if not os.path.exists(CURRENT_DATE_FILE):
        with open(CURRENT_DATE_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['current_date'])
            writer.writerow([datetime.datetime.now().strftime('%Y-%m-%d')])

def write_current_date_to_file(date: datetime.datetime):
    create_data_folder_if_not_exists()
    create_current_date_file_if_not_exists()
    with open(CURRENT_DATE_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date.strftime('%Y-%m-%d')])

def read_current_date_from_file():
    create_data_folder_if_not_exists()
    create_current_date_file_if_not_exists()
    with open(CURRENT_DATE_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        last_row = None
        for row in reader:
            if row:
                last_row = row
        if last_row:
            return datetime.datetime.strptime(last_row[0], '%Y-%m-%d')
    return datetime.datetime.now()

def set_current_date(args):
    if args is None or args.date is None:
        print("Please provide a date to set as the current date.")
        return

    try:
        new_current_date = datetime.datetime.strptime(args.date, '%Y-%m-%d')
        write_current_date_to_file(new_current_date)
        print(f"Today's date set to: {new_current_date.strftime('%Y-%m-%d')}")
    except ValueError as e:
        print(f"Invalid date format. Please enter a date in the format 'YYYY-MM-DD'.")

def get_current_date():
    current_date = read_current_date_from_file()
    return current_date.strftime('%Y-%m-%d')

def advance_date(args):
    if args.days is None:
        print("Please provide the number of days to advance.")
        return

    current_date = read_current_date_from_file()
    new_date = current_date + datetime.timedelta(days=args.days)
    write_current_date_to_file(new_date)
    print(f"Current date advanced by {args.days} days. New date: {new_date.strftime('%Y-%m-%d')}")

def reset_date(args):
    current_date = datetime.datetime.now()
    write_current_date_to_file(current_date)
    current_date_from_file = read_current_date_from_file()
    print(f"Current date: {current_date_from_file.strftime('%Y-%m-%d')}")

def handle_time_command(args):
    if args.time_subcommand == 'advance_date':
        advance_date(args)
    elif args.time_subcommand == 'set_current_date':
        set_current_date(args)
    elif args.time_subcommand == 'get_current_date':
        print(get_current_date())
    elif args.time_subcommand == 'reset_date':
        reset_date()  # Call reset_date without passing args

