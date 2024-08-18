#Customer acc management - create(password verify 2), manage, login, update
#Product browsing
#Cart management - add, remove, mod items
#Order Tracking - status of orders
#Product Review - feedback, suggestions
import re
import os

def login(users):
    cus_name = input("Enter user name: ")
    cus_password = input("Enter password: ")
    user = next((u for u in users if u[0] == cus_name and u[2] == cus_password), None)
    if user:
      print(f"***Welcome back, {user[0]}.\N{grinning face}***")
    else:
        print("User not found. Please sign up.")
    return user

def signup(users):
    user_data = []
    cus_name = str(input("Enter User Name: "))
    email = str(input("Enter User Email: "))
    while True:
        cus_password = str(input("Enter Password: "))
        if(len(cus_password) >= 8 and
            re.search("[a-z]", cus_password) and
            re.search("[A-Z]", cus_password) and
            re.search("[0-9]", cus_password)):
            break
        else:
            print("Your password should include: \n8 characters \n1 uppercase letter \n1 lowercase letter.")
    address = str(input("Enter User Address: "))

    user_data.append(cus_name)
    user_data.append(email)
    user_data.append(cus_password)
    user_data.append(address)

    users.append(user_data)
    with open('users.txt', 'a') as file:
        file.write(','.join(user_data) + '\n')

    print("User added: ", user_data)
    print("Welcome, ", cus_name)
    return user_data

# load user data from file
def load_users():
    users = []
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            for line in file:
                user_data = line.strip().split(',')
                users.append(user_data)
    return users

def cart(user):
    if user is None:
        print("Please log in first.")

    if os.path.exists('menu.txt'):
        with open('menu.txt', 'r') as file:
            lines = file.readlines()
            if lines:
                print("\nMenu:")
                print(f"{'No.':<5}{'Name':<20}{'Description':<30}{'Price':<10}{'Stock':<5}")
                print("="*70)
                for index, line in enumerate(lines, start=1):
                    try:
                        food_name, food_description, food_price, food_stock = line.strip().split(',')
                        print(f"{index:<5}{food_name:<20}{food_description:<30}{(food_price):<10}{food_stock:<5}")
                    except ValueError:
                        print(f"Skipping invalid line: {line.strip()}")
            else:
                print("Menu is empty.")
    cart = []
    while True:
        food = input("Enter food number to add to cart ('q'to quit): ")
        if food.lower() == 'q':
            main()
        cart.append(food)


def order(user):
    while True:
        print("________________")
        print(f"{user[0]}'s, Order.")
        print("________________")
        print("1. View Order")
        print("2. Update Order")
        print("3. Back")

        n = (input("Please enter your choice (1-3):"))
        if n == "1":
            pass
        elif n == "2":
            cart(user)
        elif n == "3":
            break


def product_review():
    pass

def main():
    users = load_users()
    user = None

    while True:
        print("________________________________")
        print(f"{'':<10}{'Customer Page'}")
        print("________________________________")
        if user:
            print(f"***Welcome back, {user[0]}.\N{grinning face}***")
        print("1. Log In")
        print("2. Sign Up")
        print("3. Shopping Cart")
        print("4. Order")
        print("5. Exit")

        n = input("Enter your choice (1-5): ")
        if n == "1":
            user = login(users)
        elif n == "2":
            user = signup(users)
        elif n == "3":
            if user:
                cart(user)
            else:
                print("Please login to view more.")
        elif n == "4":
            if user:
                order(user)
            else:
                print("Please login to view more.")
        elif n == "5":
            print("See you again.")
            break
        else:
            print("Invalid choice, please enter again (1-5): ")


if __name__ == "__main__":
    main()
    #Menu save in txt file, and baker customer refer to the txt file.

