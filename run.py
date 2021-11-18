import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

"""
Full functionality of the code you find in Love sandwiches challenge
at the end of the Python essentials
"""

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

"""
Refactorin of update_sales_worksheet and update_surplus_worksheet
in update_worksheet(data, worksheet) function

def update_sales_worksheet(data):
    
    Update sales worksheet, add new row with the list data provided
    
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales") # the value "sales" relates to the name of the worksheet in our google spreadsheet
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")


def update_surplus_worksheet(data):
    
    Update surplus worksheet, add new row with the list data provided
    
    print("Updating surplus worksheet...\n")
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n")
"""

def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplis indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data

def get_last_5_entries_sales():
    """
    Collects collumns of data from sales worksheet, collecting
    last 5 entries for each sandwich and returns the data 
    as a list of lists.
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])

    return columns

def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []
    
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column) # sum(int_column)/5 would also work as we know the length of our data
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")
    

print("Welcome to Love Sandwiches Data Automation")
main()