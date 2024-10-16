import random
from datetime import datetime

def load_csv(file_path='menu.csv'): 
    menu = {'items': []}
    try:
        with open(file_path, 'r') as file:
            for line in file.readlines()[1:]:  
                product_number, product_name, category, price, stock = line.strip().split(',')
                menu['items'].append({
                    'ProductNumber': product_number.strip(),
                    'ProductName': product_name.strip(),
                    'category': category.strip(),
                    'price': float(price.replace('RM', '').strip()),  
                    'stocksAmount': int(stock.strip())
                })
    except Exception as e:
        print(f"Error loading menu: {e}")
        return None

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

def generate_receipt(menu, order_file='order.txt', receipt_file='cus_recp.txt', completed_file='completed_order.txt'):
    print("Would you like to:")
    print("1. Print a receipt for an online order (existing order).")
    print("2. Create a new order.")
    
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        order_number = input("Enter the Order Number to print the receipt: ")
        try:
            with open(order_file, 'r') as file:
                lines = file.readlines()

            customer_name, order_status, items_bought, total = None, None, [], 0.0
            processing_order = False
            order_lines = []
            current_order = []

            for line in lines:
                line = line.strip()

                if f'Order Number: {order_number}' in line:
                    processing_order = True
                    current_order.append(line)
                    continue

                if processing_order:
                    
                    current_order.append(line)

                    if line and 'Order Status' not in line and 'Order Number:' not in line:
                        if customer_name is None:
                            customer_name = line

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

                            items_bought.append(f"{quantity} * {product_name} - RM{price * quantity:.2f}")

                    elif 'Total:' in line:
                        total = float(line.split('RM')[1].strip())
                        break  

            if processing_order:
                if order_status in ['completed', 'order placed']:
                    bill_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
                    now = datetime.now()
                    date_time = now.strftime("%Y-%m-%d %H:%M:%S")

                    print_receipt(customer_name, items_bought, total, bill_id, date_time)
                    save_recp_file(customer_name, items_bought, total, bill_id, date_time, receipt_file)
                    update_order_status(order_number, 'Completed', order_file)
                    print(f"Order {order_number}'s status updated to 'Completed'.")

                    with open(completed_file, 'a') as completed:
                        for order_line in current_order:
                            completed.write(order_line + '\n')

                    with open(order_file, 'w') as file:
                        for line in lines:
                            if line.strip() not in current_order:
                                file.write(line)

                elif order_status == 'cancelled':
                    print(f"Order {order_number} is cancelled. Receipt cannot be printed.")
                else:
                    print(f"Order {order_number} status is '{order_status}'. Receipt cannot be printed.")

        except FileNotFoundError:
            print(f"Error: '{order_file}' file not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    elif choice == '2':
        customer_name = input("Enter customer's name: ")
        items_bought = []
        total = 0.0
        order_number = random.randint(100, 999)  
        
        while True:
            product_number = input("Enter Product Number (or type 'done' to finish): ").strip()
            if product_number.lower() == 'done':
                break
            
            quantity = int(input(f"Enter quantity for product number {product_number}: "))
            
            product_found = False
            for item in menu['items']:
                if item['ProductNumber'] == product_number:
                    product_name = item['ProductName']
                    price = item['price']
                    stock = item['stocksAmount']
                    
                    if quantity > stock:
                        print(f"Insufficient stock for {product_name}. Only {stock} left.")
                    else:
                        item['stocksAmount'] -= quantity
                        total += price * quantity
                        items_bought.append(f"{quantity} * {product_name} - RM{price * quantity:.2f}")
                        product_found = True
                    break

            if not product_found:
                print(f"Product with Product Number {product_number} not found.")
         
        discount_choice = input("Would you like to apply a discount? (yes or no): ").strip().lower()
        if discount_choice == 'yes':
            discount = float(input("Enter discount percentage (e.g., 10 for 10%): "))
            total = total - total * (discount / 100)
            print(f"Discount of {discount}% applied. New total is RM{total:.2f}")

        bill_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        
        print_receipt(customer_name, items_bought, total, bill_id, date_time)
        save_recp_file(customer_name, items_bought, total, bill_id, date_time, receipt_file)

        try:
            with open(order_file, 'a') as file:
                file.write(f"{customer_name}\n")
                file.write(f"Order Number: {order_number}\n")
                file.write(f"Order Status: Order placed\n")
                for item in items_bought:
                    file.write(f"{item}\n")
                file.write(f"Total: RM{total:.2f}\n")
                file.write("\n")  
                
            print(f"New order successfully saved with Order Number: {order_number}")
        except Exception as e:
            print(f"Error writing to {order_file}: {e}")
            print("Please check file permissions or the file path.")

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

def calculate_total_sales(order_file='order.txt'):
    total_sales = 0.0
    
    try:
        with open(order_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if 'Total:' in line:
                    total_sales += float(line.split('RM')[1].strip())
    except FileNotFoundError:
        print(f"Error: '{order_file}' file not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    return total_sales

def calculate_profit(order_file='order.txt', inventory_file='inventory_cost.txt'):
    sales_total = calculate_total_sales(order_file)
    
    if sales_total is None:
        return None  
    
    inventory_cost = 0
    
    try:
        with open(inventory_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if 'RM' in line and 'Total' not in line:
                    cost = float(line.split('RM')[1].strip())
                    inventory_cost += cost
                elif 'Total' in line:
                    total_cost = float(line.split('RM')[1].strip())
                    break
    except FileNotFoundError:
        print(f"Error: '{inventory_file}' file not found.")
        return None

    profit = sales_total - inventory_cost
    return profit

def cashier_main():
    menu = load_csv()
    
    while True:
        print("Welcome to the Bakery Management System")
        print("1. Display Menu")
        print("2. Manage Discounts")
        print("3. Generate Receipt")
        print("4. Generate Sales Reports")
        print("5. Calculate The Total Profit")
        print("6. Exit Cashier Page")
        
        choice = input("Choose an option (1-6): ")
        
        if choice == '1':
            display_menu(menu)
        elif choice == '2':
            manage_discount(menu)
        elif choice == '3':
            generate_receipt(menu)
        elif choice == '4':
            generate_reports()
        elif choice == '5':
            profit = calculate_profit()  
            if profit is not None:
                print(f"Profit: RM{profit:.2f}")
        elif choice == '6':
            print("Exiting Bakery System: Cashier Page...")
            break
        else:
            print("Invalid choice, please try again.")

