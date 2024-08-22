products = {}
discounts = {}
sales = []

    
def add_product(name, price):
        products[name] = price
        print(f"Product added: {name} - ${price:.2f}")

def delete_product(name):
    if name in products:
        del products[name]
        print(f"Product deleted: {name}")
    else:
        print(f"Product {name} not found")

def add_discount(des, dict_per):
        discounts[des] = dict_per
        print(f"Discount added: {des} - {dict_per}%")

def delete_discount(des):
    if des in discounts:
        del discounts[des]
        print(f"Discount deleted: {des}")
    else:
        print(f"Discount {des} not found")

def apply_discount(pro_name, dict_des):
    if pro_name in products and dict_des in discounts:
        dict_amt = products[pro_name] * (discounts[dict_des]/100)
        dict_price = products[pro_name] - dict_amt
        print(f"Applied {discounts[dict_des]}% discount on {pro_name}. New price: ${dict_price:.2f}")
        return dict_price
    
    else:
        print("Product or discount not found")
        return None
        
def gen_recp(purc_item):
    total = 0 
    print("\n--- Receipt ---\n")
    for item, quantity in purc_item.items():
        if item in products:
            line_total = products[item] * quantity
            print(f"{item} x{quantity} - ${line_total:.2f}")
            total += line_total
    print(f"Total: ${total:.2f}")
    sales.append({'total':total, 'items': purc_item})
    return total
            
def gen_sales_rep():
    total_sales = sum(sale['total'] for sale in sales)
    print(f"\nTotal Sales: ${total_sales:2f}")
    print(f"Number of Transactions: {len(sales)}")

def gen_popu_rep():
    product_popu = {product.name: 0 for product in products}

    for sale in sales:
        for item , count in sale ['items'].items():
            product_popu[item] += count

    print("\nProduct Popularity Report:")
    for product, count in product_popu:
        print(f"{product}: {count} items sold")

