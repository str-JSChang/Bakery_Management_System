import json
import hashlib

#banner
def print_banner():
    print("   ___       __                  __  ___                                       __    ____         __          ")
    print("  / _ )___ _/ /_____ ______ __  /  |/  /__ ____  ___ ____ ____ __ _  ___ ___  / /_  / __/_ _____ / /____ __ _ ")
    print(" / _  / _ `/  '_/ -_) __/ // / / /|_/ / _ `/ _ \/ _ `/ _ `/ -_)  ' \/ -_) _ \/ __/ _\ \/ // (_-</ __/ -_)  ' |")
    print("/____/\_,_/_/\_\\__/_/  \_, / /_/  /_/\_,_/_//_/\_,_/\_, /\__/_/_/_/\__/_//_/\__/ /___/\_, /___/\__/\__/_/_/_/")
    print("                       /___/                        /___/                             /___/                   ")
    print("")

# Main Menu
def display_main_menu():
    while True:
        print("Welcome to Bakery Management System")
        print("1. Login. ")
        print("2. Signup. ")
        print("3. Exit the program. ")
        while True:
            try:
                choice = int(input("Please enter your selection (1-3): "))
                if choice in [1, 2, 3]:
                    break
                else:
                    print("Please enter a valid option between 1 to 3.")
            except ValueError:
                print("Invalid Input. Error occurs, Please enter NUMBER ONLY between 1 and 3.")
        
        if choice == 1:
            login()
        elif choice == 2:
            signup()
        elif choice == 3:
            print("Exiting program...")
            exit()


# Manager Login
# Check Line112 - 2023-08-23
def ManagerLogin():
    print("To register as staff, your account must be 'Manager' to register staff account.")
    manager_username = input("Please enter Manager username: ")
    manager_password = input("Please enter Manager password: ")
    confirmManager_password = input("Confirm Manager password: ")

    # confirm manager password
    if confirmManager_password == manager_password:
            try:
                with open("manager_acc.json", "r") as file:
                    existing_manager_acc = json.load(file)

                if manager_username in existing_manager_acc:
                    manager_stored_password = existing_manager_acc[manager_username]['manager_password']
                    hashing_manager_password = hashlib.md5(manager_password.encode()).hexdigest()
                    if manager_stored_password == hashing_manager_password:
                        print("Welcome back, Mr.Jason")
                    else:
                        print("Invalid password")
                else:
                    print("Manager username not found")

            except FileNotFoundError:
                print("ERROR, NO MANAGER ACCOUNT EXIST IN THE SYSTEM, PLEASE CONTACT SYSTEM ADMINSTRATOR IMMEDIATELY")
                signup()
    else:
        print("Passwords do not match")

# Sign Up system
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
            print("Invalid Input. Error occurs, Please enter NUMBER ONLY between 1 and 3. ")


    if signupOption == 1:
        email = input("Please fill up your email address: ")
        pwd = input("Please enter your password that you want to register: ")
        confirmPwd = input("Confirm password: ")

        if confirmPwd == pwd:
            enc = pwd.encode()
            hashed_pwd = hashlib.md5(enc).hexdigest()
            user_data = {
                "email": email,
                "password": hashed_pwd
            }

            try:
                with open("users.json", "r") as file:
                    existing_data = json.load(file)
            except json.JSONDecodeError:
                    existing_data = {}
            except FileNotFoundError:
                    existing_data = {}

            if email in existing_data:
                print("An account with this email already exists.\n")
                return

            existing_data[email] = user_data

            with open("users.json", "w") as file:
                json.dump(existing_data, file, indent = 4)
            print("You have registered successfully.")
        else:
            print("The password doesn't matched. \n")

    if signupOption == 2:
        ManagerLogin()
        # Do I need to make managerlogin as a function? or no need, just proceduring it as a part of signing up staff?

    if signupOption == 3:
        exit()
        

# Login System
def login():
    print("--------Login Page--------")
    email = input("Please enter your email address: ")
    pwd = input("Please enter your password: ")

    try:
        with open("users.json", "r") as file:
            user_data = json.load(file)
        try:
            if user_data[email]['password'] == hashlib.md5(pwd.encode()).hexdigest():
                print("Login successful!")
            else:
                print("Account exist, but wrong password.")
        # When no account founded in users.json
        except KeyError:
            print("Account not found.\n","Please make sure your account is registered or ensure your email and password is correct.")
    except FileNotFoundError:
            print("Error: 'users.json' file not found.")
            print("PLEASE CONTACT ADMINSTRATOR IMMEDIATELY")
    except json.JSONDecodeError:
            print("Error: Unable to read user data.")
            print("PLEASE CONTACT ADMINSTRATOR IMMEDIATELY")
    

# load data from json (users)

# load data from json (inventory)

# load data from json (orders)

# load data from json (feedback)

# load data from json (sales)

# load data from json (recipes)



# Main program
def main():
    print_banner()
    display_main_menu()


if __name__ == "__main__":
    main()







