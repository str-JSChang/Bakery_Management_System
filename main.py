import json
import os
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
    print("Welcome to Bakery Management System")
    print("1. Login. ")
    print("2. Signup. ")
    print("3. Exit the program. ")

# Sign Up system
def signup():
    email = input("Enter email address: ")
    pwd = input("Enter password: ")
    confirmPassword = input("Confirm password: ")

    if confirmPassword == pwd:
        enc = confirmPassword.encode()
        hash1 = hashlib.md5(enc).hexdigest()
                # data.txt need to change to ur json file
        with open("data.txt", "w") as f:
            f.write(email + "\n")
            f.write(hash1)
        f.close()
        print("You have registered successfully!")
    else:
        print("The password doesn't matched. \n")

# Login System
def login():
    email = input("Please enter your email address: ")
    pwd = input("Please enter your password: ")

    auth = pwd.encode()
    auth_hash = hashlib.md5(auth).hexdigest()
    with open("data.txt", "r") as f:
        stored_email, stored_pwd = f.read().split("\n")
    f.close()

    if email == stored_email and auth_hash == stored_pwd:
        print("Login Success!")
    else:
        print("Login Failed! \n")

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







