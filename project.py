import pandas as pd
import csv
import json
from datetime import datetime
from colorama import init, Fore, Back, Style
import os

# Initialize colorama for colored output
init()

# Initialize colorama for Windows support
init()

# Constants
date_format = "%d-%m-%Y"
CONFIG_FILE = "finance_config.json"
DEFAULT_CONFIG = {
    "currency": {
        "symbol": "$",
        "code": "USD",
        "position": "before"  # or "after"
    },
    "categories": {
        "Income": [
            "Salary",
            "Freelance",
            "Investments",
            "Other Income"
        ],
        "Expense": [
            "Food",
            "Transportation",
            "Housing",
            "Utilities",
            "Healthcare",
            "Entertainment",
            "Shopping",
            "Other Expenses"
        ]
    }
}

CURRENCY_OPTIONS = {
    "1": {"symbol": "$", "code": "USD", "position": "before"},
    "2": {"symbol": "€", "code": "EUR", "position": "before"},
    "3": {"symbol": "£", "code": "GBP", "position": "before"},
    "4": {"symbol": "¥", "code": "JPY", "position": "before"},
    "5": {"symbol": "₹", "code": "INR", "position": "before"}
}


def get_date(prompt="Enter date (dd-mm-yyyy): ", allow_default=False, test_input=None):
    if test_input is not None:
        date_str = test_input
    else:
        date_str = input(f"{Fore.YELLOW}{prompt}{Style.RESET_ALL}")
        
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)

    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        if test_input is not None:
            raise ValueError("Invalid date format. Please use dd-mm-yyyy format")
        print(f"{Fore.RED}Invalid date format. Please enter the date in dd-mm-yyyy format{Style.RESET_ALL}")
        return get_date(prompt, allow_default)


def get_amount(test_input=None):
    try:
        if test_input is not None:
            amount = float(test_input)
        else:
            amount = float(input(f"{Fore.YELLOW}Enter the amount: {Style.RESET_ALL}"))
            
        if amount <= 0:
            raise ValueError("Amount must be a non-negative non-zero value.")
        return amount
    except ValueError as e:
        if test_input is not None:
            raise
        print(f"{Fore.RED}{str(e)}{Style.RESET_ALL}")
        return get_amount()


def get_category():
    config = load_config()
    
    print(f"\n{Fore.CYAN}Select Transaction Type:{Style.RESET_ALL}")
    print(f"1. Income")
    print(f"2. Expense")
    
    while True:
        type_choice = input(f"{Fore.YELLOW}Enter choice (1-2): {Style.RESET_ALL}")
        if type_choice == "1":
            category_type = "Income"
            break
        elif type_choice == "2":
            category_type = "Expense"
            break
        print(f"{Fore.RED}Invalid choice. Please enter 1 or 2.{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}Available {category_type} Categories:{Style.RESET_ALL}")
    categories = config["categories"][category_type]
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")
    
    while True:
        try:
            idx = int(input(f"{Fore.YELLOW}Enter category number: {Style.RESET_ALL}")) - 1
            if 0 <= idx < len(categories):
                return category_type, categories[idx]
            print(f"{Fore.RED}Invalid number. Please try again.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")
    


def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def format_amount(amount, currency):
    if currency["position"] == "before":
        return f"{currency['symbol']}{amount:,.2f}"
    return f"{amount:,.2f}{currency['symbol']}"

def set_currency():
    print(f"\n{Fore.CYAN}Available Currencies:{Style.RESET_ALL}")
    for key, curr in CURRENCY_OPTIONS.items():
        print(f"{Fore.YELLOW}{key}. {curr['symbol']} ({curr['code']}){Style.RESET_ALL}")
    
    while True:
        choice = input(f"\n{Fore.YELLOW}Select currency (1-{len(CURRENCY_OPTIONS)}): {Style.RESET_ALL}")
        if choice in CURRENCY_OPTIONS:
            config = load_config()
            config["currency"] = CURRENCY_OPTIONS[choice]
            save_config(config)
            print(f"{Fore.GREEN}Currency updated successfully!{Style.RESET_ALL}")
            return
        print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

def manage_categories():
    config = load_config()
    while True:
        print(f"\n{Fore.CYAN}Category Management{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1. View categories{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}2. Add category{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}3. Remove category{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}4. Back to main menu{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.GREEN}Enter your choice (1-4): {Style.RESET_ALL}")
        
        if choice == "1":
            print(f"\n{Fore.CYAN}Current Categories:{Style.RESET_ALL}")
            for type_name, categories in config["categories"].items():
                print(f"\n{Fore.YELLOW}{type_name}:{Style.RESET_ALL}")
                for cat in categories:
                    print(f"  • {cat}")
                    
        elif choice == "2":
            type_name = input(f"{Fore.YELLOW}Enter type (Income/Expense): {Style.RESET_ALL}").capitalize()
            if type_name in config["categories"]:
                new_cat = input(f"{Fore.YELLOW}Enter new category name: {Style.RESET_ALL}")
                if new_cat not in config["categories"][type_name]:
                    config["categories"][type_name].append(new_cat)
                    save_config(config)
                    print(f"{Fore.GREEN}Category added successfully!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Category already exists!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Invalid type. Use 'Income' or 'Expense'.{Style.RESET_ALL}")
                
        elif choice == "3":
            type_name = input(f"{Fore.YELLOW}Enter type (Income/Expense): {Style.RESET_ALL}").capitalize()
            if type_name in config["categories"]:
                print(f"\n{Fore.CYAN}Available categories:{Style.RESET_ALL}")
                for i, cat in enumerate(config["categories"][type_name], 1):
                    print(f"{i}. {cat}")
                try:
                    idx = int(input(f"{Fore.YELLOW}Enter number to remove: {Style.RESET_ALL}")) - 1
                    if 0 <= idx < len(config["categories"][type_name]):
                        removed = config["categories"][type_name].pop(idx)
                        save_config(config)
                        print(f"{Fore.GREEN}Removed category: {removed}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Invalid number!{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}Invalid input!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Invalid type. Use 'Income' or 'Expense'.{Style.RESET_ALL}")
                
        elif choice == "4":
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please enter 1-4.{Style.RESET_ALL}")


def export_data():
    config = load_config()
    while True:
        print(f"\n{Fore.CYAN}Export Options:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1. Export to Excel{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}2. Export to CSV{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}3. Back to main menu{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.GREEN}Enter your choice (1-3): {Style.RESET_ALL}")
        
        if choice in ["1", "2"]:
            try:
                df = pd.read_csv(CSV.CSV_FILE)
                if choice == "1":
                    output_file = "finance_export.xlsx"
                    df.to_excel(output_file, index=False)
                else:
                    output_file = "finance_export.csv"
                    df.to_csv(output_file, index=False)
                print(f"{Fore.GREEN}Data exported successfully to {output_file}!{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}Error exporting data: {str(e)}{Style.RESET_ALL}")
                break
        elif choice == "3":
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please enter 1-3.{Style.RESET_ALL}")

def get_description():
    return input(f"{Fore.YELLOW}Enter a description (optional): {Style.RESET_ALL}")


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "subcategory", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category_type, subcategory, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category_type,
            "subcategory": subcategory,
            "description": description,
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print(f"{Fore.GREEN}✓ Entry added successfully{Style.RESET_ALL}")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print(f"{Fore.YELLOW}⚠️  No transactions found in the given date range.{Style.RESET_ALL}")

        return filtered_df


def add():
    CSV.initialize_csv()
    date = get_date(
        "Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ",
        allow_default=True,
    )
    amount = get_amount()
    category_type, subcategory = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category_type, subcategory, description)


def format_transaction_table(df):
    """Format the transaction table with colors and alignment"""
    # Convert date to datetime for proper sorting
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    df = df.sort_values('date')
    
    config = load_config()
    currency = config["currency"]
    
    # Print transaction table header with blue borders
    print(f"\n{Fore.BLUE}╔{'═' * 86}╗{Style.RESET_ALL}")
    print(f"{Fore.BLUE}║{Fore.WHITE}{'Transaction History':^86}{Fore.BLUE}║{Style.RESET_ALL}")
    print(f"{Fore.BLUE}╠{'═' * 12}╦{'═' * 14}╦{'═' * 12}╦{'═' * 15}╦{'═' * 30}╣{Style.RESET_ALL}")
    print(f"{Fore.BLUE}║{Fore.WHITE}{'Date':^12}{Fore.BLUE}║{Fore.WHITE}{'Amount':^14}{Fore.BLUE}║{Fore.WHITE}{'Category':^12}{Fore.BLUE}║{Fore.WHITE}{'Subcategory':^15}{Fore.BLUE}║{Fore.WHITE}{'Description':^30}{Fore.BLUE}║{Style.RESET_ALL}")
    print(f"{Fore.BLUE}╠{'═' * 12}╬{'═' * 14}╬{'═' * 12}╬{'═' * 15}╬{'═' * 30}╣{Style.RESET_ALL}")
    
    # Print each transaction
    for _, row in df.iterrows():
        date_str = row['date'].strftime('%d-%m-%Y')
        amount_str = format_amount(row['amount'], currency)
        category_color = Fore.GREEN if row['category'] == 'Income' else Fore.RED
        
        print(f"{Fore.BLUE}║{Style.RESET_ALL}", end='')
        print(f"{date_str:^12}", end='')
        print(f"{Fore.BLUE}║{Style.RESET_ALL}", end='')
        print(f"{category_color}{amount_str:>14}{Style.RESET_ALL}", end='')
        print(f"{Fore.BLUE}║{Style.RESET_ALL}", end='')
        print(f"{category_color}{row['category']:^12}{Style.RESET_ALL}", end='')
        print(f"{Fore.BLUE}║{Style.RESET_ALL}", end='')
        print(f"{row['subcategory']:^15}", end='')
        print(f"{Fore.BLUE}║{Style.RESET_ALL}", end='')
        print(f"{row['description']:<30}", end='')
        print(f"{Fore.BLUE}║{Style.RESET_ALL}")
    
    print(f"{Fore.BLUE}╚{'═' * 12}╩{'═' * 14}╩{'═' * 12}╩{'═' * 15}╩{'═' * 30}╝{Style.RESET_ALL}\n")
    
    # Category Summary with magenta borders
    print(f"{Fore.MAGENTA}╔{'═' * 50}╗{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}║{Fore.WHITE}{'Category Summary':^50}{Fore.MAGENTA}║{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}╠{'═' * 25}╦{'═' * 24}╣{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}║{Fore.WHITE}{'Category/Subcategory':^25}{Fore.MAGENTA}║{Fore.WHITE}{'Amount':^24}{Fore.MAGENTA}║{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}╠{'═' * 25}╬{'═' * 24}╣{Style.RESET_ALL}")
    
    # Calculate category and subcategory totals
    categories = df.groupby(['category', 'subcategory'])['amount'].sum()
    
    current_category = None
    for (category, subcategory), amount in categories.items():
        if current_category != category:
            if current_category is not None:
                print(f"{Fore.MAGENTA}╟{'─' * 25}╫{'─' * 24}╢{Style.RESET_ALL}")
            current_category = category
            cat_total = df[df['category'] == category]['amount'].sum()
            category_color = Fore.GREEN if category == 'Income' else Fore.RED
            print(f"{Fore.MAGENTA}║{category_color}{category:^25}{Fore.MAGENTA}║{category_color}{format_amount(cat_total, currency):>24}{Style.RESET_ALL}{Fore.MAGENTA}║{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}║{Style.RESET_ALL} - {subcategory:<22}{Fore.MAGENTA}║{Style.RESET_ALL}{format_amount(amount, currency):>24}{Fore.MAGENTA}║{Style.RESET_ALL}")
    
    print(f"{Fore.MAGENTA}╚{'═' * 25}╩{'═' * 24}╝{Style.RESET_ALL}\n")
    
    # Financial Summary with cyan borders
    total_income = df[df['category'] == 'Income']['amount'].sum()
    total_expense = df[df['category'] == 'Expense']['amount'].sum()
    net_savings = total_income - total_expense
    
    print(f"{Fore.CYAN}╔{'═' * 45}╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Fore.WHITE}{'Financial Summary':^45}{Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╠{'═' * 45}╣{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} {'Total Income:':<25} {Fore.GREEN}{format_amount(total_income, currency):>17}{Style.RESET_ALL} {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} {'Total Expenses:':<25} {Fore.RED}{format_amount(total_expense, currency):>17}{Style.RESET_ALL} {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╟{'─' * 45}╢{Style.RESET_ALL}")
    savings_color = Fore.GREEN if net_savings >= 0 else Fore.RED
    print(f"{Fore.CYAN}║{Style.RESET_ALL} {'Net Savings:':<25} {savings_color}{format_amount(net_savings, currency):>17}{Style.RESET_ALL} {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚{'═' * 45}╝{Style.RESET_ALL}")


def display_menu():
    print(f"\n{Fore.CYAN}╔══════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║     Personal Finance Manager     ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╠══════════════════════════════════╣{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} 1. {Fore.YELLOW}📝 Add a new transaction{Style.RESET_ALL}      {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} 2. {Fore.YELLOW}📊 View transactions summary{Style.RESET_ALL}  {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} 3. {Fore.YELLOW}🚪 Exit{Style.RESET_ALL}                       {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════╝{Style.RESET_ALL}")

def display_menu():
    print(f"\n{Fore.CYAN}╔══════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║     Personal Finance Manager     ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╠══════════════════════════════════╣{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} 1. {Fore.YELLOW}📝 Add a new transaction{Style.RESET_ALL}      {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} 2. {Fore.YELLOW}📊 View transactions & summary{Style.RESET_ALL}{Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} 3. {Fore.YELLOW}💰 Manage categories{Style.RESET_ALL}          {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} 4. {Fore.YELLOW}💱 Change currency{Style.RESET_ALL}            {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} 5. {Fore.YELLOW}📤 Export data{Style.RESET_ALL}                {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} 6. {Fore.YELLOW}🚪 Exit{Style.RESET_ALL}                       {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════╝{Style.RESET_ALL}")

def main():
    # Initialize config if it doesn't exist
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)

    while True:
        display_menu()
        choice = input(f"{Fore.GREEN}Enter your choice (1-6): {Style.RESET_ALL}")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if not df.empty:
                format_transaction_table(df)
        elif choice == "3":
            manage_categories()
        elif choice == "4":
            set_currency()
        elif choice == "5":
            export_data()
        elif choice == "6":
            print(f"{Fore.GREEN}Thank you for using Personal Finance Manager!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}❌ Invalid choice. Please enter 1-6.{Style.RESET_ALL}")


if __name__ == "__main__":
    main()