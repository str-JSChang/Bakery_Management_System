import random
from datetime import datetime

# Load CSV file manually without using csv module
def load_csv():
    csv_file = 'menu.csv'   # Hardcoded filename for the menu
    data = {'items': []}
    
    try:
        with open(csv_file, 'r') as menu_file:
            lines = menu_file.readlines()
            headers = lines[0].strip().split(',')  # Extract headers
            
            for line in lines[1:]:  # Skip header line
                values = line.strip().split(',')
                item = dict(zip(headers, values))  # Combine headers with values
                data['items'].append(item)
        return data
    except FileNotFoundError:
        print(f"Error: '{csv_file}' file not found.")
        return data

# Display Menu
def display_menu(menu):
    items = menu['items']
    
    print('-' * 90)
    print(f"{'ProductNumber': <15}{'ProductName': <35}{'Category': <15}{'Price': <10}{'Stocks': <10}")
    print('-' * 90)
    
    for item in items:
        product_number = item.get('ProductNumber').strip()
        product_name = item.get('ProductName').strip()
        category = item.get('category').strip()
        price = item.get('price').strip()
        stock = item.get('stocksAmount').strip()
        
        # Print formatted output
        print(
            f"{product_number: <15}"
            f"{product_name: <35}"
            f"{category: <15}"
            f"{price: <10}"
            f"{stock: <10}"
        )
    
    print('-' * 90)

# Apply discounts to items
def manage_discount(menu):
    prod_num = input("Enter Product Number to apply discount: ")
    discount = float(input("Enter discount percentage (e.g., 10 for 10%): "))
    for item in menu['items']:
        if item['ProductNumber'] == prod_num:
            original_price = float(item['price'].replace('RM', ''))  # Removing 'RM' for calculation
            discounted_price = original_price - original_price * (discount / 100)
            item['price'] = f"RM{discounted_price:.2f}"
            print(f"Discount applied: {item['ProductName']} new price is {item['price']} (was RM{original_price:.2f})")
            break
    else:
        print("Product not found!")

# Complete transaction and generate receipt
def complete_transaction(menu):
    total = 0
    items_bought = []
    quantity_sold = {}

    customer_name = input("Enter Customer Name: ")

    while True:
        prod_num = input("Enter Product Number to purchase (or 'done' to finish): ")
        if prod_num == 'done':
            break
        for item in menu['items']:
            if item['ProductNumber'] == prod_num and int(item['stocksAmount']) > 0:
                quantity = int(input(f"How many {item['ProductName']}s? "))
                if quantity <= int(item['stocksAmount']):
                    total += float(item['price'].replace('RM', '')) * quantity
                    item['stocksAmount'] = str(int(item['stocksAmount']) - quantity)
                    items_bought.append(f"{quantity} * {item['ProductName'].strip()} - RM{float(item['price'].replace('RM', '')) * quantity:.2f}")
                    # Track the quantity sold for the product
                    if item['ProductName'] in quantity_sold:
                        quantity_sold[item['ProductName']] += quantity
                    else:
                        quantity_sold[item['ProductName']] = quantity
                else:
                    print(f"Only {item['stocksAmount']} left in stock.")
                break
        else:
            print("Product not found or out of stock!")

    # Generate a unique bill ID (random alphanumeric string)
    bill_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))

    # Get current date and time
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # Print the receipt on screen
    print("\n--- RECEIPT ---")
    print("DATA INTO BAKERY SDN.BHD")
    print(f"WELCOME {customer_name}")
    print(f"Bill ID: {bill_id}")
    print(f"Date: {date_time}")
    print("-" * 40)
    print(f"Customer Name: {customer_name}")
    print("Order Summary:")
    for order in items_bought:
        print(order)
    print(f"Total: RM{total:.2f}")
    print("-" * 40)
    print(f"--- THANK YOU {customer_name}, SEE YOU NEXT TIME! ---")

    # Write the receipt to a file
    write_receipt(customer_name, items_bought, total, bill_id, date_time, quantity_sold)

# Write receipt to a text file
def write_receipt(customer_name, items_bought, total, bill_id, date_time, quantity_sold, receipt_file='cus_recp.txt'):
    with open(receipt_file, mode='a') as file:
        file.write("\n--- RECEIPT ---\n")
        file.write("DATA INTO BAKERY SDN.BHD\n")
        file.write(f"WELCOME {customer_name}\n")
        file.write(f"Bill ID: {bill_id}\n")
        file.write(f"Date: {date_time}\n")
        file.write("-" * 40 + "\n")
        file.write(f"Customer Name: {customer_name}\n")
        file.write("Order Summary:\n")
        for order in items_bought:
            file.write(order + '\n')
        file.write(f"Total: RM{total:.2f}\n")
        file.write("-" * 40 + "\n")
        file.write(f"--- THANK YOU {customer_name}, SEE YOU NEXT TIME! ---\n\n")
        
        # Log quantities sold
        for product, quantity in quantity_sold.items():
            file.write(f"{product}: {quantity} sold\n")

# Generate sales report
def generate_report(menu):
    print("\nSales Report")
    for item in menu['items']:
        print(f"{item['ProductName']} - Remaining Stock: {item['stocksAmount']}")

# Generate sales performance report
def generate_sales_performance_report(receipt_file='cus_recp.txt'):
    sales_data = {}
    
    try:
        with open(receipt_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if "sold" in line:
                    product_info = line.split(': ')
                    if len(product_info) == 2:
                        product_name = product_info[0]
                        quantity_sold = int(product_info[1].strip().replace(' sold', ''))  # Remove ' sold' before converting to int
                        if product_name in sales_data:
                            sales_data[product_name] += quantity_sold
                        else:
                            sales_data[product_name] = quantity_sold

        print("\nSales Performance Report")
        print('-' * 40)
        for product, quantity in sales_data.items():
            print(f"{product}: {quantity} sold")
        print('-' * 40)

    except FileNotFoundError:
        print(f"Error: '{receipt_file}' file not found.")

# Main function to operate the system
def main():
    data = load_csv()  # Load the menu from the CSV
    
    while True:
        print("\nBakery Management System - Cashier")
        print("1. Display Menu")
        print("2. Manage Discount")
        print("3. Complete Transaction")
        print("4. Generate Sales Report")
        print("5. Generate Sales Performance Report")
        print("6. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            display_menu(data)  # Pass the menu data to the function
        elif choice == '2':
            manage_discount(data)
        elif choice == '3':
            complete_transaction(data)
        elif choice == '4':
            generate_report(data)
        elif choice == '5':
            generate_sales_performance_report()  # Generate the sales performance report
        elif choice == '6':
            print("Exiting system...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
