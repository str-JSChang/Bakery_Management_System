#Customer acc management - create(password verify 2), manage, login, update
#Product browsing
#Cart management - add, remove, mod items
#Order Tracking - status of orders
#Product Review - feedback, suggestions
def cart():
    with open('menu.txt','r') as file:
        lines = file.readlines()
        for line in lines:
            food_name, food_description, food_price = line.strip().split(',')
            print(f"Breads: {food_name}, Description: {food_description}, Price: {food_price}")

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
            cart()
        elif n == "3":
            break


def product_review():
    pass

def main():
    user = None

    while True:
        print("________________________________")
        print("         Customer Page")
        print("________________________________")
        if user:
            print(f"***Welcome back, {user[0]}.\N{grinning face}***")
        print("1. Shopping Cart")
        print("2. Order")
        print("3. Product Review")
        print("4. Exit")

        n = input("Enter your choice (1-4): ")
        if n == "1":
            cart()
        elif n == "2":
            order()
        elif n == "3":
            if user:
                cart(user)
            else:
                print("Please login to view more.")
        elif n == "4":
            print("See you again.")
            break
        else:
            print("Invalid choice, please enter again (1-5): ")


if __name__ == "__main__":
    main()
    #Menu save in txt file, and baker customer refer to the txt file.


if __name__ == "__main__":
    main()
    #Menu save in txt file, and baker customer refer to the txt file.

