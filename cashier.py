
import pandas as pd 
import csv

def load_products(menu_path):
    df = pd.read_csv(menu_path)
    
    return df.set_index('ProductName').to_dict(orient='index')

def update_csv(menu_path, products):
    df = pd.DataFrame.from_dict(products, orient='index')
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'ProductName'}, inplace=True)
    df.to_csv(menu_path, index=False)

def add_product(menu_path, products, name, price, quantity):
    if name in products:
        print(f"Product {name} already exists. Update the price instead.")
    else:
        products[name] = {'price': price, 'stocksAmount': quantity}
        update_csv(menu_path, products)
        print(f"Product added: {name} - RM{price:.2f} with quantity {quantity}")
    return products

def delete_product(menu_path, products, name):
    if name in products:
        del products[name]
        update_csv(menu_path, products)
        print(f"Product deleted: {name}")
    else:
        print(f"Product {name} not found.")
    return products

def update_product(menu_path, products, name, new_price, new_quantity):
    if name in products:
        products[name]['price'] = new_price
        products[name]['stocksAmount'] = new_quantity
        update_csv(menu_path, products)
        print(f"Product updated: {name} - RM{new_price:.2f} with quantity {new_quantity}")
    else:
        print(f"Product {name} not found.")
    return products

def add_discount(discounts, description, discount_percent):
    discounts[description] = discount_percent
    print(f"Discount added: {description} - {discount_percent}%")
    return discounts

def delete_discount(discounts, description):
    if description in discounts:
        del discounts[description]
        print(f"Discount deleted: {description}")
    else:
        print(f"Discount {description} not found")
    return discounts

def apply_discount(products, discounts, product_name, discount_description):
    if product_name in products and discount_description in discounts:
        discount_amount = products[product_name]['price'] * (discounts[discount_description] / 100)
        discount_price = products[product_name]['price'] - discount_amount
        print(f"Applied {discounts[discount_description]}% discount on {product_name}. New price: RM{discount_price:.2f}")
        return discount_price
    else:
        print("Product or discount not found")
        return None

def gen_recp(menu_path, products, sales, purchased_items):
    total = 0
    receipt_lines = ["\n--- Receipt ---\n"]
    for item, quantity in purchased_items.items():
        if item in products:
            if products[item]['stocksAmount'] >= quantity:
                line_total = products[item]['price'] * quantity
                receipt_lines.append(f"{item} x{quantity} - RM{line_total:.2f}\n")
                total += line_total
                products[item]['stocksAmount'] -= quantity 
            else:
                print(f"Not enough {item} in stock. Available: {products[item]['stocksAmount']}")
    receipt_lines.append(f"Total: RM{total:.2f}\n")

    for line in receipt_lines:
        print(line, end=" ")

    sales.append({'total': total, 'items': purchased_items})
    update_csv(menu_path, products) 
    return total, sales

def gen_sales_rep(sales):
    total_sales = sum(sale['total'] for sale in sales)
    print(f"\nTotal Sales: RM{total_sales:.2f}")
    print(f"Number of Transactions: {len(sales)}")

def gen_popu_rep(products, sales):
    product_popularity = {product: 0 for product in products}

    for sale in sales:
        for item, count in sale['items'].items():
            if item in product_popularity:
                product_popularity[item] += count

    print("\nProduct Popularity Report:")
    for product, count in product_popularity.items():
        print(f"{product}: {count} items sold")

def cashier_page(menu_path):
    products = load_products(menu_path)
    discounts = {}
    sales = []

    while True:
        print("\n--- Bakery Management System ---")
        print("1. Add Product")
        print("2. Delete Product")
        print("3. Update Product")
        print("4. Generate Receipt")
        print("5. Exit")

        choice = input("Choose an option (1-5): ")

        if choice == '1':
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            quantity = int(input("Enter product quantity: "))
            products = add_product(menu_path, products, name, price, quantity)
        elif choice == '2':
            name = input("Enter product name to delete: ")
            products = delete_product(menu_path, products, name)
        elif choice == '3':
            name = input("Enter product name to update: ")
            new_price = float(input("Enter new price: "))
            new_quantity = int(input("Enter new quantity: "))
            products = update_product(menu_path, products, name, new_price, new_quantity)
        elif choice == '4':
            purchased_items = {}
            print("Enter purchased items (type 'done' to finish):")
            while True:
                item = input("Item name: ")
                if item.lower() == 'done':
                    break
                quantity = int(input(f"Quantity of {item}: "))
                purchased_items[item] = quantity
            _, sales = gen_recp(menu_path, products, sales, purchased_items)
        elif choice == '5':
            print("Exiting Bakery Management System: Cashier.")
            break
        else:
            print("Invalid choice. Please try again.")

menu_path = 'C:\\Users\\ameli\\Downloads\\menu (1).csv'

cashier_page(menu_path)
