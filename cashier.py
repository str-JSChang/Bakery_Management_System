products = {}
discounts = {}
sales = []

def add_product(name, price):
    products[name] = price
    print(f"Product added: {name} - ${price:.2f}")

def delete_product(name):
    if name in products:
        del products[name]
        save_bakery_items(products)
        print(f"Product deleted: {name}")
    else:
        print(f"Product {name} not found.")

def add_discount(des, disc_per):
    discounts[des] = disc_per
    print(f"Discount added: {des} - {disc_per}%")

def delete_discount(des):
    if des in discounts:
        del discounts[des]
        print(f"Discount deleted: {des}")
    else:
        print(f"Discount {des} not found")

def apply_discount(pro_name, disc_des):
    if pro_name in products and disc_des in discounts:
        disc_amt = products[pro_name] * (discounts[disc_des] / 100)
        disc_price = products[pro_name] - disc_amt
        print(f"Applied {discounts[disc_des]}% discount on {pro_name}. New price: ${disc_price:.2f}")
        return disc_price
    else:
        print("Product or discount not found")
        return None
        
def load_bakery_items(filename="inventory.txt"):
    products = {}
    with open(filename, "r") as file:
        for line in file:
            name, price = line.strip().split(", ")
            products[name] = float(price)
    return products

def save_bakery_items(products, filename="inventory.txt"):
    with open(filename, "w") as file:
        for name, price in products.items():
            file.write(f"{name}, {price:.2f}\n")

def gen_recp(purc_item, recp_file="cus_report.txt"):
    total = 0 
    recp_line = ["\n--- Receipt ---\n"]
    for item, quantity in purc_item.items():
        if item in products:
            line_total = products[item] * quantity
            recp_line.append(f"{item} x{quantity} - ${line_total:.2f}\n")
            total += line_total
    recp_line.append(f"Total: ${total:.2f}\n")
    
    with open(recp_file, "a") as file:
        file.writelines(recp_line)
    
    sales.append({'total': total, 'items': purc_item})  # Update sales list
    print(f"Receipt saved to {recp_file}")
    return total

def gen_sales_rep():
    total_sales = sum(sale['total'] for sale in sales)
    print(f"\nTotal Sales: ${total_sales:.2f}")
    print(f"Number of Transactions: {len(sales)}")

def gen_popu_rep():
    product_popu = {product: 0 for product in products}  # Initialize correctly

    for sale in sales:
        for item, count in sale['items'].items():
            product_popu[item] += count

    print("\nProduct Popularity Report:")
    for product, count in product_popu.items():  # Use .items() for correct tuple unpacking
        print(f"{product}: {count} items sold")

def cashier_page():
    load_bakery_items()  # Load products from the file into the global dictionary
    
    while True:
        print("\n--- Bakery Management System ---")
        print("1. Add Product")
        print("2. Delete Product")
        print("3. Generate Receipt")
        print("4. Exit")

        choice = input("Choose an option (1-4): ")

        if choice == '1':
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            add_product(name, price)
            save_bakery_items(products)  # Save the updated products to file
        elif choice == '2':
            name = input("Enter product name to delete: ")
            delete_product(name)
        elif choice == '3':
            purchased_items = {}
            print("Enter purchased items (type 'done' to finish):")
            while True:
                item = input("Item name: ")
                if item.lower() == 'done':
                    break
                quantity = int(input(f"Quantity of {item}: "))
                purchased_items[item] = quantity
            gen_recp(purchased_items)
        elif choice == '4':
            print("Exiting Bakery Management System: Cashier.")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the bakery management system
cashier_page()
