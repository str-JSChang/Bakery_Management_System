import hashlib
from main import login, validate_email, register_customer, register_staff

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
                return manage_credentials()
            elif choice == 2:
                return manage_orders()
            elif choice == 3:
                return manage_financials()
            elif choice == 4:
                return manage_inventory()
            elif choice == 5:
                return view_customer_feedback()
            elif choice == 6:
                print("Exiting Manager's page...")
                return
            else:
                print("Please enter a valid option between 1 to 6.")
        except ValueError:
            print("Invalid Input. Error occurs, Please enter NUMBER ONLY between 1 and 6.")

# CREDENTIALS PART
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
                return managerPage()
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
    
    return managerPage()

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
                print("\nUpdated user data:")
                view_credentials()
            elif choice == 2:
                register_staff()
                print("\nUpdated user data:")
                view_credentials()
            elif choice == 3:
                return manage_credentials()
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
                if new_email:
                    new_email = validate_email()
                new_role = input("Enter new role (or press enter to keep current): ")
                
                user[0] = new_name if new_name else user[0]
                user[1] = new_email if new_email else user[1]
                user[4] = new_role if new_role else user[4]
                
                lines[i] = ",".join(user) + "\n"
                updated = True
                break
            i += 1
        
        if updated:
            with open("user_data.csv", "w") as file:
                file.writelines(lines)
            print("User updated successfully.")
            print("\nUpdated user data:")
            view_credentials()
        else:
            print("User not found.")
    except IOError:
        print("Error: Unable to update user.")
    
    return managerPage()

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
        
        if deleted:
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
    
    return managerPage()

# ORDERS
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
                print("Returning to Manager's page...")
                return managerPage()
            else:
                print("Please enter a valid option between 1 to 3.")
        except ValueError:
            print("Invalid Input. Error occurs, Please enter NUMBER ONLY between 1 and 3.")
    

def view_all_orders():
    try:
        with open("orders.csv", "r") as file:
            print("----------All Orders----------")
            for line in file:
                order = line.strip().split(",")
                print(f"Order ID: {order[0]}, Customer: {order[1]}, Items: {order[2]}, Total: {order[3]}, Status: {order[4]}")
    except FileNotFoundError:
        print("Error: 'orders.csv' file not found.")
    
    return managerPage()

def update_order_status():
    order_id = input("Enter the Order ID to update: ")
    new_status = input("Enter the new status: ")

    try:
        with open("orders.csv", "r") as file:
            lines = file.readlines()
        
        updated = False
        i = 0
        while i < len(lines):
            order = lines[i].strip().split(",")
            if order[0] == order_id:
                order[4] = new_status
                lines[i] = ",".join(order) + "\n"
                updated = True
                break
            i += 1
        
        if updated:
            with open("orders.csv", "w") as file:
                file.writelines(lines)
            print("Order status updated successfully.")
        else:
            print("Order not found.")
    except IOError:
        print("Error: Unable to update order status.")
    
    return managerPage()

# FINANCIALS
def manage_financials():
    print("----------Manage Company Financials----------")
    print("1. View Financial Summary")
    print("2. Add Income")
    print("3. Add Expense")
    print("4. Back to Manager's page")

    while True:
        try:
            choice = int(input("Please enter your selection (1-4): "))
            if choice == 1:
                pass# view_financial_summary()
            elif choice == 2:
                pass# add_income()
            elif choice == 3:
                pass# add_expense()
            elif choice == 4:
                print("Returning to Manager's page...")
                return managerPage()
            else:
                print("Please enter a valid option between 1 to 4.")
        except ValueError:
            print("Invalid Input. Error occurs, Please enter NUMBER ONLY between 1 and 4.")
    
# INVENTORY
def manage_inventory():
    print("----------Manage Inventory----------")
    print("1. View Inventory")
    print("2. Add New Item")
    print("3. Update Item Quantity")
    print("4. Remove Item")
    print("5. Back to Manager's page")

    while True:
        try:
            choice = int(input("Please enter your selection (1-5): "))
            if choice == 1:
                view_inventory()
            elif choice == 2:
                add_inventory_item()
            elif choice == 3:
                update_item_quantity()
            elif choice == 4:
                remove_inventory_item()
            elif choice == 5:
                print("Returning to Manager's page...")
                return managerPage()
            else:
                print("Please enter a valid option between 1 to 5.")
        except ValueError:
            print("Invalid Input. Error occurs, Please enter NUMBER ONLY between 1 and 5.")
    


def view_inventory():
    try:
        with open("inventory.csv", "r") as file:
            print("----------Inventory----------")
            for line in file:
                item = line.strip().split(",")
                print(f"Item: {item[0]}, Quantity: {item[1]}, Cost: {item[2]}")
    except FileNotFoundError:
        print("Error: 'inventory.csv' file not found.")
    
    return managerPage()

def add_inventory_item():
    item_name = input("Enter item name: ")
    quantity = input("Enter quantity: ")
    cost = input("Enter cost per unit: ")
    
    try:
        with open("inventory.csv", "a") as file:
            file.write(f"{item_name},{quantity},{cost}\n")
        print("Item added successfully.")
    except IOError:
        print("Error: Unable to add item.")
    
    return managerPage()

def update_item_quantity():
    item_name = input("Enter item name to update: ")
    new_quantity = input("Enter new quantity: ")
    
    try:
        with open("inventory.csv", "r") as file:
            lines = file.readlines()
        
        updated = False
        i = 0
        while i < len(lines):
            item = lines[i].strip().split(",")
            if item[0] == item_name:
                item[1] = new_quantity
                lines[i] = ",".join(item) + "\n"
                updated = True
                break
            i += 1
        
        if updated:
            with open("inventory.csv", "w") as file:
                file.writelines(lines)
            print("Item quantity updated successfully.")
        else:
            print("Item not found.")
    except IOError:
        print("Error: Unable to update item quantity.")
    
    return managerPage()

def remove_inventory_item():
    item_name = input("Enter item name to remove: ")
    
    try:
        with open("inventory.csv", "r") as file:
            lines = file.readlines()
        
        updated_lines = []
        for line in lines:
            if line.strip().split(",")[0] != item_name:
                updated_lines.append(line)
        
        if len(updated_lines) < len(lines):
            with open("inventory.csv", "w") as file:
                for line in updated_lines:
                    file.write(line)
            print("Item removed successfully.")
        else:
            print("Item not found.")
    except IOError:
        print("Error: Unable to remove item.")
    
    return managerPage()

# FEEDBACK
def view_customer_feedback():
    try:
        with open("feedback.csv", "r") as file:
            print("----------Customer Feedback----------")
            for line in file:
                feedback = line.strip().split(",")
                print(f"Customer: {feedback[0]}, Product: {feedback[1]}, Rating: {feedback[2]}, Comment: {feedback[3]}")
    except FileNotFoundError:
        print("Error: 'feedback.csv' file not found.")
    
    return managerPage()

if __name__ == "__main__":
    managerPage()
