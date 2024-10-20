import random
from datetime import datetime

def load_csv(menu_file='menu.csv'):
    try:
        with open(menu_file, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: '{menu_file}' file not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading the CSV: {e}")
        return None

    menu_items = []
    try:
        for line in lines[1:]:
            data = line.strip().split(',')
            item = {
                'ProductNumber': data[0],
                'ProductName': data[1],
                'Category': data[2],
                'price': float(data[3].replace("RM", "")),
                'stocksAmount': int(data[4]),
                'Discount': float(data[5])
            }
            menu_items.append(item)
    except (ValueError, IndexError) as e:
        print(f"Error processing line: {line}. Error: {e}")
        return None

    return {'items': menu_items}

def display_menu(menu):
    if not menu:
        print("Menu data is missing or couldn't be loaded.")
        return

    try:
        items = menu['items']
        print('-' * 90)
        print(f"{'ProductNumber': <15}{'ProductName': <35}{'Category': <15}{'Price': <10}{'Stocks': <10}{'Discount': <10}")
        print('-' * 90)

        for item in items:
            product_number = item['ProductNumber'].strip()
            product_name = item['ProductName'].strip()
            category = item['Category'].strip()
            price = item['price']
            stock = item['stocksAmount']
            discount = item['Discount']

            print(f"{product_number: <15}{product_name: <35}{category: <15}RM{price: <10.2f}{stock: <10}{discount: <10.2f}")

        print('-' * 90)
    except Exception as e:
        print(f"An error occurred while displaying the menu: {e}")

def manage_discount(menu_file='menu.csv'):
    try:
        prod_num = input("Enter Product Number: ")
        action = input("Enter apply, modify, or delete: ").strip().lower()

        with open(menu_file, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: '{menu_file}' file not found.")
        return
    except ValueError as e:
        print(f"Invalid input: {e}")
        return

    updated_lines = []
    product_found = False

    try:
        for line in lines:
            if line.startswith('ProductNumber'):
                updated_lines.append(line)
                continue

            data = line.strip().split(',')
            if data[0] == prod_num:
                product_found = True
                discounted_price = float(data[3].replace("RM", ""))  
                current_discount = float(data[5])  
                if action == 'apply':
                    discount = float(input("Enter discount percentage (e.g., 10 for 10%): "))
                    new_discounted_price = discounted_price - discounted_price * (discount / 100)
                    data[3] = f"RM{new_discounted_price:.2f}"
                    data[5] = f"{discount:.2f}"
                    print(f"Discount applied: {data[1]} new price is RM{new_discounted_price:.2f} (was RM{discounted_price:.2f})")

                elif action == 'modify':
                    print(f"Current discount: {current_discount}%")
                    new_discount = float(input(f"Enter new discount percentage (current: {current_discount}%): "))
                    new_discounted_price = discounted_price - discounted_price * (new_discount / 100)
                    data[3] = f"RM{new_discounted_price:.2f}"
                    data[5] = f"{new_discount:.2f}"
                    print(f"Discount modified: {data[1]} new price is RM{new_discounted_price:.2f} (was RM{discounted_price:.2f})")

                elif action == 'delete':
                    original_price = discounted_price * (100 + current_discount) / 100
                    data[3] = f"RM{original_price:.2f}"
                    data[5] = "0.00"  
                    print(f"Discount removed: {data[1]} price restored to RM{original_price:.2f}")

            updated_lines.append(','.join(data) + '\n')

        if not product_found:
            print("Product not found!")
            return

        with open(menu_file, 'w') as file:
            file.writelines(updated_lines)
    except Exception as e:
        print(f"An error occurred while managing the discount: {e}")

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

            current_order = []
            processing_order = False
            customer_name = None

            for i, line in enumerate(lines):
                line = line.strip()

                if 'Customer name:' in line:
                    customer_name = line.split('Customer name: ')[1]

                if f'Order Number: {order_number}' in line:
                    processing_order = True
                    current_order.append(line)
                    continue

                if processing_order:
                    current_order.append(line)
                    if 'Total:' in line:  
                        break

            if current_order:  
                bill_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
                now = datetime.now()
                date_time = now.strftime("%Y-%m-%d %H:%M:%S")

                items_bought = [line for line in current_order if '*' in line]
                total_line = next((line for line in current_order if 'Total:' in line), None)
                total = float(total_line.split('RM')[1].strip()) if total_line else 0.0

                print_receipt(customer_name, items_bought, total, bill_id, date_time)
                save_recp_file(customer_name, items_bought, total, bill_id, date_time, receipt_file)

                with open(completed_file, 'a') as completed:
                    completed.write(f"Customer Name: {customer_name}\n")
                    for order_line in current_order:
                        completed.write(order_line + '\n')
                    completed.write("\n")

                update_order_status(order_number, 'Completed', order_file)

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

            try:
                quantity = int(input(f"Enter quantity for product number {product_number}: "))
            except ValueError:
                print("Invalid input for quantity.")
                continue

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
            try:
                discount = float(input("Enter discount percentage (e.g., 10 for 10%): "))
                total = total - total * (discount / 100)
                print(f"Discount of {discount}% applied. New total is RM{total:.2f}")
            except ValueError:
                print("Invalid input for discount.")

        bill_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")

        print_receipt(customer_name, items_bought, total, bill_id, date_time)
        save_recp_file(customer_name, items_bought, total, bill_id, date_time, receipt_file)

        with open(order_file, 'a') as order:
            order.write(f"Customer name: {customer_name}\n")
            order.write(f"Order Number: {order_number}\n")
            order.write(f"Order Status: Order placed\n")
            for item in items_bought:
                order.write(item + '\n')
            order.write(f"Total: RM{total:.2f}\n\n")

        print(f"Order placed successfully. Your order number is {order_number}.")
    else:
        print("Invalid choice.")

def print_receipt(customer_name, items_bought, total, bill_id, date_time):
    print("\n----- Bakery Receipt -----")
    print(f"Customer: {customer_name}")
    print(f"Bill ID: {bill_id}")
    print(f"Date & Time: {date_time}")
    print("\nItems:")
    for item in items_bought:
        print(f"- {item}")
    print(f"\nTotal: RM{total:.2f}")
    print("--------------------------\n")

def save_recp_file(customer_name, items_bought, total, bill_id, date_time, receipt_file='cus_recp.txt'):
    try:
        with open(receipt_file, 'a') as file:
            file.write(f"\n----- Bakery Receipt -----\n")
            file.write(f"Customer: {customer_name}\n")
            file.write(f"Bill ID: {bill_id}\n")
            file.write(f"Date & Time: {date_time}\n")
            file.write("\nItems:\n")
            for item in items_bought:
                file.write(f"- {item}\n")
            file.write(f"\nTotal: RM{total:.2f}\n")
            file.write("--------------------------\n\n")
        print("Receipt saved successfully.")
    except Exception as e:
        print(f"An error occurred while saving the receipt: {e}")

def update_order_status(order_number, new_status, order_file='order.txt'):
    try:
        with open(order_file, 'r') as file:
            lines = file.readlines()

        updated_lines = []
        order_found = False

        for line in lines:
            if f'Order Number: {order_number}' in line:
                order_found = True
                updated_lines.append(line)
                continue

            if order_found and 'Order Status:' in line:
                updated_lines.append(f"Order Status: {new_status}\n")
                order_found = False  
            else:
                updated_lines.append(line)

        with open(order_file, 'w') as file:
            file.writelines(updated_lines)

    except FileNotFoundError:
        print(f"Error: '{order_file}' file not found.")
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

def main():
    menu = load_csv()
    
    while True:
        print("----------Cashier's Menu----------")
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
            manage_discount()
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

if __name__ == '__main__':
    main()
