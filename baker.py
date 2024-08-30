
# menu
# need to access by customer, while baker(me) can update, create, delete and etc.


#home
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
    else:
        pass

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




#recipe, CRUD by Baker
def recipe():
    print("------Avengers' Bakery Recipe------")
    print("1.Create")
    print("2.Update")
    print("3.Delete")
    print("4.Return to Home")

    input=("Choose which to operate(1-4):")



#inventory
def inventory():
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


#Product Record
def productrecord():
    list=['cake', 'bread', 'snacks']
    print(list)
    option=input("Which one you want to choose? :")

    cake="cake"
    bread="bread"
    snacks="snacks"

    if option==cake :
        print("You want to update\n1.Batch Number & Quantities\n\t or \n2.Expiration date?")

    if option==bread :
        print("You want to update\n1.Batch Number & Quantities\n\t or \n2.Expiration date?")

    if option==snacks :
        print("You want to update\n1.Batch Number & Quantities\n\t or \n2.Expiration date?")


#equipment
def equipment():
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
