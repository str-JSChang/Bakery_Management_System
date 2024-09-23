import csv
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
                choice = int(input("Please enter your selection (1-3): "))  # REPROMPT WITH ERRORS EXCEPTION HANDLING
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


def validate_email():
    while True:
        email = input("Please enter your email address: ").strip()
        if email and email.endswith("@gmail.com"):
            return email
        elif not email:
            print("Email cannot be empty. Please try again.")
        else:
            print("Invalid email. Please use a valid domain. eg: (@gmail.com).")


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
            # Create a open file object, together with DictReader, create a Reader object using DictReader to find the header, and return the key values.
            with open("manager_acc.csv", "r", newline='') as file:
                reader = csv.DictReader(file)
                existing_manager_acc = [row for row in reader]

            # Using "List Comprehension" instead of building global empty list in the beginning.
            manager_accounts = [account for account in existing_manager_acc if account['Username'] == manager_username]

            if manager_accounts:
                manager_stored_password = manager_accounts[0]['Password']
                hashing_manager_password = hashlib.md5(manager_password.encode()).hexdigest()
                if manager_stored_password == hashing_manager_password:
                    print(f"Welcome back, {manager_accounts[0]['Name']}")
                else:
                    print("Invalid password")
            else:
                print("Manager username not found")

        except FileNotFoundError:
            print("ERROR, NO MANAGER ACCOUNT EXISTS IN THE SYSTEM, PLEASE CONTACT SYSTEM ADMINISTRATOR IMMEDIATELY")
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
        name = input("Please enter your name: ")
        email = validate_email()
        username = input("Please enter your username: ")
        pwd = input("Please enter your password: ")
        confirmPwd = input("Confirm password: ")
        
        if confirmPwd == pwd:
            hashed_pwd = hashlib.md5(pwd.encode()).hexdigest()
            
            # Validate the existing account
            with open("customer_data.csv","r", newline='') as file:
                reader = csv.DictReader(file)
                existing_emails = [row['Email'] for row in reader]
                existing_usernames = [row['Username'] for row in reader]
            if email in existing_emails or  username in existing_usernames:
                print("The account has existed.")
                return

            # Append new row of data.
            with open("customer_data.csv", "a", newline='') as file:
                writer = csv.writer(file)
                writer.writerow([name, email, username, hashed_pwd, "customer"])
            print("You have registered successfully.")
        else:
            print("The passwords doesn't match. \n")

    if signupOption == 2:
        ManagerLogin()
        # Do I need to make managerlogin as a function? or no need, just proceduring it as a part of signing up staff?

    if signupOption == 3:
        exit()
        

def staffSignup():
    name = input("Please enter your name:")
    staffid = input("Please enter your Staff ID that you want to register: ")
    username = input("Please enter your username: ")
    email = validate_email
    pwd = input("Please enter your password: ")
    confirmPwd = input("Please confirm your password: ")
    
    if confirmPwd == pwd:
        hashed_pwd = hashlib.md5(pwd.encode()).hexdigest()

# Login System
def login():
    print("--------Login Page--------")
    username = input("Please enter your username: ")
    pwd = input("Please enter your password: ")

    try:
        with open("customer_data.csv", "r", newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Username'] == username:
                    if row['Password'] == hashlib.md5(pwd.encode()).hexdigest():
                        print(f"Login successful! Welcome, {row.get('Name', username)}.")
                        return
                    else:
                        print("Account exists, but wrong password.")
                        return
            print("Account not found.\n", "Please make sure your account is registered or ensure your username and password are correct.")
    except FileNotFoundError:
        print("Error: 'customer_data.csv' file not found.")
        print("PLEASE CONTACT ADMINISTRATOR IMMEDIATELY")


# Main program
def main():
    print_banner()
    display_main_menu()


if __name__ == "__main__":
    main()
