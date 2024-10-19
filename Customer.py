import hashlib
import random

# this function will be delete after import Customer into main
def validate_email():
    while True:
        email = input("Please enter your email address: ").strip()
        if email and email.endswith("@gmail.com"):
            return email
        elif not email:
            print("Email cannot be empty. Please try again.")
        else:
            print("Invalid email. Please use a valid domain. eg: (@gmail.com).")


def update_account():
    # Validate old username and password first
    old_username = input("Enter your current username: ")
    old_password = input("Enter your current password: ")

    hashed_old_password = hashlib.md5(old_password.encode()).hexdigest()
    
    customer_found = False
    customers = []
    
    try: 
        with open('user_data.csv', 'r') as file:
            lines = file.readlines()

            for line in lines[1:]: # ignore the first line (title line)
                name, email, user_name, password, role = line.strip().split(',')[:5]

                if user_name == old_username and password == hashed_old_password:
                    customer_found = True
                    print('-'*50 + f"\nUpdate {old_username}'s Account.\n" + '-'*50)
                    user_name = input("Enter new username: ")
                    if not user_name:
                        print("Update failed: new username cannot be empty.")
                        return

                    new_password = input("Enter new password: ")
                    if not new_password:
                        print("Update failed: new password cannot be empty.")
                        return
                    comfirmed_pw = input("Comfirm new password: ")

                    if comfirmed_pw == new_password:
                        password = hashlib.md5(new_password.encode()).hexdigest()
                    else:
                        print("Passwords don't match.")
                        return
                    email = validate_email()

                customers.append([name,email,user_name,password,role])

    except FileNotFoundError:
        print("'user_data.csv' file not found.")
        print("PLEASE CONTACT ADMINISTRATOR IMMEDIATELY")
        return

    if customer_found:
        # Overwrite the file using updated customer list
        with open("user_data.csv", "w", newline='') as file:
            file.write("Name,Email,Username,Password,Role,Staff_ID\n")
            for customer in customers:
                file.write(','.join(customer) + "\n")
        print("Customer details updated successfully.")
    else:
        print("Customer not found.")
    

def cart_page(username):
        while True:
            print("-"*50 + "\n\t\t" + "Shopping Cart\n"+ "-"*50)
            print("1. Add to Cart")
            print("2. Remove items")
            print("3. Check Out")
            print("4. Back")
            print("-"*50)
            choice = str(input("Enter your selection: "))
            if choice == "1":
                update_cart(username)
            elif choice == "2":
                remove_cart_item(username)
            elif choice == "3":
                place_order(username)
            elif choice == "4":
                print("Return to main customer page...")
                break
            else:
                print("Invalid selection, please enter a number between 1-4.")

def display_menu():
    try:
        with open('menu.csv','r',newline='') as menu:
            lines = menu.readlines()[1:] # start with items without title
            items = []
        for line in lines:
            menu_item = line.strip()  # Remove leading whitespace
            split_line = menu_item.split(',')  # Split by ,
            items.append(split_line)  # Add the result to the items list

        print('-'*110 + '\nProductNumber\tProductName\t\t\tCategory\tPrice\t\tStocks\t\tDiscount\n' + '-'*110)

        for item in items:
            product_number, product_name, category, price, stock, discount = item

            print(f"\t{product_number: <7}  {product_name: <30} {category: <14} {price: <17} {stock:<15} {discount}")
        print("-"*110)
        return items
    except FileNotFoundError:
        print("Error: File not found.")
        print("PLEASE CONTACT ADMINISTRATOR IMMEDIATELY")


def find_cart(username):
    try:
        with open('cart.txt', 'r') as file:
            lines = file.readlines()

        customer_cart = []
        cart_found = False  # Check if username has a cart or not

        for line in lines:
            if line.strip() == username:  # If the username is found
                cart_found = True
                continue  # without add the username to the list
            
            if "Order Status: in-cart" in line:
                continue # without adding status

            if cart_found:
                if line.strip() == "":  # Break when reach empty line
                    break
                customer_cart.append(line.strip())  # Add all exist items and total in cart

        if customer_cart:
            print(f"{username}'s Cart: ")
            print("\n".join(customer_cart))
            print("-" * 55)
        else:
            customer_cart = [] # if username not found cart is empty

        return customer_cart
    
    except FileNotFoundError:
        print("Error: File not found.")
        print("PLEASE CONTACT ADMINISTRATOR IMMEDIATELY")
        return


def clear_cart(username):
    try:
        with open('cart.txt', 'r') as file:
            lines = file.readlines()

        other_carts = []  # To store lines that will be written back
        user_cart = False # clean the current username cart

        # Find username cart
        for line in lines:
            if line.strip() == username:
                user_cart = True
                continue

            if user_cart and line.strip() == "": # stop when meet empty line
                user_cart = False
                continue

            if not user_cart:
                other_carts.append(line)
        
        with open('cart.txt', 'w') as file: # write back the rest without the cleared cart
            file.writelines(other_carts)
        return
    except FileNotFoundError:
        print("Error: File not found.")
        print("PLEASE CONTACT ADMINISTRATOR IMMEDIATELY")
        return

def update_cart(username):
    try:
        with open('menu.csv','r',newline='') as file:
            lines = file.readlines()[1:] # start with items without title
            items = [line.strip().split(',') for line in lines]
    except FileNotFoundError:
        print("Error: File not found.")
        print("PLEASE CONTACT ADMINISTRATOR IMMEDIATELY")
        return

    display_menu()
    customer_cart = find_cart(username) # search for existing cart
    total_bill = 0

    if customer_cart:
        old_total = customer_cart.pop() # remove the old total(last line)
        if old_total.startswith("Total: RM"):
            total_bill = float(old_total.replace("Total: RM","").strip())
        else:
            customer_cart.append(old_total) # add back the old total in pure float form

    if not customer_cart:
        print("You cart is empty.")

    while True:
        item_number = (input("Enter the Product Number to add to cart('q' to quit): "))

        if item_number.lower() == "q":
            if customer_cart:
                print("-"*50 + f"\nItems in {username}'s cart:") # display current user cart
                for item in customer_cart:
                    print(f"{item}")
                print(f"\nTotal Amount: RM{total_bill:.2f}\n" + "-"*50)
            print("Exiting...")
            break
        
        if item_number.isdigit():
            for item in items:
                if item[0] == item_number:
                    price = float(item[3].replace('RM','').strip()) # remove the RM in price
                    stock_amount = int(item[4])  # get stock amount from menu
                    try:
                        quantity = int(input("Enter the quantity of item: ").strip())
                        if quantity <= stock_amount:
                            total_bill += float(price) * quantity
                            print(f"Added to your cart: {item[1]} {item[3]} x {quantity}")
                            customer_cart.append(f"{item[0]} {item[1]}, RM{price} x {quantity}")

                        else:
                            print(f"**Not enough stock for {item[1]}.**")
                            break
                    except ValueError:
                        print("Please enter a valid integer.")
                        break

            display_menu()
            print("-"*50 + f"\nItems in {username}'s cart:") # display current user cart
            for item in customer_cart:
                print(f"{item}")
            print(f"\nTotal Amount: RM{total_bill:.2f}\n" + "-"*50)

        else:
            print("Invalid Input.")

    clear_cart(username)# clear old cart if cart exist before writing the new cart

    # write all items in customer_cart into txt when user quit
    try:
        with open('cart.txt','a') as file:
            file.write(f"{username}\n")
            file.write("Order Status: in-cart\n")
            for item in customer_cart:
                file.write(f"{item}\n")
            file.write(f"Total: RM{total_bill:.2f}\n\n")

    except FileNotFoundError:
        print("Error: File not found.")
        print("PLEASE CONTACT ADMINISTRATOR IMMEDIATELY")
        return

def deduct_stock(customer_cart):
        menu = {}
        with open('menu.csv', 'r') as file:
            next(file)  # Skip the header line
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 5:
                    product_number, product_name, category, price, stock_amount = parts
                    menu[product_number] = [product_name.strip(), category.strip(), price.strip(), int(stock_amount)]

        for item in customer_cart:
            parts = item.strip().split(' ')
            if len(parts) >= 2 and 'x' in item:
                product_number = parts[0]
                quantity = int(parts[-1])  # The quantity is at the end
                if product_number in menu:
                    menu[product_number][3] -= quantity  # Deduct stock
                else:
                    print(f"Error: Product number {product_number} not found in the menu.")  # Log an error
                    return

        with open('menu.csv', 'w') as file:
            file.write("ProductNumber,ProductName,Category,Price,StocksAmount\n")
            for product_number, item in menu.items():
                file.write(f"{product_number},{item[0]},{item[1]},{item[2]},{item[3]}\n")

def place_order(username):
    customer_cart = find_cart(username)

    if not customer_cart:
        
        print("Your cart is empty.")
        return

    while True:
        order = input("Would you like to place the order? (yes/no): ").lower()
        if order == "yes":
            with open('order.txt', 'a') as file:
                # generate order number using random module
                order_number = ''.join(random.choices("0123456789", k=3))
                file.write(f"{username}\nOrder Number: {order_number}\nOrder Status: order placed\n") # update order status
                for item in customer_cart:
                    file.write(f"{item}\n")
                file.write("\n")

            deduct_stock(customer_cart)
            clear_cart(username)
            print("**Your order has been placed successfully.**")
            return

        elif order == "no":
            print("**Your items are still in the shopping cart.**")
            return

        else:
            print("Invalid input, please type 'yes' or 'no'.")


def remove_cart_item(username):
    customer_cart = find_cart(username)

    if not customer_cart:
        print("Your cart is empty.")
        return

    # set total bill from the existing cart
    total_bill = 0
    old_total = customer_cart.pop()  # Get and remove the old total
    if old_total.startswith("Total: RM"):
        total_bill = float(old_total.replace("Total: RM", "").strip())
    else:
        customer_cart.append(old_total)  # Put it back if not valid

    while True:
        print("\n#1 Enter number of item to remove.")
        print("#2 Type in 'clear' to clear shopping cart.")
        print("#3 Type 'q' to quit.")
        print("-" * 55)

        customer_input = input("Enter the number of item to remove from cart: ")

        if customer_input.lower() == 'q':
            print("Exiting...")
            break

        elif customer_input.lower() == "clear":
            clear_cart(username)
            print("Your cart has been cleared...")
            break

        elif customer_input.isdigit():
            remove_num = int(customer_input)
            item_found = False

            for item in customer_cart:
                if item.startswith(str(remove_num)):
                    # get price and quantity from item inside cart
                    product_part = item.split() #['4', 'Chocolate', 'Chips', 'Cream', 'Bun', 'RM3.00', 'x', '3']
                    item_part = item.split("RM")[-1] # split item_details into 2 parts and take second part
                    # 1: ['4 Chocolate Chips Cream Bun ', '3.00 x 3'], 2: '3.00 x 3'
                    
                    item_part_split = item_part.split("x")
                    price = item_part_split[0].strip() # extract price from item part and remove spaces
                    quantity = item_part_split[1].strip() # extract quantity and remove spaces
                    # price = '3.00', quantity = '3'
                    price = float(price)
                    quantity = int(quantity)

                    product_name = " ".join(product_part[1:-3]) # Ignore number and price x quantity

                    remove_quantity = int(input("Enter the quantity to remove: "))
                    
                    item_found = True
                    if remove_quantity > quantity:
                        print("You cannot remove more than you have.")
                        continue
                    
                    if remove_quantity == quantity:
                        customer_cart.remove(item)
                        total_bill -= price * quantity
                        print(f"Removed all {quantity} of {product_name}.")
                    else:
                        new_quantity = quantity - remove_quantity
                        updated_item = f"{remove_num}  {product_name} RM{price:.2f} x {new_quantity}"
                        customer_cart[customer_cart.index(item)] = updated_item
                        total_bill -= price * remove_quantity

                        print("-"*50 + f"\nItems in {username}'s cart:") # display current user cart
                        for item in customer_cart:
                            print(f"{item}")
                        print(f"\nTotal Amount: RM{total_bill:.2f}\n" + "-"*50)

                    # Write the updated cart back to the file
                    clear_cart(username)

                    with open('cart.txt', 'a') as file:
                        file.write(f"{username}\n")
                        file.write(f"Order Status: in-cart\n")
                        for item in customer_cart:
                            file.write(f"{item}\n")
                        file.write(f"Total: RM{total_bill:.2f}\n\n")
                    break  # Exit the loop after modify cart item list

            if not item_found:
                print("Item not found in your cart.")
        else:
            print("Please enter a valid number, 'clear', or 'q' to quit.")


def order(username):
    order_found = False

    while True:
        print("\n1. Orders in Progress.")
        print("2. Completed Orders.")
        print("3. Back")
        print("-" * 55)

        try:
            order_input = int(input("Enter your selection(1-3):"))
        except ValueError:
            print("Invalid input. Please enter an integer number between 1-3.")
            continue

        if order_input == 1:
            with open('order.txt', 'r') as file:
                lines = file.readlines()

            for line in lines:
                if line.strip() == username:
                    order_found = True

                if order_found:
                    if line.strip() == "":
                        order_found = False
                        print("-" * 50)
                        continue
                    print(line.strip())
            print("-" * 50)
            order_found = True

            if not order_found:
                print(f"You have no order in progress.")

        if order_input == 2:
            with open('completed_order.txt', 'r') as file:
                lines = file.readlines()

            for line in lines:
                if line.strip() == username:
                    order_found = True

                if order_found:
                    if line.strip() == "":
                        order_found = False
                        print("-" * 50)
                        continue
                    print(line.strip())
            print("-" * 50)
            order_found = True

            if not order_found:
                print(f"You have no completed orders.")

        if order_input == 3:
            print("Exiting My Order...")
            return

        
def feedback(username):
    completed_orders = []

    # read completed.order.txt to find username's order
    with open('completed_order.txt','r') as file:
        lines = file.readlines()

    order_found = False
    username_orders = []

    for line in lines:
        if line.strip() == username:
            order_found = True
            username_orders.append(line.strip())
        elif order_found:
            username_orders.append(line.strip())
            if line.startswith("Total: "):
                completed_orders.append(username_orders)
                username_orders = []
                order_found = False
        
    if not completed_orders:
        print("**You have no completed order.**")
        return
        
    print("-"*50 + "\n" + f"{username}'s Completed Orders: ")
    for order in completed_orders:
        print("\n".join(order))
        print("-"*50)

    order_number = input("\nEnter the order number you want to leave feedback: ")

    # check if user give feedback for the currrent order
    feedback_given = False
    with open('feedback.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if username in line and f"Order Number: {order_number}" in line:
                feedback_given = True
                break
    
    if feedback_given:
        print("Feedback already provided for this order.")
        return
    
    # Rating from 1-5
    while True:
        rating = input("Please rate your order (1-5): ")
        if rating.isdigit() and 1 <= float(rating) <= 5:
            break
        else:
            print("Invalid rating. Please enter a number between 1 and 5.")
        
    comment = input("Please provide your feedback: ")

    with open('feedback.txt', 'a') as file:
        file.write(f"{username} - Order Number: {order_number}\nRating: {rating}\nFeedback: {comment}\n\n")

    print("Thank you for your feedback!")

def main_customer_page(username):
    while True:
        print("-"*50 + "\n  " + f"-----Welcome to Avenger Bakery! {username.upper()}.-----\n"+ "-"*50)
        print("1. Update Account")
        print("2. Shopping Cart")
        print("3. My Order")
        print("4. Feedback")
        print("5. Exit")
        print("-"*50)

        while True:
            try:
                choice = int(input("Enter your selection(1-5): "))
                if choice in [1,2,3,4,5]:
                    break
                else:
                    print("Please enter a valid option between 1-5")
            except:
                print("Invalid selection. Please enter a number between 1-5.")

        if choice == 1:
            update_account()
        elif choice == 2:
            cart_page(username)
        elif choice == 3:
            order(username)
        elif choice == 4:
            feedback(username)
        elif choice == 5:
            print("Exiting customer page...")
            return

if __name__ == "__main__":
    main_customer_page(username="USER_UNDEFINED")

