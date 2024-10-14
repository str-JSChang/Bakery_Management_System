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
        with open('customer_data.csv', 'r') as file:
            lines = file.readlines()

            for line in lines[1:]: # ignore the first line (title line)
                name, email, user_name, password, role = line.strip().split(',')
                # If username and password match, update user details
                if user_name == old_username and password == hashed_old_password:
                    customer_found = True
                    print(f"Update {old_username}'s Account.")
                    user_name = input("Enter new username: ")

                    new_pw = input("Enter new password: ")
                    comfirmed_pw = input("Comfirm new password: ")

                    if comfirmed_pw == new_pw:
                        password = hashlib.md5(new_pw.encode()).hexdigest()
                    else:
                        print("Passwords don't match.")
                        return
                    email = validate_email()

                customers.append([name,email,user_name,password,role])

    except FileNotFoundError:
        print("'customer_data.csv' file not found.")
        return

    if customer_found:
        # Overwrite the file using updated cus list
        with open("customer_data.csv", "w", newline='') as file:
            file.write("Name,Email,Username,Password,Role\n")
            for customer in customers:
                file.write(','.join(customer) + "\n")
        print("Customer details updated successfully.")
    else:
        print("Customer not found.")
    

def cart_page(username):
    def menu():
        with open('menu.csv','r',newline='') as menu:
            lines = menu.readlines()[1:] # start with items without title
            items = [line.strip().split(',') for line in lines]

        print('-'*90 + '\nProductNumber\tProductName\t\t\tCategory\tPrice\t\tStocks\n' + '-'*90)
        for item in items:
            product_number, product_name, category, price, stock = item

            print(f"\t{product_number: <8.5}  {product_name: <33} {category: <14} {price: <17} {stock}")
        print("-"*90)
    

    def find_cart(username):
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
                customer_cart.append(line.strip())  # Add all exist items and total

        if customer_cart:
            print(f"{username}'s Cart: ")
            print("\n".join(customer_cart))
            print("-" * 55)
        else:
            customer_cart = [] # if username not found cart is empty

        return customer_cart

    
    def update_cart(username):
        with open('menu.csv','r',newline='') as file:
            lines = file.readlines()[1:]
            items = [line.strip().split(',') for line in lines]

        menu()
        customer_cart = find_cart(username) # search for existing cart
        total_bill = 0

        if customer_cart:
            old_total = customer_cart.pop() # remove the old total(last line)
            if old_total.startswith("Total: RM"):
                total_bill = float(old_total.replace("Total: RM","").strip())
            else:
                customer_cart.append(old_total) # add back the old total in pure float form

        if not customer_cart:
            print(f"Your cart is empty.")

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
                                item[4] = str(stock_amount - quantity) # update stock amount
                            else:
                                print(f"**Not enough stock for {item[1]}.**")
                        except ValueError:
                            print("Please enter a valid integer.")

                with open('menu.csv', 'w') as file:
                    file.write("ProductNumber,ProductNumber,ProductName,Category,Price,StocksAmount\n")
                    for item in items:
                        file.write(','.join(item) + '\n')

                menu()
                print("-"*50 + f"\nItems in {username}'s cart:") # display current user cart
                for item in customer_cart:
                    print(f"{item}")
                print(f"\nTotal Amount: RM{total_bill:.2f}\n" + "-"*50)

            else:
                print("Invalid Input.")

        clear_cart(username)# clear old cart if cart exist before writing the new cart

        # write all items in customer_cart into txt when user quit
        with open('cart.txt','a') as file:
            file.write(f"{username}\n")
            file.write("Order Status: in-cart\n")
            for item in customer_cart:
                file.write(f"{item}\n")
            file.write(f"Total: RM{total_bill:.2f}\n\n")
        return


    def clear_cart(username):
        with open('cart.txt', 'r') as file:
            lines = file.readlines()

        new_lines = []  # To store lines that will be written back
        clear_line = False # clean the current username cart

        # Find username cart
        for line in lines:
            if line.strip() == username:
                clear_line = True
                continue

            if clear_line and line.strip() == "": # stop when meet empty line
                clear_line = False
                continue

            if not clear_line:
                new_lines.append(line)
        
        with open('cart.txt', 'w') as file: # write back the rest without the cleared cart
            file.writelines(new_lines)
        return

            
    def place_order(username):
        customer_cart = find_cart(username)
       
        if customer_cart:
            while True:
                order = input("Would you like to place order?(yes/no): ")
                if order.lower() == "yes":
                    with open('order.txt','a') as file:
                        file.write(f"{username}\n")
                        # use random to generate order number
                        file.write(f"Order Number: {random.randint(100,999)}\n")
                        # write cart into order + change status
                        for item in customer_cart:
                            file.write("Order Status: order placed\n")
                            file.write(f"{item}\n")
                        file.write("\n")
                    
                    clear_cart(username)

                    print("**Your order has been placed successfully.**")
                    return

                elif order.lower == "no":
                    print("\t**Your items are still in shopping cart.**")
                    return

                else:
                    print("Invalid input, please type 'yes' or 'no'. ")

        else:
            print("Your cart is empty.")
        return


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


    while True:
        print("-"*50 + "\n\t" + "Shopping Cart\n"+ "-"*50)
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


def order(username):
    order_found = False
    order_number = None

    while True:
        print("\n1. Orders in Progress.")
        print("2. Completed Orders.")
        print("3. Back")
        print("-" * 55)

        try:
            order_input = int(input("Enter your selection(1-3):"))
        except ValueError:
            print("Invalid input. Please enter integer number between 1-3.")
            continue

        if order_input == 1:
            with open('order.txt', 'r') as file:
                lines = file.readlines()

            order_found = False
            for line in lines:
                if line.strip() == username:
                    order_found = True
                
                if order_found:
                    if line.strip() == "":
                        order_found = False
                        print("-"*50)
                        continue
                    print(line.strip())

                    if "Order Number:" in line:
                        order_number = line.strip().split(": ")[1]
            print("-"*50)
            order_found = True

            if order_found:
                    cancel_order_input = input("Would you like to cancel your order?(yes/no): ")

                    if cancel_order_input.lower() == "yes":
                        input_num = input("Enter order number you want to cancel: ")

                        if input_num == order_number:
                            with open('order.txt','w') as file:
                                ignore_order = False
                                for line in lines:
                                    if line.strip() == username:
                                        file.write(line)

                                        if f"Order Number: {input_num}" in line:
                                            ignore_order = True
                                            continue

                                        if ignore_order == True and "Order Status: order placed" in line:
                                            file.write("Order Status: cancelled\n")
                                            ignore_order = False
                                        else:
                                            file.write(line)

                                print(f"**Your order {input_num} has been cancelled successfully.**")
                        else:
                            print("Order not found. Please check order number.")
                    elif cancel_order_input.lower()=="no":
                        print("\t**Baker is preparing your order.**")
                    else:
                        print("Invalid input, please type 'yes' or 'no'.")

        if order_input == 2:
            with open('completed_order.txt', 'r') as file:
                lines = file.readlines()

            for line in lines:
                if line.strip() == username:
                    order_found = True
                
                if order_found:
                    if line.strip() == "":
                        order_found = False
                        print("-"*50)
                        continue
                    print(line.strip())
            print("-"*50)
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
        print("-"*50 + "\n\t" + f"Welcome, {username.upper()}.\n"+ "-"*50)
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
                print("Invalid input. Please enter integer number between 1-5.")

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
            break

if __name__ == "__main__":
    username = "Chong"  # storing customer username (testing purpose)
    main_customer_page(username)
