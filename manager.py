import hashlib

def managerPage():
    print("----------Manager's page----------")
    print("1. Manage System Credentials")
    print("2. Manage Orders")
    print("3. Manage Company Financials")
    print("4. Manage Inventory")
    print("5. View Customer Feedback")
    print("6. Exit")

    while True:
        try:
            choice = int(input("Please enter your selection (1-6): "))
            if choice == 1:
                manage_credentials()
            elif choice == 2:
                manage_orders()
            elif choice == 3:
                manage_financials()
            elif choice == 4:
                manage_inventory()
            elif choice == 5:
                view_customer_feedback()
            elif choice == 6:
                print("Exiting Manager's page...")
                return
            else:
                print("Please enter a valid option between 1 to 6.")
        except ValueError:
            print("Invalid Input. Error occurs, Please enter NUMBER ONLY between 1 and 6.")

def manage_credentials():
    print("----------Manage System Credentials----------")
    print("1. View Credentials")
    print("2. Add New User")
    print("3. Update Existing User")
    print("4. Delete User")
    print("5. Back to Manager's page")

    while True:
        try:
            choice = int(input("Please enter your selection (1-5): "))
            if choice == 1:
                view_credentials()
            elif choice == 2:
                add_new_user()
            elif choice == 3:
                update_user()
            elif choice == 4:
                delete_user()
            elif choice == 5:
                print("Returning to Manager's page...")
                return
            else:
                print("Please enter a valid option between 1 to 5.")
        except ValueError:
            print("Invalid Input. Error occurs, Please enter NUMBER ONLY between 1 and 5.")


def manage_orders():
    print("----------Manage Orders----------")
    # Code to manage orders
    pass

def manage_financials():
    print("----------Manage Company Financials----------")
    # Code to manage company financials
    pass

def manage_inventory():
    print("----------Manage Inventory----------")
    # Code to manage inventory
    pass

def view_customer_feedback():
    print("----------View Customer Feedback----------")
    # Code to view customer feedback
    pass
