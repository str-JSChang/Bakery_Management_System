import csv
import hashlib

def validate_email():
    while True:
        email = input("Please enter your email address: ").strip()
        if email and email.endswith("@gmail.com"):
            return email
        elif not email:
            print("Email cannot be empty. Please try again.")
        else:
            print("Invalid email. Please use a valid domain. eg: (@gmail.com).")

def update_acc(username):
    # Validate old username and password first
    old_username = input("Enter your current username: ")
    old_password = input("Enter your current password: ")

    hashed_old_pw = hashlib.md5(old_password.encode()).hexdigest()
    
    cus_found = False
    customers = []
    
    try: 
        with open('customer_data.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # If username and password match, update user details
                if row["Username"] == old_username and row["Password"] == hashed_old_pw:
                    cus_found = True
                    print(f"Update {old_username}'s account.")
                    row['Username'] = input("Enter new username: ")
                    
                    new_pw = input("Enter new password: ")
                    confirmed_new_pw = input("Confirm new password: ")
                    
                    if confirmed_new_pw == new_pw:
                        row['Password'] = hashlib.md5(new_pw.encode()).hexdigest()
                    else:
                        print("Passwords don't match. Update failed.")
                        return
                    
                    row["Email"] = validate_email()
                
                # Always append row (modified or unmodified) to customers list
                customers.append(row)

    except FileNotFoundError:
        print("'customer_data.csv' file not found.")
        return

    if cus_found:
        # Overwrite the file using updated cus list
        with open("customer_data.csv", "w", newline='') as file:
            fieldnames = ['Name', 'Email', 'Username', 'Password', 'Role']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(customers)
        
        print("Customer details updated successfully.")
    else:
        print("Customer not found.")
    

def cart(username):
    # find customer cart
    def cart_exist(cus_cart):
        cus_cart = False
        with open('order.csv','r') as file:
            lines = file.readlines()

        current_username = None
        for line in lines:
            if line.strip() == username:
                current_username = username
                cus_cart = True
            elif current_username and "Order Status: in-cart" in line:
                print("-"*50 + f"\n{username}'s Cart: ")
                print(line.strip())  # status
            elif current_username and line[0].isdigit():  # For lines starting with product number
                print(line.strip())  # items
            elif current_username and line.startswith("Total:"):
                print(line.strip())  # total
                print("-"*50)
                return True
        
        if cus_cart == False:
            print("Your cart is empty.")
            return False

    def update_cart(username):
        total_bill = 0
        old_total = 0
        customer_cart = []

        #Read and display the menu
        with open('menu.csv', 'r', newline='') as menu:
            reader = list(csv.DictReader(menu))
            print('-'*90 + '\nProductNumber\tProductName\t\t\tCategory\tPrice\t\tStocks\n' + '-'*90)

            for item in reader:
                product_number = item.get('ProductNumber')
                product_name = item.get('ProductName')
                category = item.get('category')
                price = item.get('price')
                stock = item.get('stocksAmount')

                print(" "*5 + product_number + " " * (10 - len(product_number)) +
                    product_name + " " * (34 - len(product_name)) +
                    category + " " * (14 - len(category)) +
                    price + " " * (18 - len(price)) +
                    stock
                    )
            print("-"*90)

        # Display user cart if it exists
        cart_exist(username)
        while True:
            order_input = input("Enter item number to add to cart (q to quit): ").strip()
            if order_input.lower() == "q":
                break

            try:
                order_input = int(order_input)
                # product = next((item for item in reader if int(item['ProductNumber']) == order_input), None)
                product_found = False
                
                with open('menu.csv', 'r', newline='') as menu:
                    reader = list(csv.DictReader(menu))
                for item in reader:
                    if int(item.get('ProductNumber')) == order_input:
                        product_number = item.get('ProductNumber')
                        product_name = item.get('ProductName')
                        price = item.get('price').replace('RM', '').strip()

                        quantity = int(input("Enter quantity: "))

                        total_bill += float(price) * quantity
                        # Add product to the list (customer cart)
                        customer_cart.append(f"{product_number} {product_name}, RM{price} x {quantity}")
                        print(f"Added to cart: {product_number} {product_name}, RM{price} x {quantity}")

                        print(f"\nItems in {username}'s cart:")
                        for item in customer_cart:
                            print(f"{item}")
                        print(f"\nTotal Amount: RM{total_bill + old_total:.2f}")

                        product_found = True
                        break

                if not product_found:
                    print(f"Item with number {order_input} not found.")
            except ValueError:
                print("Invalid input. Please enter a valid item number or 'q' to quit.")

        # Write updated cart to order csv
        with open('order.csv', 'a', newline='') as file:
            file.write(f"{username}\n")
            file.write("Order Status: in-cart\n")
            for item in customer_cart:
                file.write(f"{item}\n")
            file.write(f"Total: RM{total_bill + old_total:.2f}\n\n")


    def remove_cart(username):
        if not cart_exist(username):
            return
        
        while True:
            remove_item = input("Enter the number of item you want to remove('q' to quit): ")
            if remove_item.lower() == 'q':
                break
            
            try:
                remove_item = int(remove_item)
                item_found = False
                with open('order.csv', 'w') as file:
                    lines = file.readlines()
                    for line in lines:
                        if remove_item != line[0].isdigit():
                            file.write(line)
                            item_found = True
                        else:
                            item_found = True
                            print(f"{line.strip()} has been remove successfully.")
                if not item_found:
                    print(f"Item with number {remove_item} not found.")
            except ValueError:
                print("Invalid input. Please enter a valid item number or 'q' to quit.")

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
            order(username)
        elif choice == "4":
            main_cus_page(username)


def order(username):
    cus_cart = False
    with open('order.csv', 'r') as file:
        lines = file.readlines()

    current_username = None
    for line in lines:
        if line.strip() == username:
            cus_cart = True
            ordered = False
            current_username = username

        elif current_username and ("Order Status: in-cart" in line or "Order Status: order placed" in line):
            if "in-cart" in line:
                print("-"*50 + f"\n{username}'s Cart: ")
            else:
                print("-"*50 + f"\n{username}'s Order: ")
                ordered = True
            print(line.strip())  # status
        elif current_username and line[0].isdigit():  # For lines starting with product number
            print(line.strip())  # items
        elif current_username and line.startswith("Total:"):
            print(line.strip())  # total
            print("-"*50)
            break
 
    if cus_cart and ordered == False:
        order = input("Would you like to place your order?(yes/no): ")
        if order.lower() == "yes":
            with open('order.csv','w') as file:
                cus_found = False
                for line in lines:
                    if line.strip() == username:
                        cus_found = True
                    elif cus_found and "Order Status: in-cart" in line:
                        line = "Order Status: order placed\n"
                        cus_found = False
                    file.write(line)
            
            print("\t**Your order has been placed successfully.**")
        else:
            print("\t**Your items are still in shopping cart.**")
    elif cus_cart and ordered == True:
        print("**\tYour order has been placed.**")

    if not cus_cart:
        print(f"\tNo cart or order found for {username}")


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
                choice = int(input("Enter your selection(1-4): "))
                if choice in [1,2,3,4,5]:
                    break
                else:
                    print("Please enter a valid option between 1-5")
            except:
                print("Invalid input. Please enter integer number between 1-5.")

        if choice == 1:
            update_acc(username)
        elif choice == 2:
            cart(username)
        elif choice == 3:
            order(username)
        elif choice == 4:
            feedback(username)
        elif choice == 5:
            break

if __name__ == "__main__":
    username = "customer_name"  # storing customer username (testing purpose)
    main_cus_page(username)
