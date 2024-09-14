#Customer acc management - create(password verify 2), manage, login, update
#Product browsing
#Cart management - add, remove, mod items
#Order Tracking - status of orders
#Product Review - feedback, suggestions
import csv

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
    

def cart():
    def update_cart():
        with open('menu.csv','r',newline='') as menu:
            reader = csv.DictReader(menu)
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

        while True:
            while True:
                item_num = input("Enter item number to add (press q to quit): ")
                if item_num == "q":
                    break
                else:
                    continue
            quantity = input("Enter quantity: ")
            with open('menu.csv',newline ='') as menu:
                items = csv.reader(menu)
                next(items)

                for row in items:
                    if row[0] == item_num:
                        with open('cart.csv', 'a') as cart:
                            writer = csv.writer(cart)

                            if cart.tell() == 0:
                                writer.writerow(['No.','Name','Category','Price','Quantity'])
                            
                            writer.writerow([row[0],row[1],row[2],row[3], quantity])
                        
                    print(f"{row[1]} x {quantity} added to cart.") #this message should be delete after printing
                    break
            #     user cart save in a straight line, line by line moving right 
            
            # for line in csv:
            #     file.write(line)
            #     file.write('\n')
        
    def remove_cart():
        # with open('cart.csv','w') as cart:
        #      writer = csv.writer(cart)
        pass

    while True:
        print("1. View Cart")
        print("2. Remove items")
        print("3. Check Out")
        print("4. Back")

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


def main_cus_page():
    while True:
        print("-"*50 + "\n\t\t" + f"Welcome, .\n"+ "-"*50)
        print("1. Update Account")
        print("2. Shopping Cart")
        print("3. My Order")
        print("4. Feedback")
        print("5. Exit")
        print("-"*50)

        choice = str(input("Enter your selection(1-4): "))
        if choice == "1":
            update_acc()
        elif choice == "2":
            cart()
        elif choice == "3":
            order()
        elif choice == "4":
            feedback()
        elif choice == "5":
            break
        else:
                print("Invalid selection. Enter number between 1-4.")

main_cus_page()
