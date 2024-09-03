import pandas as pd

# Home
def home():
    print("--------Baker--------")
    print("1.Menu")
    print("2.Recipe")
    print("3.Inventory")
    print("4.Product Record")
    print("5.Equipment")
    print("6.Exit")
    while True:
        try:
            option = int(input("Please enter your selection (1-5): "))
            if option in [1, 2, 3, 4, 5]:
                break
            else:
                print("Please enter a valid option between 1 to 5.")
        except ValueError:
            print("Invalid Input. Error occurs, Please enter NUMBER ONLY between 1 to 5")

    if option == 1:
        menu()
    elif option == 2:
        recipe()
    elif option == 3:
        inventory()
    elif option == 4:
        product_record()
    elif option == 5:
        equipment()
    elif option == 6:
        exit()    

# MENU
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
        menuTable = pd.read_csv("menu.csv")
        print(menuTable)


    elif choice == 2:
        view = open('menu.txt','r')
        print(view.read())
        
    elif choice == 3:
        view = open('menu.txt','r')
        print(view.read())
        print("Which product you want to update?")
        update_input = input("Enter the number of the product only (EXP: '1.tiramisu cake', enter 1):\n")
        update = open('menu.txt','w')
        update.write(update_input)

    elif choice == 4:
        pass
    elif choice == 5:
        home()




#recipe, CRUD by Baker
def recipe():
    print("------Avengers' Bakery Recipe------")
    print("1.Add new recipe")
    print("View recipe")
    print("2.Update")
    print("3.Delete")
    print("4.Return to Home")

    input=("Choose which to operate(1-4):")



#inventory
def inventory():
    print("------Avengers' Bakery Inventory------")
    print("1.Add on new inventory")
    print("2.Update")
    print("3.Check")
    print("4.Delete inventory")
    print("5.Return to Home")

    input=("Choose which to operate(1-5):")

    list=["fruit", "flour", "egg", "sugar", "vanilla extract"]
    print(list)
    option=input("Which inventory you want to check? : ")
    fruit= "fruit"
    flour= "flour"
    egg= "egg"
    sugar= "sugar"
    vanilla= "vanilla extract"


    def fruitamt() :
        while fruit<10:
            print("Warning! Need to purchase new stock!")
            print("Your stock remaining :" + fruit)
        else:
            print("Still got stock no worries")
            print("Your stock remaining :" + fruit)

    def flouramt():
        while flour<2:
            print("Warning! Need to purchase new stock!")
            print("Your stock remaining :" + flour)
        else:
            print("Still got stock no worries")
            print("Your stock remaining :" + flour)

    def eggamt():
        while egg<20:
            print("Warning! Need to purchase new stock!")
            print("Your stock remaining :" + egg)
        else:
            print("Still got stock no worries")
            print("Your stock remaining :" + egg)

    def sugaramt():
        while sugar<2:
            print("Warning! Need to purchase new stock!")
            print("Your stock remaining :" + sugar)
        else:
            print("Still got stock no worries")
            print("Your stock remaining :" + sugar)

    def vanillaamt():
        while vanilla<1:
            print("Warning! Need to purchase new stock!")
            print("Your stock remaining :" + vanilla)
        else:
            print("Still got stock no worries")
            print("Your stock remaining :" + vanilla)

    if option==fruit:
        fruitamt()

    if option==flour:
        flouramt()

    if option==egg:
        eggamt()

    if option==sugar:
        sugaramt()

    if option==vanilla:
        vanillaamt()



#equipment
def equipment():
    print("------Avengers' Bakery Equipment------")
    print("1.New Equipment")
    print("2.Check")
    print("3.Update")
    print("4.Delete")
    print("5.Return to Home")

    input=("Choose which to operate(1-5):")

    list=["oven", "fridge", "stand mixer"]
    print(list)
    option=input("Which one you want to choose? :")

    oven="oven"
    fridge="frigde"
    stand_mixer="stand mixer"



    if option==oven :
        print("You want to check\n1.Maintainence period\n\t or \n2.Last mantainence date?")


    if option==fridge :
        print("You want to check\n1.Maintainence period\n\t or \n2.Last mantainence date?")

    if option==stand_mixer :
        print("You want to check\n1.Maintainence period\n\t or \n2.Last mantainence date?")



#start
home()
