import random
from datetime import datetime

def load_csv():
    menu_file = 'menu.csv'   
    menu = {'items': []}
    
    try:
        with open(menu_file, 'r') as file:
            lines = file.readlines()
            header = lines[0].strip().split(',')  
            
            if header != ['ProductNumber', 'ProductName', 'category', 'price', 'stocksAmount']:
                print(f"Warning: Unexpected header format in {menu_file}")
                return menu 

            for line in lines[1:]:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) == 5:
                        menu['items'].append({ 
                            'ProductNumber': parts[0].strip(),
                            'ProductName': parts[1].strip(),
                            'category': parts[2].strip(),
                            'price': float(parts[3].replace('RM', '').strip()),
                            'stocksAmount': int(parts[4].strip())
                        })
                    else:
                        print(f"Warning: Invalid format in menu file line: {line}")

    except FileNotFoundError:
        print(f"Error: '{menu_file}' file not found")
        return menu

def display_menu(menu):
    items = menu['items']
    
    print('-' * 90)
    print(f"{'ProductNumber': <15}{'ProductName': <35}{'Category': <15}{'Price': <10}{'Stocks': <10}")
    print('-' * 90)
    
    for item in items:
        product_number = item.get('ProductNumber').strip()
        product_name = item.get('ProductName').strip()
        category = item.get('category').strip()
        price = item.get('price')
        stock = item.get('stocksAmount')
        
        print(
            f"{product_number: <15}"
            f"{product_name: <35}"
            f"{category: <15}"
            f"RM{price: <10.2f}"
            f"{stock: <10}"
        )
    
    print('-' * 90)

def manage_discount(menu):
    prod_num = input("Enter Product Number to apply discount: ")
    discount = float(input("Enter discount percentage (e.g., 10 for 10%): "))
    
    for item in menu['items']:
        if item['ProductNumber'] == prod_num:
            original_price = item['price']
            discounted_price = original_price - original_price * (discount / 100)
            item['price'] = discounted_price
            print(f"Discount applied: {item['ProductName']} new price is RM{item['price']:.2f} (was RM{original_price:.2f})")
            break
    else:
        print("Product not found!")

def generate_receipt(order_file='order.txt', receipt_file='cus_recp.txt'):
    print("Would you like to:")
    print("1. Print a receipt for an online order (existing order).")
    print("2. Create a new order.")
    
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        order_number = input("Enter the Order Number to print the receipt: ")
        try:
            with open(order_file, 'r') as file:
                lines = file.readlines()

            customer_name, order_status, items_brought, total = None, None, [], 0.0
            processing_order = False

            for i, line in enumerate(lines):
                line = line.strip()

                if f'Order Number: {order_number}' in line:
                    processing_order = True
                    customer_name = lines[i - 1].strip() if i > 0 else None

                if processing_order:
                    if 'Order Status:' in line:
                        order_status = line.split(': ')[1].strip().lower()
                    
                    elif any(char.isdigit() for char in line) and 'Total' not in line:
                        parts = line.split(',')
                        if len(parts) >= 2:
                            quantity_and_product = parts[0].strip()
                            product_price = parts[1].strip()  

                            quantity = int(quantity_and_product.split()[0])  
                            product_name = quantity_and_product[len(str(quantity)):].strip()  

                            price = float(product_price.replace('RM', '').strip().split('x')[0])  

                            items_brought.append(f"{quantity} * {product_name} - RM{price * quantity:.2f}")

                    elif 'Total:' in line:
                        total = float(line.split('RM')[1].strip())
                        break  

            if processing_order:
                if order_status in ['completed', 'order placed']:
                    bill_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
                    now = datetime.now()
                    date_time = now.strftime("%Y-%m-%d %H:%M:%S")

                    print_receipt(customer_name, items_brought, total, bill_id, date_time)
                    save_recp_file(customer_name, items_bought, total, bill_id, date_time, receipt_file)
                    update_order_status(order_number, 'Completed', order_file)
                    print(f"Order {order_number}'s status updated to 'Completed'.")
                elif order_status == 'cancelled':
                    print(f"Order {order_number} is cancelled. Receipt cannot be printed.")
                else:
                    print(f"Order {order_number} status is '{order_status}'. Receipt cannot be printed.")

        except FileNotFoundError:
            print(f"Error: '{order_file}' file not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    elif choice == '2':
        print("Create a new order functionality goes here.")
    else:
        print("Invalid choice. Please enter 1 or 2.")

def print_receipt(customer_name, items_bought, total, bill_id, date_time):
    print("\n--- RECEIPT ---")
    print("DATA INTO BAKERY SDN.BHD")
    print(f"Bill ID: {bill_id}")
    print(f"Date: {date_time}")
    print(f"Customer Name: {customer_name}")
    print("Order Summary:")
    for item in items_bought:
        print(item)
    print(f"Total: RM{total:.2f}")
    print("-" * 40)
    print(f"--- THANK YOU {customer_name}, SEE YOU NEXT TIME! ---")

def save_recp_file(customer_name, items_bought, total, bill_id, date_time, receipt_file):
    with open(receipt_file, 'a') as file:
        file.write("\n--- RECEIPT ---\n")
        file.write("DATA INTO BAKERY SDN.BHD\n")
        file.write(f"Bill ID: {bill_id}\n")
        file.write(f"Date: {date_time}\n")
        file.write(f"Customer Name: {customer_name}\n")
        file.write("Order Summary:\n")
        for item in items_bought:
            file.write(f"{item}\n")
        file.write(f"Total: RM{total:.2f}\n")
        file.write("--- THANK YOU, SEE YOU NEXT TIME! ---\n")

def update_order_status(order_number, new_status, order_file='order.txt'):
    try:
        with open(order_file, 'r') as file:
            lines = file.readlines()

        with open(order_file, 'w') as file:
            for line in lines:
                if f'Order Number: {order_number}' in line:
                    index = lines.index(line) + 1
                    if index < len(lines):
                        lines[index] = f"Order Status: {new_status}\n"
                file.write(line)
    except Exception as e:
        print(f"An error occurred while updating the order status: {e}")

def generate_reports(order_file='order.txt'):
    try:
        with open(order_file, 'r') as file:
            lines = file.readlines()

        sales_data = {}
        current_order = {}

        for line in lines:
            line = line.strip()
            if not line:  
                if current_order:
                    for item in current_order.get('Items', []):
                        product_name = item['ProductName']
                        quantity = item['Quantity']

                        if product_name not in sales_data:
                            sales_data[product_name] = {'total_sales': 0.0, 'order_count': 0}
                        
                        sales_data[product_name]['total_sales'] += item['Price'] * quantity
                        sales_data[product_name]['order_count'] += quantity

                    current_order = {}
                continue

            if 'Order Number:' in line:
                current_order['OrderNumber'] = line.split(': ')[1]
            elif 'Order Status:' in line:
                current_order['Status'] = line.split(': ')[1]
            elif any(char.isdigit() for char in line) and 'Total' not in line:
                parts = line.split(',')
                if len(parts) >= 2:
                    quantity_and_product = parts[0].strip()
                    product_name = quantity_and_product.split(',')[0].strip()  
                    quantity = int(quantity_and_product.split()[0])  

                    price = float(parts[1].replace('RM', '').strip().split('x')[0])  
                    current_order.setdefault('Items', []).append({
                        'ProductName': product_name,
                        'Quantity': quantity,
                        'Price': price
                    })

            elif 'Total:' in line:
                current_order['Total'] = float(line.split('RM')[1].strip())
                if current_order:
                    for item in current_order.get('Items', []):
                        product_name = item['ProductName']
                        quantity = item['Quantity']

                        if product_name not in sales_data:
                            sales_data[product_name] = {'total_sales': 0.0, 'order_count': 0}
                        
                        sales_data[product_name]['total_sales'] += item['Price'] * quantity
                        sales_data[product_name]['order_count'] += quantity
                    
                    current_order = {}

        print("\n--- SALES PERFORMANCE REPORT ---")
        print(f"{'ProductName': <35}{'Total Sales (RM)': <20}{'Order Count': <15}")
        print("-" * 70)
        
        for product, data in sales_data.items():
            print(f"{product: <35}{data['total_sales']:<20.2f}{data['order_count']:<15}")

    except FileNotFoundError:
        print(f"Error: '{order_file}' file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    menu = load_csv()
    
    while True:
        print("Welcome to the Bakery Management System")
        print("1. Display Menu")
        print("2. Manage Discounts")
        print("3. Generate Receipt")
        print("4. Generate Sales Reports")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ")
        
        if choice == '1':
            display_menu(menu)
        elif choice == '2':
            manage_discount(menu)
        elif choice == '3':
            generate_receipt()
        elif choice == '4':
            generate_reports()
        elif choice == '5':
            print("Exiting system.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    main()
