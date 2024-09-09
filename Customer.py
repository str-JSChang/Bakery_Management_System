#Customer acc management - create(password verify 2), manage, login, update
#Product browsing
#Cart management - add, remove, mod items
#Order Tracking - status of orders
#Product Review - feedback, suggestions
import csv

def update_acc():
    name = "Bowie"
    return name
cus_name = update_acc()

def cart():
    def menu():
        #store csv menu in a list and display in table
        menu = []
        with open('menu.csv', newline='') as csvfile:
            items = csv.reader(csvfile)
            next(items)
            print("No." + "\t" + "Name" + "\t "*3 + "Category" + "\t  " + "Price" + "\t  " + "  Stock")
            print("-"*70)
            for row in items:
                item  = {
                    'number': row[0].strip(),
                    'name': row[1].strip(),
                    'category': row[2].strip(),
                    'price': row[3].strip(),
                    'stock': row[4].strip()
                }
                menu.append(item)
        for item in menu:
            print(item['number'] + " "*(5 -len(item['number'])) +
                  item['name'] + " " * (30 - len(item['name'])) +  # space adjustment for each column
                  item['category'] + " " * (15 - len(item['category'])) +  
                  item['price'] + " " * (12 - len(item['price'])) + 
                  item['stock']
                  )
            print("-" *70)

    def update_cart():
        menu()
        item_num = input("Enter item number to add: ")
        quantity = input("Enter quantity: ")
        with open('menu.csv',newline ='') as menu:
            items = csv.reader(menu)
            next(items)

            for row in items:
                if row[0] == item_num:
                    with open('cart.csv', 'a') as cart:
                        writer = csv.writer(cart)

                        if cart == None:
                            writer.writerow(['No.','Name','Category','Price','Quantity'])
                        writer.writerow([row[0],row[1],row[2],row[3], quantity])
                    print(f"{row[1]} x {quantity} added to cart.")
                    break
            
            # for line in csv:
            #     file.write(line)
            #     file.write('\n')


    while True:
        print("1. View Menu")
        print("2. Shopping Cart")
        print("3. Check Out")
        print("4. Back")

        choice = str(input("Enter your selection: "))
        if choice == "1":
            menu()
            break
        elif choice == "2":
            update_cart()
        elif choice == "3":
            order()
        elif choice == "4":
            main_cus_page(cus_name)


def order():
    pass

def feedback():
    pass


def main_cus_page(cus_name):
    print("-"*50 + "\n\t\t" + f"Welcome, {cus_name}.\n"+ "-"*50)
    print("1. Update Account")
    print("2. Shopping Cart")
    print("3. My Order")
    print("4. Feedback")

    while True:
        choice = str(input("Enter your selection(1-4): "))
        if choice == "1":
            update_acc()
        elif choice == "2":
            cart()
        elif choice == "3":
            order()
        elif choice == "4":
            feedback()
        else:
            print("Invalid selection. Enter number between 1-4.")

main_cus_page(cus_name)
