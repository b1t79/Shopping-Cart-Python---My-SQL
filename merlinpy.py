import mysql.connector

# Connect to MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="t15ha",
  database="cart"
)

cursor = mydb.cursor()

# Customer operations
def register_customer(name, email):
  sql = "INSERT INTO customers (name, email) VALUES (%s, %s)"
  values = (name, email)
  cursor.execute(sql, values)
  mydb.commit()
  print("Registered new customer:", name)

def view_products():
  sql = "SELECT * FROM products"
  cursor.execute(sql)
  result = cursor.fetchall()
  print("Available products:")
  for product in result:
    print(product)
    
def add_to_cart (customer_id, product_id, quantity):
  sql = "INSERT INTO carts (customer_id, product_id, quantity) VALUES (%s, %s, %s)" 
  values = (customer_id, product_id, quantity)
  cursor.execute(sql, values)
  mydb.commit()
  print("Added product to cart")
  
def remove_from_cart(cart_id):
  sql = "DELETE FROM carts WHERE id=%s"
  values = (cart_id,)  
  cursor.execute(sql, values)
  mydb.commit() 
  print("Removed product from cart")


def purchase_product(customer_id, product_id, quantity):
  sql = "INSERT INTO purchases (customer_id, product_id, quantity) VALUES (%s, %s, %s)"
  values = (customer_id, product_id, quantity)
  cursor.execute(sql, values)
  mydb.commit()

  print("Product purchased successfully")
  
# Employee operations  
def add_product(name, price, stock):
  sql = "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)"
  values = (name, price, stock)
  cursor.execute(sql, values)  
  mydb.commit()
  print("Added new product:", name)

def update_product(product_id, name, price, stock):
  sql = "UPDATE products SET name=%s, price=%s, stock=%s WHERE id=%s"
  values = (name, price, stock, product_id)
  cursor.execute(sql, values)
  mydb.commit()
  print("Updated product:", product_id)

def view_sales():
  sql = "SELECT SUM(total_price) AS total_sales FROM orders" 
  cursor.execute(sql)
  total_sales = cursor.fetchone()[0]
  print("Total sales:", total_sales)


def CustomerMenu():
    print("Enter 1: To Register")
    print("Enter 2: To View Product")
    print("Enter 3: Add Product to Cart")
    print("Enter 4: Remove Product from Cart")
    print("Enter 5: To Purchase Product")
    print("Enter 6: For Employee Portal")
    print("Enter 0: To Exit")
    return int(input("Enter your choice: "))

def EmployeeMenu():
    print("Enter 7: To List Product")
    print("Enter 8: To Update Product")
    print("Enter 9: To View Sales")
    print("Enter 0: To Exit")
  
    return int(input("Enter your choice: "))


def handleCustomerChoice(choice):
    if choice == 1:
        name = input("Enter customer name: ")
        email = input("Enter customer email: ")
        register_customer(name, email)
    elif choice == 2:
        view_products()
    elif choice == 3:
        customer_id = input("Enter customer ID: ")
        product_id = input("Enter product ID: ")
        quantity = input("Enter quantity: ")
        add_to_cart(customer_id, product_id, quantity)
    elif choice == 4:
        cart_id = input("Enter cart ID: ")
        remove_from_cart(cart_id)
    elif choice == 5:
        customer_id = input("Enter customer ID: ")
        product_id = input("Enter product ID: ")
        quantity = input("Enter quantity: ")
        purchase_product(customer_id, product_id, quantity)

def handleEmployeeChoice(choice):
    if choice == 7:
        name = input("Enter product name: ")
        price = input("Enter product price: ")
        stock = input("Enter product stock: ")
        add_product(name, price, stock)
    elif choice == 8:
        product_id = input("Enter product ID: ")
        name = input("Enter product name: ")
        price = input("Enter product price: ")
        stock = input("Enter product stock: ")
        update_product(product_id, name, price, stock)
    elif choice == 9:
        view_sales()

def MainMenu():
    while True:
        customer_choice = CustomerMenu()
        if customer_choice == 0:
            break
        handleCustomerChoice(customer_choice)

        employee_choice = EmployeeMenu()
        if employee_choice == 0:
            break
        handleEmployeeChoice(employee_choice)

if __name__ == "__main__":
    MainMenu()
