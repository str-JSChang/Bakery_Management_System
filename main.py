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
        choice = input("Please select your options.: ")

        if choice == '1':
            login()
        elif choice == '2':
            signup()
        elif choice == '3':
            print("The program are going to exit.")
            exit()
        else:
            print("Invalid Choice.")

# Sign Up system
def signup():
    print("----------Signup page----------")
    print("1. Register as Customer")
    print("2. Register as Staff")
    print("3. Exit")
    signupOption = int(input("Please enter your selection (1-3):  "))


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

            with open("users.json", "r") as file:
                try:
                    existing_data = json.load(file)
                except json.JSONDecodeError:
                    existing_data = {}

            existing_data[email] = user_data

            with open("users.json", "w") as file:
                json.dump(existing_data, file, indent = 4)
            print("You have registered successfully.")
        else:
            print("The password doesn't matched. \n")

# Login System
def login():
    email = input("Please enter your email address: ")
    pwd = input("Please enter your password: ")

    try:
        with open("users.json", "r") as file:
            user_data = json.load(file)
        
        if user_data[email]['password'] == hashlib.md5(pwd.encode()).hexdigest():
            print("Login successful!")
        else:
            print("Invalid email or password.\n" ,"Are you sure that your account is registered before?")
    except FileNotFoundError:
            print("Error: 'users.json' file not found.")
            print("PLEASE CONTACT ADMINSTRATOR IMMEDIATELY")
            display_main_menu()
    except json.JSONDecodeError:
            print("Error: Unable to read user data.")
            print("PLEASE CONTACT ADMINSTRATOR IMMEDIATELY")
            display_main_menu()
    

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







