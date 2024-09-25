# Load CSV file manually without using csv module
def load_csv():
    csv_file = 'menu.csv'   # Hardcoded filename for the menu
    data = {'items': []}
    
    try:
        with open('menu.csv', 'r') as menu_file:
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
    items = menu.get('items', [])
    
    print('-' * 90 + '\nProductNumber\tProductName\t\t\tCategory\tPrice\t\tStocks\n' + '-' * 90)
    
    for item in items:
        product_number = item.get('ProductNumber')
        product_name = item.get('ProductName')
        category = item.get('Category')
        price = item.get('Price')
        stock = item.get('StocksAmount')
        
        # Print formatted output
        print(
            f"{product_number: <10}"
            f"{product_name: <30}"
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
            original_price = float(item['Price'])
            item['Price'] = str(original_price - original_price * (discount / 100))
            print(f"Discount applied: {item['ProductName']} new price is ${item['Price']} (was ${original_price})")
            break
    else:
        print("Product not found!")

# Complete transaction and generate receipt
def complete_transaction(menu):
    total = 0
    items_bought = []
    
    while True:
        prod_num = input("Enter Product Number to purchase (or 'done' to finish): ")
        if prod_num == 'done':
            break
        for item in menu['items']:
            if item['ProductNumber'] == prod_num and int(item['StocksAmount']) > 0:
                quantity = int(input(f"How many {item['ProductName']}s? "))
                if quantity <= int(item['StocksAmount']):
                    total += float(item['Price']) * quantity
                    item['StocksAmount'] = str(int(item['StocksAmount']) - quantity)
                    items_bought.append(f"{item['ProductName']} (x{quantity}) - ${float(item['Price']) * quantity}")
                else:
                    print(f"Only {item['StocksAmount']} left in stock.")
                break
        else:
            print("Product not found or out of stock!")

    print("\n--- Receipt ---")
    for order in items_bought:
        print(order)
    print(f"Total: ${total}\n")
    
    write_receipt(items_bought, total)

# Write receipt to a text file
def write_receipt(items_bought, total, receipt_file='cus_recp.txt'):
    with open(receipt_file, mode='a') as file:
        file.write("\n--- Receipt ---\n")
        for order in items_bought:
            file.write(order + '\n')
        file.write(f"Total: ${total}\n\n")

# Generate sales report
def generate_report(menu):
    print("\nSales Report")
    for item in menu['items']:
        print(f"{item['ProductName']} - Remaining Stock: {item['StocksAmount']}")

# Main function to operate the system
def main():
    data = load_csv()  # Load the menu from the CSV
    
    while True:
        print("\nBakery Management System - Cashier")
        print("1. Display Menu")
        print("2. Manage Discount")
        print("3. Complete Transaction")
        print("4. Generate Sales Report")
        print("5. Exit")
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
            print("Exiting system...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
