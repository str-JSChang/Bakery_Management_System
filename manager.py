from main import main,validate_email, register_customer, register_staff
from baker import inventory
from cashier import generate_reports, calculate_total_sales, calculate_profit

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
                return
            else:
                print("Please enter a valid option between 1 to 5.")
        except ValueError:
            print("Invalid Input. Error occurs, Please enter NUMBER ONLY between 1 and 5.")

def view_credentials():
    try:
        with open("user_data.csv", "r") as file:
            print("----------User Credentials----------")
            for line in file:
                user = line.strip().split(",")
                print(f"Name: {user[0]}, Email: {user[1]}, Username: {user[2]}, Role: {user[4]}")
    except FileNotFoundError:
        print("Error: 'user_data.csv' file not found.")

def add_new_user():
    print("----------Add New User----------")
    print("1. Add Customer")
    print("2. Add Staff")
    print("3. Back")

    while True:
        try:
            choice = int(input("Please enter your selection (1-3): "))
            if choice == 1:
                register_customer()
            elif choice == 2:
                register_staff()
            elif choice == 3:
                return
            else:
                print("Please enter a valid option between 1 to 3.")
        except ValueError:
            print("Invalid Input. Error occurs, Please enter NUMBER ONLY between 1 and 3.")

def update_user():
    print("----------Update Existing User----------")
    username = input("Enter username of user to update: ")
    
    try:
        with open("user_data.csv", "r") as file:
            lines = file.readlines()
        
        updated = False
        i = 0
        while i < len(lines):
            user = lines[i].strip().split(",")
            if user[2] == username:
                print("Current user details:")
                print(f"Name: {user[0]}, Email: {user[1]}, Role: {user[4]}")
                
                new_name = input("Enter new name (or press enter to keep current): ")
                new_email = input("Enter new email (or press enter to keep current): ")
                if new_email == True:
                    new_email = validate_email()
                new_role = input("Enter new role (or press enter to keep current): ")
                
                user[0] = new_name if new_name else user[0]
                user[1] = new_email if new_email else user[1]
                user[4] = new_role if new_role else user[4]
                
                lines[i] = ",".join(user) + "\n"
                updated = True
                break
            i += 1
        
        if updated == True:
            with open("user_data.csv", "w") as file:
                file.writelines(lines)
            print("User updated successfully.")
            print("\nUpdated user data:")
            view_credentials()
        else:
            print("User not found.")
    except IOError:
        print("Error: Unable to update user.")

def delete_user():
    print("----------Delete User----------")
    username = input("Enter username of user to delete: ")
    
    try:
        with open("user_data.csv", "r") as file:
            lines = file.readlines()
        
        updated_lines = []
        deleted = False
        for line in lines:
            if line.strip().split(",")[2] != username:
                updated_lines.append(line)
            else:
                deleted = True
        
        if deleted == True:
            with open("user_data.csv", "w") as file:
                for line in updated_lines:
                    file.write(line)
            print("User deleted successfully.")
            print("\nUpdated user data:")
            view_credentials()
        else:
            print("User not found.")
    except IOError:
        print("Error: Unable to delete user.")

def manage_orders():
    print("----------Manage Orders----------")
    print("1. View All Orders")
    print("2. Update Order Status")
    print("3. Back to Manager's page")

    while True:
        try:
            choice = int(input("Please enter your selection (1-3): "))
            if choice == 1:
                view_all_orders()
            elif choice == 2:
                update_order_status()
            elif choice == 3:
                return
            else:
                print("Please enter a valid option between 1 to 3.")
        except ValueError:
            print("Invalid Input. Error occurs, Please enter NUMBER ONLY between 1 and 3.")

def view_all_orders():
    try:
        with open("order.txt", "r") as file:
            print("----------All Orders----------")
            for line in file:
                print(line.strip())
    except FileNotFoundError:
        print("Error: 'order.txt' file not found.")

def update_order_status():
    order_number = input("Enter the Order Number to update: ")
    new_status = input("Enter the new status: ")

    try:
        with open("order.txt", "r") as file:
            lines = file.readlines()
        
        updated = False
        i = 0
        while i < len(lines):
            if f"Order Number: {order_number}" in lines[i]:
                lines[i+1] = f"Order Status: {new_status}\n"
                updated = True
                break
            i += 1
        
        if updated == True:
            with open("order.txt", "w") as file:
                file.writelines(lines)
            print("Order status updated successfully.")
        else:
            print("Order not found.")
    except IOError:
        print("Error: Unable to update order status.")

def manage_financials():
    print("----------Manage Company Financials----------")
    print("1. View Financial Summary")
    print("2. Generate Sales Report")
    print("3. Back to Manager's page")

    while True:
        try:
            choice = int(input("Please enter your selection (1-3): "))
            if choice == 1:
                view_financial_summary()
            elif choice == 2:
                generate_reports()
            elif choice == 3:
                return
            else:
                print("Please enter a valid option between 1 to 3.")
        except ValueError:
            print("Invalid Input. Error occurs, Please enter NUMBER ONLY between 1 and 3.")

def view_financial_summary():
    total_sales = calculate_total_sales()
    profit = calculate_profit()
    
    print("----------Financial Summary----------")
    print(f"Total Sales: RM{total_sales:.2f}")
    print(f"Total Profit: RM{profit:.2f}")

def manage_inventory():
    inventory()

def view_customer_feedback():
    print("----------Customer Feedback----------")
    try:
        with open("feedback.txt", "r") as file:
            feedback_found = False
            for line in file:
                print(line.strip())
                feedback_found = True
            if feedback_found == False:
                print("No feedback available.")
    except FileNotFoundError:
        print("Error: 'feedback.txt' file not found.")
    except IOError:
        print("Error: Unable to read the feedback file.")

if __name__ == "__main__":
    main()
