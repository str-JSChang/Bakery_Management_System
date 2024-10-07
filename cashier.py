import random
from datetime import datetime

def load_csv():
    csv_file = 'menu.csv'   
    data = {'items': []}
    
    try:
        with open(csv_file, 'r') as menu_file:
            lines = menu_file.readlines()
            headers = lines[0].strip().split(',')  
            
            for line in lines[1:]:  
                values = line.strip().split(',')
                item = dict(zip(headers, values))  
                data['items'].append(item)
        return data
    except FileNotFoundError:
        print(f"Error: '{csv_file}' file not found.")
        return data

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
        
        print(
            f"{product_number: <15}"
            f"{product_name: <35}"
            f"{category: <15}"
            f"{price: <10}"
            f"{stock: <10}"
        )
    
    print('-' * 90)

def manage_discount(menu):
    prod_num = input("Enter Product Number to apply discount: ")
    discount = float(input("Enter discount percentage (e.g., 10 for 10%): "))
    for item in menu['items']:
        if item['ProductNumber'] == prod_num:
            original_price = float(item['price'].replace('RM', ''))  
            discounted_price = original_price - original_price * (discount / 100)
            item['price'] = f"RM{discounted_price:.2f}"
            print(f"Discount applied: {item['ProductName']} new price is {item['price']} (was RM{original_price:.2f})")
            break
    else:
        print("Product not found!")

def generate_receipt(order_file='order.txt', receipt_file='cus_recp.txt'):
    try:
        with open(order_file, 'r') as file:
            lines = file.readlines()

        current_order = {}
        orders = []
        
        for line in lines:
            line = line.strip()
            if not line:  
                if current_order:
                    orders.append(current_order)
                    current_order = {}
                continue

            if 'Order Number:' in line:
                current_order['OrderNumber'] = line.split(': ')[1]
            elif 'Order Status:' in line:
                current_order['Status'] = line.split(': ')[1]
            elif any(char.isdigit() for char in line) and 'Total' not in line:
                parts = line.split(' x ')
                if len(parts) == 2:  
                    quantity = int(parts[1].strip())  

                    product_details = parts[0].rsplit(',', 1)
                    
                    if len(product_details) == 2:  
                        product_name = product_details[0].split(' ', 1)[1].strip()  
                        price = float(product_details[1].replace('RM', '').strip())  

                        if 'Items' not in current_order:
                            current_order['Items'] = []
                        current_order['Items'].append({
                            'ProductName': product_name,
                            'Price': price,
                            'Quantity': quantity
                        })
                    else:
                        print(f"Warning: Invalid product format in line: {line}")
                else:
                    print(f"Warning: Invalid format in line: {line}")
            elif 'Total:' in line:
                current_order['Total'] = float(line.split('RM')[1].strip())
            else:
                if 'CustomerName' not in current_order:
                    current_order['CustomerName'] = line

        if current_order:
            orders.append(current_order)

        for order in orders:
            if order['Status'] == 'order placed':
                customer_name = order['CustomerName']
                total = order['Total']
                items_bought = []
                
                for item in order['Items']:
                    quantity = item['Quantity']
                    product_name = item['ProductName']
                    price = item['Price']
                    
                    for menu_item in menu['items']:
                        if menu_item['ProductName'] == product_name:
                            if int(menu_item['stocksAmount']) >= quantity:
                                menu_item['stocksAmount'] = str(int(menu_item['stocksAmount']) - quantity)
                                items_bought.append(f"{quantity} * {product_name} - RM{price * quantity:.2f}")
                            else:
                                print(f"Not enough stock for {product_name}.")
                            break

                bill_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))

                now = datetime.now()
                date_time = now.strftime("%Y-%m-%d %H:%M:%S")

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

                write_receipt(customer_name, items_bought, total, bill_id, date_time)

                update_order_status(customer_name, order['OrderNumber'], 'Completed', order_file)
                break
        else:
            print("No pending orders found.")
    except FileNotFoundError:
        print(f"Error: '{order_file}' file not found.")

def update_order_status(order_file='order.txt', order_number='', new_status=''):
    """
    Updates the status of a specific order identified by order number in the order file.
    """
    try:
        with open(order_file, 'r') as file:
            lines = file.readlines()

        updated_lines = []
        found_order = False
        order_started = False

        for line in lines:
            if f"Order Number: {order_number}" in line:
                found_order = True
                order_started = True  
                updated_lines.append(line)  
            elif found_order and 'Order Status:' in line:
                updated_lines.append(f"Order Status: {new_status}\n")
                found_order = False  
            else:
                updated_lines.append(line)

        if order_started and not found_order:
            with open(order_file, 'w') as file:
                file.writelines(updated_lines)
            print(f"Order {order_number}'s status has been updated to '{new_status}'.")
        else:
            print(f"Order {order_number} not found.")
    
    except FileNotFoundError:
        print(f"Error: '{order_file}' file not found.")

def print_pending_orders(order_file='order.txt'):
    """
    Prints orders that are not marked as 'Completed'.
    """
    try:
        with open(order_file, 'r') as file:
            lines = file.readlines()

        current_order = {}
        orders = []
        
        for line in lines:
            line = line.strip()
            if not line:  
                if current_order:
                    orders.append(current_order)
                    current_order = {}
                continue

            if 'Order Number:' in line:
                current_order['OrderNumber'] = line.split(': ')[1]
            elif 'Order Status:' in line:
                current_order['Status'] = line.split(': ')[1]
            elif any(char.isdigit() for char in line) and 'Total' not in line:
                parts = line.split(' x ')
                if len(parts) == 2:
                    product_details = parts[0].rsplit(',', 1)
                    if len(product_details) == 2:
                        product_name = product_details[0].split(' ', 1)[1].strip()
                        quantity = int(parts[1].strip())
                        if 'Items' not in current_order:
                            current_order['Items'] = []
                        current_order['Items'].append({
                            'ProductName': product_name,
                            'Quantity': quantity
                        })
            elif 'Total:' in line:
                current_order['Total'] = float(line.split('RM')[1].strip())
            else:
                if 'CustomerName' not in current_order:
                    current_order['CustomerName'] = line

        if current_order:
            orders.append(current_order)

        print("\n--- PENDING ORDERS ---")
        for order in orders:
            if order['Status'] != 'Completed':
                print(f"Order Number: {order['OrderNumber']}, Status: {order['Status']}")
                print(f"Customer Name: {order['CustomerName']}")
                print("Items:")
                for item in order['Items']:
                    print(f"  {item['Quantity']} x {item['ProductName']}")
                print(f"Total: RM{order['Total']:.2f}")
                print("-" * 30)
        print("-" * 30)

    except FileNotFoundError:
        print(f"Error: '{order_file}' file not found.")

def write_receipt(customer_name, items_bought, total, bill_id, date_time, receipt_file='cus_recp.txt'):
    with open(receipt_file, 'a') as file:
        file.write("\n--- RECEIPT ---\n")
        file.write(f"DATA INTO BAKERY SDN.BHD\n")
        file.write(f"WELCOME {customer_name}\n")
        file.write(f"Bill ID: {bill_id}\n")
        file.write(f"Date: {date_time}\n")
        file.write("-" * 40 + "\n")
        file.write(f"Customer Name: {customer_name}\n")
        file.write("Order Summary:\n")
        for order in items_bought:
            file.write(order + "\n")
        file.write(f"Total: RM{total:.2f}\n")
        file.write("-" * 40 + "\n")
        file.write(f"--- THANK YOU {customer_name}, SEE YOU NEXT TIME! ---\n")

def main():
    menu = load_csv()
    
    while True:
        print("\n--- Bakery Management System ---")
        print("1. Display Menu")
        print("2. Manage Discounts")
        print("3. Generate Receipt")
        print("4. Print Pending Orders")
        print("5. Update Order Status")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            display_menu(menu)
        elif choice == '2':
            manage_discount(menu)
        elif choice == '3':
            generate_receipt()  
        elif choice == '4':
            print_pending_orders()  
        elif choice == '5':
            order_number = input("Enter the Order Number to update: ")
            new_status = input("Enter the new status (e.g., Completed): ")
            update_order_status(order_number=order_number, new_status=new_status)
        elif choice == '6':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
