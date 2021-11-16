import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures input from the user
    While loop above and if statement below + setting return False/True allow us to run the input again in case invalid values without need of restarting the program
    This block of code will run unless the data are valid
    Run a while loop to collect a valid string of data from the user via
    terminal, which must be a string of 6 numbers separated by commas. 
    The loop will repeatedly request data, until it is valid
    """
    while True:
        print("Please enter sales date from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
    
        """
        The split() method returns the broken up values as a list.
        # print(sales_data) Prints sales data separated by a comma with split() into terminal.
        """
        sales_data = data_str.split(",")
        
        """
        While loop above and if statement below + setting return False/True allow us to run the input again in case invalid values without need of restarting the program
        This block of code will run until the data are valid
        """
        if validate_data(sales_data):
            print("Data is valid")
            break

    return sales_data

def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Riases ValueError if strings cannot be converted into int, or if there aren't exactly 6 values. 
    """
    try:
        [int(value) for value in values] # converts the string inserted by user in sales_data variable into integers(whole numbers)
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True


def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales") # the value "sales" relates to the name of the worksheet in our google spreadsheet
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplis indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    print(stock_row)

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)

print("Welcome to Love Sandwiches Data Automation")
main()