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
                # Call manage_recipes() function
                pass
            elif choice == 3:
                # Call verify_ingredients() function
                pass
            elif choice == 4:
                # Call record_production() function
                pass
            elif choice == 5:
                # Call report_equipment() function
                pass
            elif choice == 6:
                print("Exiting Baker's Menu...")
                return
            else:
                print("Please enter a valid option between 1 to 6.")
        except ValueError:
            print("Invalid Input. Error occurs, Please enter NUMBER ONLY between 1 and 6.")

# Store Menu
def store_menu():
    print("----------Store Menu----------")
    try:
        with open("menu.txt", "r") as file:
            menu_items = [line.strip().split(",") for line in file]
    except FileNotFoundError:
        print("Error: 'your_file.txt' file not found.")
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
        with open("menu.txt", "w", newline="") as file:
            for item in menu_items:
                file.write(",".join(item) + "\n")
    except:
        print("Error occurred while updating the menu file.")

def display_menu(menu_items):
    print("----------Current Menu----------")
    for item in menu_items:
        print(f"Item: {item[0]}, Price: {item[1]}")

def create_menu_item(menu_items):
    print("----------Create New Menu Item----------")
    item_name = input("Enter the item name: ")
    item_price = input("Enter the item price: ")
    print(f"New item: {item_name}, Price: {item_price}")
    confirm = input("Confirm to add this item? (y/n): ")
    if confirm.lower() == "y":
        menu_items.append([item_name, item_price])
        print("Item added successfully.")
        save_menu(menu_items)
    else:
        print("Item creation cancelled.")
    return menu_items

def update_menu_item(menu_items):
    print("----------Update Existing Menu Item----------")
    display_menu(menu_items)
    item_name = input("Enter the item name to update: ")
    for item in menu_items:
        if item[0] == item_name:
            new_price = input(f"Enter the new price for {item[0]} (current: {item[1]}): ")
            print(f"Updating {item[0]} - Price: {item[1]} -> {new_price}")
            confirm = input("Confirm the update? (y/n): ")
            if confirm.lower() == "y":
                item[1] = new_price
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
    item_name = input("Enter the item name to remove: ")
    for item in menu_items:
        if item[0] == item_name:
            print(f"Removing {item[0]} - Price: {item[1]}")
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
            recipes = [line.strip().split(",") for line in file]
    except FileNotFoundError:
        print("Error: 'recipes.txt' file not found.")
        return

    while True:
        print("1. View Recipes")
        print("2. Create New Recipe")
        print("3. Update Existing Recipe")
        print("4. Remove Recipe")
        print("5. Back to Baker's Menu")

        try:
            choice = int(input("Please enter your selection (1-5): "))
            if choice == 1:
                display_recipes(recipes)
            elif choice == 2:
                recipes = create_recipe(recipes)
            elif choice == 3:
                recipes = update_recipe(recipes)
            elif choice == 4:
                recipes = remove_recipe(recipes)
            elif choice == 5:
                print("Returning to Baker's Menu...")
                return
            else:
                print("Please enter a valid option between 1 to 5.")
        except ValueError:
            print("Invalid Input. Error occurs, Please enter NUMBER ONLY between 1 and 5.")

def display_recipes(recipes):
    print("----------Current Recipes----------")
    for recipe in recipes:
        print(f"Name: {recipe[0]}, Ingredients: {recipe[1]}, Instructions: {recipe[2]}")

def create_recipe(recipes):
    print("----------Create New Recipe----------")
    recipe_name = input("Enter the recipe name: ")
    recipe_ingredients = input("Enter the recipe ingredients (comma-separated): ")
    recipe_instructions = input("Enter the recipe instructions: ")
    print(f"New recipe: {recipe_name}, Ingredients: {recipe_ingredients}, Instructions: {recipe_instructions}")
    confirm = input("Confirm to add this recipe? (y/n): ")
    if confirm.lower() == "y":
        recipes.append([recipe_name, recipe_ingredients, recipe_instructions])
        print("Recipe added successfully.")
        save_recipes(recipes)
    else:
        print("Recipe creation cancelled.")
    return recipes

def update_recipe(recipes):
    print("----------Update Existing Recipe----------")
    display_recipes(recipes)
    recipe_name = input("Enter the recipe name to update: ")
    for recipe in recipes:
        if recipe[0] == recipe_name:
            new_ingredients = input(f"Enter the new ingredients for {recipe[0]} (current: {recipe[1]}): ")
            new_instructions = input(f"Enter the new instructions for {recipe[0]} (current: {recipe[2]}): ")
            print(f"Updating {recipe[0]} - Ingredients: {recipe[1]} -> {new_ingredients}, Instructions: {recipe[2]} -> {new_instructions}")
            confirm = input("Confirm the update? (y/n): ")
            if confirm.lower() == "y":
                recipe[1] = new_ingredients
                recipe[2] = new_instructions
                print("Recipe updated successfully.")
                save_recipes(recipes)
            else:
                print("Update cancelled.")
            return recipes
    print("Recipe not found.")
    return recipes

def remove_recipe(recipes):
    print("----------Remove Recipe----------")
    display_recipes(recipes)
    recipe_name = input("Enter the recipe name to remove: ")
    for recipe in recipes:
        if recipe[0] == recipe_name:
            print(f"Removing {recipe[0]}")
            confirm = input("Confirm the removal? (y/n): ")
            if confirm.lower() == "y":
                recipes.remove(recipe)
                print("Recipe removed successfully.")
                save_recipes(recipes)
            else:
                print("Removal cancelled.")
            return recipes
    print("Recipe not found.")
    return recipes

def save_recipes(recipes):
    try:
        with open("recipes.txt", "w", newline="") as file:
            for recipe in recipes:
                file.write(",".join(recipe) + "\n")
    except:
        print("Error occurred while updating the recipes file.")

def verify_ingredients():
    print("----------Verify Ingredient Inventory----------")
    # Code to verify ingredient inventory
    pass

def record_production():
    print("----------Record Production Details----------")
    # Code to record production details
    pass

def report_equipment():
    print("----------Report Equipment Issues----------")
    # Code to report equipment issues
    pass
