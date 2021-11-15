import gspread
from google.oauth2.service_account import Credentials



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
    """
    print("Please enter sales date from the last market.")
    print("Data should be six numbers, separated by commas.")
    print("Example: 10,20,30,40,50,60\n")

    data_str = input("Enter your data here: ")
    

    sales_data = data_str.split(",") # The split() method returns the broken up values as a list.
    # print(sales_data) Prints sales data separated by a comma with split() into terminal.
    validate_data(sales_data)

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

get_sales_data()
