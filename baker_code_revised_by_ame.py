# Home menu
def home():
    while True:
        print("--------Baker--------")
        print("1. Menu")
        print("2. Recipe")
        print("3. Inventory")
        print("4. Product Record")
        print("5. Equipment")
        print("6. Exit")
        option = input("Enter your choice (1-6): ")
        if option == "1":
            menu()
        elif option == "2":
            recipe()
        elif option == "3":
            inventory()
        elif option == "4":
            productrecord()
        elif option == "5":
            equipment()
        elif option == "6":
            exit()
        else:
            print("Invalid Input, Please enter a number only.")

def menu():
    print("------Baker's Menu------")
    print("What do you want to do?")
    print("1. Create new product ")
    print("2. View all products")
    print("3. Update existing products")
    print("4. Delete product")
    print("5. Back")
    while True:
        try:
            choice = int(input("Please enter your selection (1-5): "))
            if choice in [1, 2, 3, 4, 5]:
                break
            else:
                print("Please enter a valid option between 1 to 5.")
        except ValueError:
            print("Invalid Input. Error occurs, Please enter NUMBER ONLY between 1 to 5")

    if choice == 1:
        user_input = input('Please enter "Product Name", "Price","Stocks" with double quote (eg:"Tiramisu Cake" , "RM59" , "12"): \n')
        menu = open('menu.txt','a')
        menu.write(user_input)

    elif choice == 2:
        pass
    elif choice == 3:
        pass
    elif choice == 4:
        pass
    elif choice == 5:
        home()
# Recipe, CRUD by Baker
def recipe():
    while True:
        print("------Avengers' Bakery Recipe------")
        print("1. Create")
        print("2. Update")
        print("3. Delete")
        print("4. Return to Home")
        option = input("Choose which to operate (1-4): ")
        if option == "4":
            return
        else:
            print("Feature not implemented yet.")

# Inventory
# Inventory
def inventory():
    items = ["fruit", "flour", "egg", "sugar", "vanilla extract"]
    stock = {item: 0 for item in items}  # Initialize stock with 0 for all items

    while True:
        print("\n------ Inventory Management ------")
        print("Select an operation:")
        print("1. Update Stock")
        print("2. Delete Stock")
        print("3. Check Stock Levels")
        print("4. Return to Home")
        
        operation = input("Enter your choice (1-4): ")

        if operation == "1":
            print("\n--- Update Stock ---")
            for i, item in enumerate(items, start=1):
                print(f"{i}. {item.capitalize()}")
            item_choice = input(f"Select an item to update (1-{len(items)}): ")

            if item_choice.isdigit() and 1 <= int(item_choice) <= len(items):
                item = items[int(item_choice) - 1]
                while True:
                    try:
                        amount = int(input(f"Enter the new stock amount for {item}: "))
                        stock[item] = amount
                        print(f"{item.capitalize()} stock updated to {amount}.")
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
            else:
                print("Invalid choice. Please select a valid item.")

        elif operation == "2":
            print("\n--- Delete Stock ---")
            for i, item in enumerate(items, start=1):
                print(f"{i}. {item.capitalize()}")
            item_choice = input(f"Select an item to delete (1-{len(items)}): ")

            if item_choice.isdigit() and 1 <= int(item_choice) <= len(items):
                item = items[int(item_choice) - 1]
                if item in stock:
                    del stock[item]
                    print(f"{item.capitalize()} stock has been deleted.")
                else:
                    print(f"No stock recorded for {item}.")
            else:
                print("Invalid choice. Please select a valid item.")

        elif operation == "3":
            print("\n--- Check Stock Levels ---")
            print("Current stock levels:")
            for item, amount in stock.items():
                if amount == 0:
                    print(f"{item.capitalize()}: No stock recorded.")
                elif (item == "fruit" and amount < 10) or \
                     (item == "flour" and amount < 2) or \
                     (item == "egg" and amount < 20) or \
                     (item == "sugar" and amount < 2) or \
                     (item == "vanilla extract" and amount < 1):
                    print(f"{item.capitalize()}: {amount} (Warning! Need to purchase new stock!)")
                else:
                    print(f"{item.capitalize()}: {amount} (Sufficient stock)")

        elif operation == "4":
            return  # Return to Home

        else:
            print("Invalid input. Please select a valid operation.")


# Product Record
def productrecord():
    products = ["cake", "bread", "snacks"]
    records = {product: {"batch_number": None, "quantity": None, "expiration_date": None} for product in products}

    while True:
        print("\n------ Product Record Management ------")
        print("Select an operation:")
        print("1. Update Record")
        print("2. Delete Record")
        print("3. Check Records")
        print("4. Return to Home")
        
        operation = input("Enter your choice (1-4): ")

        if operation == "1":
            print("\n--- Update Record ---")
            for i, product in enumerate(products, start=1):
                print(f"{i}. {product.capitalize()}")
            product_choice = input(f"Select a product to update (1-{len(products)}): ")

            if product_choice.isdigit() and 1 <= int(product_choice) <= len(products):
                product = products[int(product_choice) - 1]
                print("Select what to update:")
                print("1. Batch Number & Quantity")
                print("2. Expiration Date")
                update_choice = input("Enter your choice (1-2): ")

                if update_choice == "1":
                    while True:
                        try:
                            batch_number = input(f"Enter the batch number for {product}: ")
                            quantity = int(input(f"Enter the quantity for {product}: "))
                            records[product]["batch_number"] = batch_number
                            records[product]["quantity"] = quantity
                            print(f"{product.capitalize()} record updated: Batch Number = {batch_number}, Quantity = {quantity}.")
                            break
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                
                elif update_choice == "2":
                    expiration_date = input(f"Enter the expiration date for {product} (YYYY-MM-DD): ")
                    records[product]["expiration_date"] = expiration_date
                    print(f"{product.capitalize()} record updated: Expiration Date = {expiration_date}.")
                
                else:
                    print("Invalid choice. Please select a valid option.")

            else:
                print("Invalid choice. Please select a valid product.")

        elif operation == "2":
            print("\n--- Delete Record ---")
            for i, product in enumerate(products, start=1):
                print(f"{i}. {product.capitalize()}")
            product_choice = input(f"Select a product to delete (1-{len(products)}): ")

            if product_choice.isdigit() and 1 <= int(product_choice) <= len(products):
                product = products[int(product_choice) - 1]
                if product in records:
                    del records[product]
                    print(f"{product.capitalize()} record has been deleted.")
                else:
                    print(f"No record found for {product}.")
            else:
                print("Invalid choice. Please select a valid product.")

        elif operation == "3":
            print("\n--- Check Records ---")
            print("Current product records:")
            for product, details in records.items():
                batch_number = details["batch_number"] if details["batch_number"] else "Not set"
                quantity = details["quantity"] if details["quantity"] else "Not set"
                expiration_date = details["expiration_date"] if details["expiration_date"] else "Not set"
                print(f"{product.capitalize()}: Batch Number = {batch_number}, Quantity = {quantity}, Expiration Date = {expiration_date}")

        elif operation == "4":
            return  # Return to Home

        else:
            print("Invalid input. Please select a valid operation.")

# Equipment
def equipment():
    equipment_items = ["oven", "fridge", "stand mixer"]
    records = {item: {"maintenance_period": None, "last_maintenance_date": None} for item in equipment_items}

    while True:
        print("\n------ Equipment Management ------")
        print("Select an operation:")
        print("1. Update Record")
        print("2. Delete Record")
        print("3. Check Records")
        print("4. Return to Home")
        
        operation = input("Enter your choice (1-4): ")

        if operation == "1":
            print("\n--- Update Record ---")
            for i, item in enumerate(equipment_items, start=1):
                print(f"{i}. {item.capitalize()}")
            item_choice = input(f"Select an equipment item to update (1-{len(equipment_items)}): ")

            if item_choice.isdigit() and 1 <= int(item_choice) <= len(equipment_items):
                item = equipment_items[int(item_choice) - 1]
                print("Select what to update:")
                print("1. Maintenance Period")
                print("2. Last Maintenance Date")
                update_choice = input("Enter your choice (1-2): ")

                if update_choice == "1":
                    maintenance_period = input(f"Enter the maintenance period for {item} (e.g., every 6 months): ")
                    records[item]["maintenance_period"] = maintenance_period
                    print(f"{item.capitalize()} record updated: Maintenance Period = {maintenance_period}.")
                
                elif update_choice == "2":
                    last_maintenance_date = input(f"Enter the last maintenance date for {item} (YYYY-MM-DD): ")
                    records[item]["last_maintenance_date"] = last_maintenance_date
                    print(f"{item.capitalize()} record updated: Last Maintenance Date = {last_maintenance_date}.")
                
                else:
                    print("Invalid choice. Please select a valid option.")

            else:
                print("Invalid choice. Please select a valid equipment item.")

        elif operation == "2":
            print("\n--- Delete Record ---")
            for i, item in enumerate(equipment_items, start=1):
                print(f"{i}. {item.capitalize()}")
            item_choice = input(f"Select an equipment item to delete (1-{len(equipment_items)}): ")

            if item_choice.isdigit() and 1 <= int(item_choice) <= len(equipment_items):
                item = equipment_items[int(item_choice) - 1]
                if item in records:
                    del records[item]
                    print(f"{item.capitalize()} record has been deleted.")
                else:
                    print(f"No record found for {item}.")
            else:
                print("Invalid choice. Please select a valid equipment item.")

        elif operation == "3":
            print("\n--- Check Records ---")
            print("Current equipment records:")
            for item, details in records.items():
                maintenance_period = details["maintenance_period"] if details["maintenance_period"] else "Not set"
                last_maintenance_date = details["last_maintenance_date"] if details["last_maintenance_date"] else "Not set"
                print(f"{item.capitalize()}: Maintenance Period = {maintenance_period}, Last Maintenance Date = {last_maintenance_date}")

        elif operation == "4":
            return  # Return to Home

        else:
            print("Invalid input. Please select a valid operation.")



# Start the program
home()
