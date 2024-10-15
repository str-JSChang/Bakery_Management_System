def baker_menu():
    print("----------Baker's Menu----------")
    print("1. Store Menu")
    print("2. Manage Recipes")
    print("3. Inventory check")
    print("4. Record Production Details")
    print("5. Report Equipment Issues")
    print("6. Exit")

    while True:
        try:
            choice = int(input("Please enter your selection (1-6): "))
            if choice == 1:
                store_menu()
            elif choice == 2:
                manage_recipes()
            elif choice == 3:
                inventory()
            elif choice == 4:
                record_production()
            elif choice == 5:
                report_equipment()
            elif choice == 6:
                print("Exiting Baker's Menu...")
                return
            else:
                print("Please enter a valid option between 1 to 6.")
        except ValueError:
            print("Invalid Input. Error occurs, Please enter NUMBER ONLY between 1 and 6.")

def store_menu():
    print("----------Store Menu----------")
    try:
        with open("menu.csv", "r") as file:
            menu_items = []
            for line in file:
                menu_items.append(line.strip().split(","))
    except FileNotFoundError:
        print("Error: 'menu.csv' file not found.")
        return

    while True:
        print("1. View Menu")
        print("2. Create New Menu Item")
        print("3. Update Existing Menu Item")
        print("4. Remove Menu Item")
        print("5. Back to Baker's Menu")
    
        try:
            choice = int(input("Please enter your selection (1-5): "))
            if choice == 1:
                display_menu(menu_items)
            elif choice == 2:
                menu_items = create_menu_item(menu_items)
            elif choice == 3:
                menu_items = update_menu_item(menu_items)
            elif choice == 4:
                menu_items = remove_menu_item(menu_items)
            elif choice == 5:
                print("Returning to Baker's Menu...")
                return
            else:
                print("Please enter a valid option between 1 to 5.")
        except ValueError:
            print("Invalid Input. Error occurs, Please enter NUMBER ONLY between 1 and 5.")

def save_menu(menu_items):
    try:
        with open("menu.csv", "w", newline="") as file:
            for item in menu_items:
                file.write(",".join(item) + "\n")
    except:
        print("Error occurred while updating the menu file.")

def display_menu(menu_items):
    print("----------Current Menu----------")
    print("ProductNumber,ProductName,category,price,stocksAmount")
    for item in menu_items[1:]:  
        print(",".join(item))

def create_menu_item(menu_items):
    print("----------Create New Menu Item----------")
    product_number = str(int(menu_items[-1][0]) + 1)
    product_name = input("Enter the product name: ")
    category = input("Enter the category: ")
    price = input("Enter the price (RM): ")
    stocks_amount = input("Enter the stocks amount: ")
    
    new_item = [product_number, product_name, category, f"RM{price}", stocks_amount]
    print(f"New item: {', '.join(new_item)}")
    confirm = input("Confirm to add this item? (y/n): ")
    if confirm.lower() == "y":
        menu_items.append(new_item)
        print("Item added successfully.")
        save_menu(menu_items)
    else:
        print("Item creation cancelled.")
    return menu_items

def update_menu_item(menu_items):
    print("----------Update Existing Menu Item----------")
    display_menu(menu_items)
    product_number = input("Enter the product number to update: ")
    for item in menu_items[1:]:  # Skip header row using slicing by init the first index 0 to second index 1
        if item[0] == product_number:
            print(f"Updating {item[1]}")
            item[1] = input(f"Enter new product name (current: {item[1]}): ") or item[1]
            item[2] = input(f"Enter new category (current: {item[2]}): ") or item[2]
            item[3] = input(f"Enter new price (current: {item[3]}): ") or item[3]
            item[4] = input(f"Enter new stocks amount (current: {item[4]}): ") or item[4]
            print(f"Updated item: {', '.join(item)}")
            confirm = input("Confirm the update? (y/n): ")
            if confirm.lower() == "y":
                print("Item updated successfully.")
                save_menu(menu_items)
            else:
                print("Update cancelled.")
            return menu_items
    print("Item not found.")
    return menu_items

def remove_menu_item(menu_items):
    print("----------Remove Menu Item----------")
    display_menu(menu_items)
    product_number = input("Enter the product number to remove: ")
    for item in menu_items[1:]:  
        if item[0] == product_number:
            print(f"Removing {item[1]} - Price: {item[3]}")
            confirm = input("Confirm the removal? (y/n): ")
            if confirm.lower() == "y":
                menu_items.remove(item)
                print("Item removed successfully.")
                save_menu(menu_items)
            else:
                print("Removal cancelled.")
            return menu_items
    print("Item not found.")
    return menu_items

def manage_recipes():
    print("----------Manage Recipes----------")
    try:
        with open("recipes.txt", "r") as file:
            recipes = []
            for line in file:
                parts = line.strip().split("|")
                if len(parts) >= 3:
                    name = parts[0].strip()
                    ingredients = parts[1].strip()
                    instructions = "|".join(parts[2:]).strip()
                    recipes.append([name, ingredients, instructions])
    except FileNotFoundError:
        print("Error: 'recipes.txt' file not found.")

    while True:
        print("1. View Recipes")
        print("2. Add New Recipe")
        print("3. Update Existing Recipe")
        print("4. Remove Recipe")
        print("5. Back to Baker's Menu")
    
        try:
            choice = int(input("Please enter your selection (1-5): "))
            if choice == 1:
                display_recipes(recipes)
            elif choice == 2:
                recipes = add_recipe(recipes)
            elif choice == 3:
                recipes = update_recipe(recipes)
            elif choice == 4:
                recipes = remove_recipe(recipes)
            elif choice == 5:
                save_recipes(recipes)
                print("Returning to Baker's Menu...")
                baker_menu()
            else:
                print("Please enter a valid option between 1 to 5.")
        except ValueError:
            print("Invalid Input. Error occurs, Please enter NUMBER ONLY between 1 and 5.")

def save_recipes(recipes):
    try:
        with open("recipes.txt", "w", newline="") as file:
            for recipe in recipes:
                file.write(f"{recipe[0]}|{recipe[1]}|{recipe[2]}\n")
        print("Recipes saved successfully.")
    except:
        print("Error occurred while updating the recipes file.")

def display_recipes(recipes):
    print("----------Current Recipes----------")
    for i in range(len(recipes)):
        print(f"{i+1}. {recipes[i][0]}")
    
    while True:
        choice = input("Enter recipe number to view details (or 0 to go back): ")
        if choice == '0':
            break
        try:
            index = int(choice) - 1
            if 0 <= index < len(recipes):
                print(f"\nName: {recipes[index][0]}")
                print(f"Ingredients: {recipes[index][1]}")
                print(f"Instructions: {recipes[index][2]}")
            else:
                print("Invalid recipe number.")
        except ValueError:
            print("Please enter a valid number.")

def add_recipe(recipes):
    print("----------Add New Recipe----------")
    name = input("Enter the recipe name: ")
    ingredients = input("Enter the ingredients (comma-separated): ")
    instructions = input("Enter the instructions: ")
    
    new_recipe = [name, ingredients, instructions]
    print(f"New recipe: {', '.join(new_recipe)}")
    confirm = input("Confirm to add this recipe? (y/n): ")
    if confirm.lower() == "y":
        recipes.append(new_recipe)
        print("Recipe added successfully.")
        save_recipes(recipes)
    else:
        print("Recipe creation cancelled.")
    return recipes

def update_recipe(recipes):
    print("----------Update Existing Recipe----------")
    for i in range(len(recipes)):
        print(f"{i+1}. {recipes[i][0]}")
    recipe_number = input("Enter the recipe number to update: ")
    try:
        index = int(recipe_number) - 1
        if 0 <= index < len(recipes):
            recipe = recipes[index]
            print(f"Updating {recipe[0]}")
            recipe[0] = input(f"Enter new recipe name (current: {recipe[0]}): ") or recipe[0]
            recipe[1] = input(f"Enter new ingredients (current: {recipe[1]}): ") or recipe[1]
            recipe[2] = input(f"Enter new instructions (current: {recipe[2]}): ") or recipe[2]
            print(f"Updated recipe: {', '.join(recipe)}")
            confirm = input("Confirm the update? (y/n): ")
            if confirm.lower() == "y":
                print("Recipe updated successfully.")
                save_recipes(recipes)
            else:
                print("Update cancelled.")
        else:
            print("Invalid recipe number.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    return recipes

def remove_recipe(recipes):
    print("----------Remove Recipe----------")
    for i in range(len(recipes)):
        print(f"{i+1}. {recipes[i][0]}")
    recipe_number = input("Enter the recipe number to remove: ")
    try:
        index = int(recipe_number) - 1
        if 0 <= index < len(recipes):
            recipe = recipes[index]
            print(f"Removing {recipe[0]}")
            confirm = input("Confirm the removal? (y/n): ")
            if confirm.lower() == "y":
                new_recipes = []
                for i in range(len(recipes)):
                    if i != index:
                        new_recipes.append(recipes[i])
                recipes = new_recipes
                print("Recipe removed successfully.")
                save_recipes(recipes)
            else:
                print("Removal cancelled.")
        else:
            print("Invalid recipe number.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    return recipes

def inventory():
    print("----------Inventory's Menu----------")
    try:
        with open("inventory.txt", "r") as file:
            inventory_items = []
            for line in file:
                if not line.startswith("Ingredients"):  
                    item = line.strip().split(",")
                    inventory_items.append(item)
    except FileNotFoundError:
        print("Error: 'inventory.txt' file not found.")
        return

    while True:
        print("1. View Inventory")
        print("2. Update Ingredient Cost")
        print("3. Add New Ingredient")
        print("4. Remove Ingredient")
        print("5. Back to Baker's Menu")

        try:
            choice = int(input("Please enter your selection (1-5): "))
            if choice == 1:
                display_inventory(inventory_items)
            elif choice == 2:
                inventory_items = update_ingredient_cost(inventory_items)
            elif choice == 3:
                inventory_items = add_new_ingredient(inventory_items)
            elif choice == 4:
                inventory_items = remove_ingredient(inventory_items)
            elif choice == 5:
                save_inventory(inventory_items)
                print("Returning to Baker's Menu...")
                baker_menu()
            else:
                print("Please enter a valid option between 1 to 5.")
        except ValueError:
            print("Invalid Input. Error occurs, Please enter NUMBER ONLY between 1 and 5.")

def save_inventory(inventory_items):
    try:
        with open("inventory.txt", "w", newline="") as file:
            file.write("Ingredients,Cost (RM)\n")
            for item in inventory_items:
                file.write(f"{item[0]},{item[1]}\n")
        print("Inventory updated successfully.")
    except:
        print("Error occurred while updating the inventory file.")

def display_inventory(inventory_items):
    print("----------Current Inventory----------")
    print("Ingredients, Cost (RM)")
    total_cost = 0
    for item in inventory_items:
        print(f"{item[0]}, {item[1]}")
        total_cost += float(item[1])
    print(f"\nTotal Inventory Cost: RM{total_cost:.2f}")

def update_ingredient_cost(inventory_items):
    print("----------Update Ingredient Cost----------")
    display_inventory(inventory_items)
    ingredient_name = input("Enter the ingredient name to update: ")
    for item in inventory_items:
        if item[0].lower() == ingredient_name.lower():
            print(f"Current cost for {item[0]}: RM{item[1]}")
            new_cost = input(f"Enter new cost (current: RM{item[1]}): ") or item[1]
            item[1] = new_cost
            print(f"Updated: {item[0]}, Cost: RM{item[1]}")
            save_inventory(inventory_items)
            return inventory_items
    print("Ingredient not found.")
    return inventory_items

def add_new_ingredient(inventory_items):
    print("----------Add New Ingredient----------")
    ingredient = input("Enter the ingredient name: ")
    cost = input("Enter the cost (RM): ")
    new_item = [ingredient, cost]
    print(f"New ingredient: {ingredient}, Cost: RM{cost}")
    confirm = input("Confirm to add this ingredient? (y/n): ")
    if confirm.lower() == "y":
        inventory_items.append(new_item)
        print("Ingredient added successfully.")
        save_inventory(inventory_items)
    else:
        print("Ingredient addition cancelled.")
    return inventory_items

def remove_ingredient(inventory_items):
    print("----------Remove Ingredient----------")
    display_inventory(inventory_items)
    ingredient_name = input("Enter the ingredient name to remove: ")
    for i in range(len(inventory_items)):
        if inventory_items[i][0].lower() == ingredient_name.lower():
            item = inventory_items[i]
            print(f"Removing {item[0]} - Cost: RM{item[1]}")
            confirm = input("Confirm the removal? (y/n): ")
            if confirm.lower() == "y":
                new_inventory = []
                for j in range(len(inventory_items)):
                    if j != i:
                        new_inventory.append(inventory_items[j])
                inventory_items = new_inventory
                print("Ingredient removed successfully.")
                save_inventory(inventory_items)
            else:
                print("Removal cancelled.")
            return inventory_items
    print("Ingredient not found.")
    return inventory_items

# Used inside get_valid_date function
def validate_date(date_input):
    try:
        year, month, day = date_input.split('-')
        year = int(year)
        month = int(month)
        day = int(day)
        if year < 1000 or year > 9999:
            return False
        if month < 1 or month > 12:
            return False
        if day < 1 or day > 31:
            return False
        if month in [4, 6, 9, 11] and day > 30:
            return False
        if month == 2:
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                if day > 29:
                    return False
            elif day > 28:
                return False
        return True
    except ValueError:
        return False

def get_valid_date(prompt):
    while True:
        date = input(prompt)
        if validate_date(date):
            return date
        else:
            print("Invalid date format. Please use YYYY-MM-DD.")

def record_production():
    print("----------Record Production Details----------")
    try:
        date = get_valid_date("Enter the production date (YYYY-MM-DD): ")
        item = input("Enter the item produced: ")
        quantity = int(input("Enter the quantity produced: "))
    except ValueError:
        print("InputType Error:Please input integer on quantity,reprompting again...")
        return record_production()
    
    production_details = f"{date},{item},{quantity}"
    
    # record a log for production added
    try:
        with open("production_log.txt", "a") as file:
            file.write(production_details + "\n")
        print("Production details recorded successfully.")
        
        menu_items = []
        with open("menu.csv", "r") as file:
            menu_items = [line.strip().split(",") for line in file]
        
    # update the stock amount in menu.csv
        for menu_item in menu_items[1:]:
            if menu_item[1].lower() == item.lower():
                current_stock = int(menu_item[4])
                new_stock = current_stock + int(quantity)
                menu_item[4] = str(new_stock)
                
                with open("menu.csv", "w", newline="") as file:
                    for item in menu_items:
                        file.write(",".join(item) + "\n")
                print(f"Stock amount for {item} updated in menu.csv")
                baker_menu()
        else:
            print(f"Warning: {item} not found in menu.csv. Stock not updated.")
    except:
        print("Error occurred while recording production or updating stock.")

def report_equipment():
    print("----------Report Equipment Issues----------")
    equipment_name = input("Enter the name of the equipment: ")
    issue_description = input("Describe the issue: ")
    date_reported = input("Enter the date of the report (YYYY-MM-DD): ")
    maintenance_cost = input("Enter the estimated cost of maintenance/repair (RM): ")
    
    equipment_issue = f"{date_reported},{equipment_name},{issue_description},{maintenance_cost}"
    
    try:
        try:
            with open("equipment_issues.txt", "r") as file:
                if file.readline().strip() != "Date,Equipment,Issue,Maintenance Cost (RM)":
                    raise FileNotFoundError  # IF no file, then create a file haha
        except FileNotFoundError:
            with open("equipment_issues.txt", "w") as file:
                file.write("Date,Equipment,Issue,Maintenance Cost (RM)\n")
        
        # Add issue
        with open("equipment_issues.txt", "a") as file:
            file.write(equipment_issue + "\n")
        print("Equipment issue reported successfully.")
        baker_menu()
    except:
        print("Error occurred while reporting equipment issue.")

if __name__ == "__main__":
    baker_menu()
