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

def update_acc():
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
    def update_cart():
        total_bill = 0
        customer_cart = []

        with open('menu.csv','r',newline='') as menu:
            # saving csvdictreader in list so it can be iterate over multiple times
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
            #     user cart save in a straight line, line by line moving right 

        user_cart = False
        with open('order.csv', 'r') as file:
            lines = file.readlines()
            current_username = None
            for line in lines:
                if line.strip() == username:
                    user_cart = True
                    print(f"\n{username}'s Cart: ")
                elif current_username and line.startswith("Order Status: in-cart"):
                    print(line.strip())  # status
                elif current_username and line.startswith("-"):
                    print(line.strip())  # items
                elif current_username and line.startswith("Total:"):
                    print(line.strip())  # total
                    break
                
        if not user_cart:
            print("Your cart is empty.") 

        while True:
            order_input = input("Enter item number to add to cart (q to quit): ").strip()

            if order_input.lower() == "q":
                break

            try:
                product_num = int(order_input)
                product_found = False
                
                for item in reader:
                    if int(item.get('ProductNumber')) == product_num:
                        product_name = item.get('ProductName')
                        price = item.get('price').replace('RM','').strip()

                        # Validate the quantity input is integer data type
                        try:
                            quantity = int(input("Enter quantity: "))
                        except ValueError:
                            print("Please enter a valid integer quantity.")
                            continue
                        
                        # display particualr things added in cart
                        total_bill += float(price)*quantity
                        customer_cart.append(f"{product_name}, RM{price} x {quantity}")
                        print(f"Added to cart: {product_name}, RM{price} x {quantity}")
                        
                        # display the things in cart and total
                        print(f"\nItems in {username}'s cart:")
                        for item in customer_cart:
                            print(f"- {item}")
                        print(f"\nTotal Amount: RM{total_bill:.2f}")
                        
                        product_found = True
                        break

                if not product_found:
                    print(f"Item with number {product_num} not found.")

            except ValueError:
                print("Invlaid input. Please enter a valid item number or 'q' to quit.")
            
        if not customer_cart:
            print("Your cart is empty.")
            return

        with open('order.csv', 'a', newline='') as file:
            file.write(f"{username}\n")
            for item in customer_cart:
                file.write(f"- {item}\n")
            file.write(f"Total: RM{total_bill:.2f}\n")
            file.write("\n")

    def remove_cart():
        # with open('cart.csv','w') as cart:
        #      writer = csv.writer(cart)
        pass

    while True:
        print("-"*50 + "\n\t" + "Shopping Cart\n"+ "-"*50)
        print("1. View Cart")
        print("2. Remove items")
        print("3. Check Out")
        print("4. Back")
        print("-"*50)
        choice = str(input("Enter your selection: "))
        if choice == "1":
            update_cart()
        elif choice == "2":
            remove_cart()
        elif choice == "3":
            order()
        elif choice == "4":
            main_cus_page()


def order():
    pass

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
    username = "customer_name"  # storing customer username
    main_cus_page(username)
