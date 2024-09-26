import hashlib
import random

def validate_email():
    while True:
        email = input("Please enter your email address: ").strip()
        if email and email.endswith("@gmail.com"):
            return email
        elif not email:
            print("Email cannot be empty. Please try again.")
        else:
            print("Invalid email. Please use a valid domain. eg: (@gmail.com).")

def update_acc():
    # Validate old username and password first
    old_username = input("Enter your current username: ")
    old_password = input("Enter your current password: ")

    hashed_old_pw = hashlib.md5(old_password.encode()).hexdigest()
    
    cus_found = False
    customers = []
    
    try: 
        with open('customer_data.csv', 'r') as file:
            lines = file.readlines()

            for line in lines[1:]: # ignore the first line (title line)
                name, email, user_name, password, role = line.strip().split(',')
                # If username and password match, update user details
                if user_name == old_username and password == hashed_old_pw:
                    cus_found = True
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

    if cus_found:
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
        with open('order.txt', 'r') as file:
            lines = file.readlines()
    
        customer_cart = []
        cart_found = False # check if username got a cart
        status_check = False # check order status

        for line in lines:
            if line.strip() == username: # if the username is found
                cart_found = True
                continue # this will not add the username in txt file into the list
            
            if cart_found and "Order Status: in-cart" in line:
                status_check = True
                continue

            elif cart_found and status_check:
                if line.strip() == "": # break when meet empty line
                    break
                customer_cart.append(line.strip()) # add the status,items and total
        
        if customer_cart:
            print(f"{username}'s Cart: ")
            print("\n".join(customer_cart))
            print("-" * 55)
        else:
            customer_cart = []

        return customer_cart

    
    def update_cart(username):
        with open('menu.csv','r',newline='') as file:
            lines = file.readlines()[1:]
            items = [line.strip().strip(',') for line in lines]

        menu()
        customer_cart = find_cart(username) # search for existing cart
        total_bill = 0

        if customer_cart:
            old_total = customer_cart.pop() # remove the old total(last line)
            if old_total.startswith("Total: RM"):
                total_bill = float(old_total.replace("Total: RM","").strip())
            else:
                customer_cart.append(old_total)

        if not customer_cart:
            print(f"Your cart is empty.")

        while True:
            order_item = (input("Enter the Product Number to add to cart('q' to quit): "))

            if order_item.lower() == "q":
                 if customer_cart:
                    print("-"*50 + f"\nItems in {username}'s cart:") # display current user cart
                    for item in customer_cart:
                        print(f"{item}")
                    print(f"\nTotal Amount: RM{total_bill:.2f}\n" + "-"*50)
                 print("Exiting...")
                 break
            
            for item in items:
                if item[0] == order_item:
                    price = item[3].replace('RM','').strip() # remove the RM in price
                    try:
                        quantity = int(input("Enter the quantity of item: "))
                        total_bill += float(price) * quantity
                        print(f"Added to your cart: {item[1]} {item[3]} x {quantity}")
                        customer_cart.append(f"{item[0]} {item[1]} {price} x {quantity}")
                    except ValueError:
                        print("Please enter a valid integer.")

            menu()
            print("-"*50 + f"\nItems in {username}'s cart:") # display current user cart
            for item in customer_cart:
                print(f"{item}")
            print(f"\nTotal Amount: RM{total_bill:.2f}\n" + "-"*50)

        clear_cart(username) # clear old cart if cart exist before writing the new cart

        # write all items in customer_cart into txt when user quit
        with open('order.txt','a') as file:
            file.write(f"{username}\n")
            file.write("Order Status: in-cart\n")
            for item in customer_cart:
                file.write(f"{item}\n")
            file.write(f"Total: RM{total_bill:.2f}\n\n")


    def clear_cart(username):
        with open('order.txt', 'r') as file:
            lines = file.readlines()

        # create the list to keep the lines
        new_lines = []
        clear_line = False
        status_check = False # To ensure the cart status is 'in-cart'

        # Search for username's cart and status 'in-cart'
        for line in lines:
            if line.strip() == username:
                next_line = lines[lines.index(line) + 1].strip()
                if "Order Status: in-cart" in next_line:
                    clear_line = True
                    status_check = True
                    continue
            
            # stop clearing when meet empty line
            if clear_line and line.strip() == "":
                clear_line = False
                continue

            if not clear_line:
                new_lines.append(line)

        if status_check:
            # write the file back without the cleared cart
            with open('order.txt', 'w') as file:
                file.writelines(new_lines)


    def check_out(username):
        cus_cart = False
        status_check = False
        with open('order.txt', 'r') as file:
            lines = file.readlines()

        for line in lines:
            if line.strip() == username:
                cus_cart = True
                
            if cus_cart and "Order Status: in-cart" in line:
                status_check = True
                print("-"*50)
                print(f"\n{username}'s Cart: ")
                print(line.strip())
                continue
                
            if status_check:
                print(line.strip())
                if line.startswith("Total: "):
                    print("\n" + "-"*50)
                    break

        if cus_cart and status_check:
            order = input("Would you like to check out?(yes/no): ")
            if order.lower() == "yes":
                with open('order.txt','w') as file:
                    cus_found = False
                    for line in lines:
                        if line.strip() == username:
                            cus_found = True
                        elif cus_found and "Order Status: in-cart" in line:
                            line = "Order Status: order placed\n"
                            cus_found = False
                        file.write(line)
                
                print("**Your order has been placed successfully.**")
            else:
                print("\t**Your items are still in shopping cart.**")

        if not cus_cart:
            print("Your cart is empty.")


    def remove_cart(username):
        customer_cart = find_cart(username)

        if not customer_cart:
            print("Your cart is empty.")
            return

        # Initialize total bill from the existing cart
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

            cus_input = input("Enter the number of item to remove from cart: ")

            if cus_input.lower() == 'q':
                print("Exiting...")
                break
            elif cus_input.lower() == "clear":
                clear_cart(username)
                print("Your cart has been cleared.")
                break
            elif cus_input.isdigit():
                remove_num = int(cus_input)
                item_found = False

                for item in customer_cart:
                    if item.startswith(str(remove_num)):
                        # get price and quantity from item inside cart
                        product_part = item.split()
                        item_part = item.split("RM")[-1] # split item_details into 2 parts and take second part
                        
                        price, quantity = map(str.strip, item_part.split("x")) # split 'x', then map p and q values
                        price = float(price)
                        quantity = int(quantity)

                        product_name = " ".join(product_part[1:-3])

                        remove_qty = int(input("Enter the quantity to remove: "))
                        
                        item_found = True
                        if remove_qty > quantity:
                            print("You cannot remove more than you have.")
                            continue
                        
                        if remove_qty == quantity:
                            customer_cart.remove(item)
                            total_bill -= price * quantity
                            print(f"Removed all {quantity} of {product_name}.")
                        else:
                            new_qty = quantity - remove_qty
                            updated_item = f"{remove_num}  {product_name} RM{price:.2f} x {new_qty}"
                            customer_cart[customer_cart.index(item)] = updated_item
                            total_bill -= price * remove_qty

                            print("-"*50 + f"\nItems in {username}'s cart:") # display current user cart
                            for item in customer_cart:
                                print(f"{item}")
                            print(f"\nTotal Amount: RM{total_bill:.2f}\n" + "-"*50)
                        break  # Exit the loop after modify cart item list

                if not item_found:
                    print("Item not found in your cart.")
            else:
                print("Please enter a valid number, 'clear', or 'q' to quit.")

    # Write the updated cart back to the file
        clear_cart(username)

        with open('order.txt', 'a') as file:
            file.write(f"{username}\n")
            file.write("Order Status: in-cart\n")
            for item in customer_cart:
                file.write(f"{item}\n")
            file.write(f"Total: RM{total_bill:.2f}\n\n")

    while True:
        print("-"*50 + "\n\t" + "Shopping Cart\n"+ "-"*50)
        print("1. View Cart")
        print("2. Remove items")
        print("3. Check Out")
        print("4. Back")
        print("-"*50)
        choice = str(input("Enter your selection: "))
        if choice == "1":
            update_cart(username)
        elif choice == "2":
            remove_cart(username)
        elif choice == "3":
            check_out(username)
        elif choice == "4":
            print("Return to main customer page...")
            break


def order(username):
    cus_cart = False # check for cart existance
    status_check = False # check for 'order placed' status
    with open('order.txt', 'r') as file:
        lines = file.readlines()

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
            for line in lines:
                if line.strip() == username: # find username's cart
                    cus_cart = True

                if cus_cart and "Order Status: order placed" in line:
                    status_check = True
                    print("-"*50)
                    print(f"\n{username}'s Order: ")
                    print(line.strip())
                    continue

                if status_check:
                    print(line.strip())
                    if line.startswith("Total: "): # stop printing when reach last line
                        print("\n" + "-"*50)
                        break

            if cus_cart:
                while True:
                    order = input("Would you like to cancel your order?(yes/no): ")

                    cus_found = False
                    if order.lower() == "yes":
                        with open('order.txt','w') as file:
                            for line in lines:
                                if line.strip() == username:
                                    cus_found = True
                                if cus_found == True and "Order Status: order placed" in line:
                                    line = "Order Status: cancelled\n"
                                file.write(line)
                            print("**Your order has been cancelled successfully.**")
                            break
                    else:
                        print("\t**Your order has been placed.\t**")
                        break

            if not cus_cart:
                print(f"**No order found for {username}, please check in shopping cart 'check out'.**")


def feedback():
    pass


def main_cus_page(username):
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
            update_acc()
        elif choice == 2:
            cart_page(username)
        elif choice == 3:
            order(username)
        elif choice == 4:
            feedback(username)
        elif choice == 5:
            break

if __name__ == "__main__":
    username = "Bowie"  # storing customer username (testing purpose)
    main_cus_page(username)

