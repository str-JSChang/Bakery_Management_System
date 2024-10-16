import hashlib
from Customer import main_customer_page
from baker import baker_menu
from cashier import cashier_main
from manager import managerPage

#banner
def print_banner():
    print("    _                            ___       _                 ")
    print("   /_\__ _____ _ _  __ _ ___ _ _| _ ) __ _| |_____ _ _ _  _  ")
    print("  / _ \ V / -_) ' \/ _` / -_) '_| _ \/ _` | / / -_) '_| || |")
    print(" /_/ \_\_/\___|_||_\__, \___|_| |___/\__,_|_\_\___|_|  \_, |")
    print("                   |___/                               |__/")
    print("")
    print("Welcome to Avenger Bakery")

def login():
    print("--------Login Page--------")
    username = input("Please enter your username: ")
    pwd = input("Please enter your password: ")

    try:
        with open("user_data.csv", "r") as file:
            for line in file:
                fields = line.strip().split(",")
                if fields[2] == username and fields[3] == hashlib.md5(pwd.encode()).hexdigest():
                    print(f"Login successful! Welcome, {fields[0]}.")
                    if fields[4] == "manager":
                        # Proceed to customer functions
                        managerPage()
                    elif fields[4] == "customer":
                        # Proceed to manager functions
                        main_customer_page(username)
                    elif fields[4] == "cashier":
                        # Proceed to baker functions
                        cashier_main()
                    elif fields[4] == "baker":
                        # Proceed to cashier functions
                        baker_menu()
                    else:
                        print("Invalid user role.")
                    return
            print("Account not found or incorrect password.")
    except FileNotFoundError:
        print("Error: 'user_data.csv' file not found.")
        print("PLEASE CONTACT ADMINISTRATOR IMMEDIATELY")

def validate_email():
    while True:
        email = input("Please enter your email address: ").strip()
        if email and email.endswith("@gmail.com"):
            return email
        elif not email:
            print("Email cannot be empty. Please try again.")
        else:
            print("Invalid email. Please use a valid domain. eg: (@gmail.com).")

def signup():
    print("----------Signup page----------")
    print("1. Register as Customer")
    print("2. Register as Staff")
    print("3. Exit")

    while True:
        try:
            signupOption = int(input("Please enter your selection (1-3):  "))
            if signupOption in [1, 2, 3]:
                break
            else:
                print("Please enter a valid option between 1 to 3. ")
        except ValueError:
            print("Invalid Input. Error occurs, Please enter NUMBER ONLY between 1 and 3.")

    if signupOption == 1:
        register_customer()
    elif signupOption == 2:
        register_staff()
    elif signupOption == 3:
        exit()

def register_customer():
    name = input("Please enter your name: ")
    email = validate_email()
    username = input("Please enter your username: ")
    pwd = input("Please enter your password: ")
    confirmPwd = input("Confirm password: ")

    if confirmPwd == pwd:
        hashed_pwd = hashlib.md5(pwd.encode()).hexdigest()
        try:
            with open("user_data.csv", "r") as file:
                for line in file:
                    fields = line.strip().split(",")
                    if fields[1] == email or fields[2] == username:
                        print("The account has already existed.")
                        return
        except FileNotFoundError:
            print("Error: File not found.")
            print("PLEASE CONTACT ADMINISTRATOR IMMEDIATELY")

        with open("user_data.csv", "a") as file:
            file.write(f"{name},{email},{username},{hashed_pwd},customer\n")
        print("You have registered successfully.")
    else:
        print("The passwords don't match.")

def register_staff():
    print("To register staff account, your account must be 'Manager' to register staff account.")
    manager_username = input("Please enter Manager username: ")
    manager_password = input("Please enter Manager password: ")
    confirmManager_password = input("Confirm Manager password: ")

    if confirmManager_password == manager_password:
        try:
            with open("user_data.csv", "r") as file:
                for line in file:
                    fields = line.strip().split(",")
                    if fields[2] == manager_username and fields[3] == hashlib.md5(manager_password.encode()).hexdigest() and fields[4] == "manager":
                        staff_name = input("Please enter the staff's name: ")
                        staff_id = input("Please enter the staff's ID: ")
                        staff_username = input("Please enter the staff's username: ")
                        staff_email = validate_email()
                        staff_role = input("Please enter the staff's role: ")
                        staff_pwd = input("Please enter the staff's password: ")
                        confirmStaff_pwd = input("Confirm the staff's password: ")

                        # check staff account exist
                        for line in file:
                            fields = line.strip().split(",")
                            if len(fields) >= 5:
                                if fields[2] == staff_username or fields[1] == staff_email or (len(fields) >= 6 and fields[5] == staff_id):
                                    print("This staff account already exists")
                                    return

                        if confirmStaff_pwd == staff_pwd:
                            hashed_pwd = hashlib.md5(staff_pwd.encode()).hexdigest()
                            with open("user_data.csv", "a") as file:
                                file.write(f"{staff_name},{staff_email},{staff_username},{hashed_pwd},{staff_role},{staff_id}\n")
                            print("You have registered the staff successfully.")
                        else:
                            print("The passwords don't match.")
                        return
                print("Invalid manager credentials.")
        except FileNotFoundError:
            print("Error: File not found.")
            print("PLEASE CONTACT ADMINISTRATOR IMMEDIATELY")
    else:
        print("The passwords don't match.")

def main():
    print_banner()

    while True:
        print("Welcome to Bakery Management System")
        print("1. Login")
        print("2. Signup")
        print("3. Exit the program")

        try:
            choice = int(input("Please enter your selection (1-3): "))
            if choice == 1:
                login()
            elif choice == 2:
                signup()
            elif choice == 3:
                print("Exiting program...")
                exit()
            else:
                print("Please enter a valid option between 1 to 3.")
        except ValueError:
            print("Invalid Input. Error occurs, Please enter NUMBER ONLY between 1 and 3.")

if __name__ == "__main__":
    main()
