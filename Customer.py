#Customer acc management - create(password verify 2), manage, login, update
#Product browsing
#Cart management - add, remove, mod items
#Order Tracking - status of orders
#Product Review - feedback, suggestions
menu_file ='menu.csv'
import csv
import json
import hashlib


# Function to hash passwords
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def update():
    # Load users.json data
    with open('users.json', 'r') as file:
        users = json.load(file)

    cus_email = input("Enter your email: ")
    cus_pwd = input("Enter your password: ")

    # Compare password
    hashed_pwd = hash_password(cus_pwd)

    # email and password matching or not
    if cus_email in users and users[cus_email]['password'] == hashed_pwd:
        new_email = input("Enter new email: ")
        new_pwd = input("Enter new password: ")

        # Hash new password
        new_h_pwd = hash_password(new_pwd)

        # Update cuz email and pw
        users.pop(cus_email)
        users[new_email] = {
            "email": new_email,
            "password": new_h_pwd
        }

        # Write the updated users data back to userjson
        with open('users.json', 'w') as file:
            json.dump(users, file, indent=4)

        print("Your information was updated successfully.")
    else:
        print("No matching account.")

def cart():
    with open(menu_file, 'r') as file:
        csv_reader = csv.reader(file)
        title = next(csv_reader)
        rows = list(csv_reader)

    print("\t")
    print(f"{'ProductName':<30} {'Category':10} {'Price':10} {'Stock':15}")
    print("-" * 60)
        
    # Read and print each row
    for row in rows:
        name, category, price, stock = row
        print(f"{name.strip():<30} {category.strip():10} {price.strip():10} {stock.strip():<10}")
    
    print("-"*60)


def update_cart(user_cart):
    with open(menu_file,'r') as file:
        lines = file.readlines()

        print("Menu: ")
        for i in range(len(user_cart)):
            food_name, food_description, food_price, food_stock = lines[i].strip().split(',')
            print(f"{i + 1}. {food_name} - {food_description} - RM{float(food_price):.2f} - Stock: {food_stock}")

def order():
    while True:
        print("________________")
        print(f"{'Your order.':>5}")
        print("________________")
        print("1. View Order")
        print("2. Update Order")
        print("3. Back")

        n = (input("Please enter your choice (1-3):"))
        if n == "1":
            pass
        elif n == "2":
            update_cart([])
        elif n == "3":
            main()
        else:
            print("Invalid choice, please try again.")

def product_review():
    pass

def main():

    while True:
        print("_"*50)
        print(f"{'Customer Page':>30}")
        print("_"*50)
        print(f"{'***\N{grinning face} Welcome back to Avengers Bakery !\N{grinning face}***':>20}")
        print("1. Shopping Cart")
        print("2. Order")
        print("3. Product Review")
        print("4. Update Account")
        print("5. Exit")

        try:
            option = int(input("Enter your selection (1-5): "))
            if option == 1:
                cart()
            elif option == 2:
                order()
            elif option == 3:
                product_review()
            elif option == 4:
                update()
            elif option == 5:
                print("Thank you for visiting.")
                exit()
                break
            else:
                print("Please enter a valid number between 1 to 5.")
        except ValueError:
            print("Invalid choice, please enter again (1-5): ")

main()
    #Menu save in csv file, and baker customer refer to the csv file.
