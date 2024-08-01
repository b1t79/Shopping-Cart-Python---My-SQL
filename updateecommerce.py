import mysql.connector
import datetime

mydb = mysql.connector.connect(
 host="localhost",
 user="root",
 password="t15ha",
 database="ecommerce"
)
mycursor = mydb.cursor()
now = datetime.datetime.now()


def add_product():
 try:  
    product_id = input("Enter product id: ")
    brand = input("Enter the Product Brand Name: ")
    Pname = input("Enter the Product Name: ")
    Rate = int(input("Enter the Rate for Product: "))
    
    product = (product_id, Pname, brand, Rate)
    sql = "INSERT INTO product (product_id, Pname, brand, Rate) VALUES (%s, %s, %s,%s)"
    mycursor.execute(sql, product)
    mydb.commit()
    
    stk = (product_id, 0, "No")
    sql = "INSERT INTO stock (item_id, Instock, status) VALUES (%s, %s, %s)"
    mycursor.execute(sql, stk)
    mydb.commit()
    
    print("One Product inserted")
 except Exception as e:
    print("Error:", e)

def update_product():
 try:
    product_id = input("Enter id to update: ")
    sql = "SELECT * FROM stock WHERE product_id = %s"
    ed = (product_id,)
    mycursor.execute(sql, ed)
    res = mycursor.fetchall()
    for x in res:
        print(x)
        print("")
        fld = input("Enter the field which you want to edit: ")
        val = input("Enter the value you want to set: ")
        sql = "UPDATE stock SET " + fld + " = %s WHERE product_id = %s"
        sq = (val, product_id)
        mycursor.execute(sql, sq)
 except Exception as e:  
    print("Error:", e)
    print("One Product inserted")
 finally:
    mydb.commit()

def DelProduct():
    product_id = input("Enter the Product ID to be deleted: ")
    sql = "DELETE FROM sales WHERE item_id = %s"
    id = (product_id,)
    mycursor.execute(sql, id)
    mydb.commit()
    sql = "DELETE FROM purchase WHERE item_id = %s"
    mycursor.execute(sql, id)
    mydb.commit()
    sql = "DELETE FROM stock WHERE item_id = %s"
    mycursor.execute(sql, id)
    mydb.commit()
    sql = "DELETE FROM product WHERE product_id = %s"
    mycursor.execute(sql, id)
    mydb.commit()
    print("One Item Deleted")


def ViewProduct():
    print("Display Menu: Select the category to display the data")
    print("1. All Details")
    print("2. Product Name:")
    print("3. Product Brand:")
    print("4. Product ID:")
    x = 0
    ch = int(input("Enter your choice to display: "))
    if ch == 1:
        sql = "SELECT * FROM product"
        mycursor.execute(sql)
        res = mycursor.fetchall()
        for x in res:
            print(x)
        x = 1
    elif ch == 2:
        var = 'PName'
        val = input("Enter the name of Product: ")
    elif ch == 3:
        var = 'brand'
        val = input("Enter the name of Brand: ")
    elif ch == 4:
        var = 'product_id'
        val = input("Enter the Product_id: ")
    if x == 0:
        sql = "SELECT * FROM product WHERE " + var + " = %s"
        sq = (val,)
        mycursor.execute(sql, sq)
        res = mycursor.fetchall()
        for x in res:
            print(x)


def PurchaseProduct():
    mn = ""
    dy = ""
    now = datetime.datetime.now()
    purchaseID = "P" + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second)
    L = []
    Lst = []
    L.append(purchaseID)
    itemId = input("Enter Product ID: ")
    L.append(itemId)
    itemNo = int(input("Enter the number of Items: "))
    L.append(itemNo)
    sql = "SELECT rate FROM product WHERE product_id = %s"
    pid = (itemId,)
    mycursor.execute(sql, pid)
    res = mycursor.fetchone()
    for x in res:
        print("rate is:", x)
    amount = x * itemNo
    print("Amount is:", amount)
    L.append(amount)
    mnth = now.month
    if mnth <= 9:
        mn = "0" + str(mnth)
    else:
        mn = str(mnth)
    day = now.day
    if day <= 9:
        dy = "0" + str(day)
    else:
        dy = str(day)

    dt = str(now.year) + "-" + mn + "-" + dy
    L.append(dt)
    tp = tuple(L)
    sql = "INSERT INTO purchase (purchase_id, item_id, no_of_items, amount, Purchase_date) VALUES (%s, %s, %s, %s, %s)"
    mycursor.execute(sql, tp)
    mydb.commit()
    sql = "SELECT Instock FROM stock WHERE item_id = %s"
    mycursor.execute(sql, pid)
    res = mycursor.fetchall()
    status = "No"
    for x in res:
        print(x)
    instock = x[0] + itemNo
    if instock > 0:
        status = "Yes"
    Lst.append(instock)
    Lst.append(status)
    Lst.append(itemId)
    tp = tuple(Lst)
    sql = "UPDATE stock SET instock = %s, status = %s WHERE item_id = %s"
    mycursor.execute(sql, tp)
    mydb.commit()
    print("1 Item purchased and saved in Database")


def ViewUserPurchases():
    sql = "SELECT pr.Pname, pr.brand, p.no_of_items, p.amount, p.Purchase_date " \
          "FROM purchase p " \
          "JOIN product pr ON pr.product_id = p.item_id " \
          "WHERE Pname = %s"
    mycursor.execute(sql, Pname)
    purchases = mycursor.fetchall()
    for purchase in purchases:
        print(purchase)



def ViewStock():
    item = input("Enter Product Name: ")
    sql = "SELECT product.product_id, product.Pname, stock.Instock, \
           stock.status FROM stock, product WHERE \
           product.product_id = stock.item_id AND product.PName = %s"
    itm = (item,)
    mycursor.execute(sql, itm)
    res = mycursor.fetchall()
    for x in res:
        print(x)


def SellProduct():
    item_id = input("Enter the Product ID: ")
    quantity = int(input("Enter the quantity sold: "))
    
    # Check if enough stock is available
    sql = "SELECT Instock FROM stock WHERE item_id = %s"
    mycursor.execute(sql, (item_id,))
    instock = mycursor.fetchone()
    
    if instock and instock[0] >= quantity:
        # Update stock
        new_stock = instock[0] - quantity
        update_stock_sql = "UPDATE stock SET Instock = %s WHERE item_id = %s"
        mycursor.execute(update_stock_sql, (new_stock, item_id))
        
        # Record the sale
        sale_id = f"S{now.year}{now.month:02d}{now.day:02d}{now.hour:02d}{now.minute:02d}{now.second:02d}"
        sql = "INSERT INTO sales (sale_id, item_id, no_of_items_sold, sale_date) VALUES (%s, %s, %s, %s)"
        mycursor.execute(sql, (sale_id, item_id, quantity, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
        # Commit the transaction
        mydb.commit()
        
        print("Sale recorded successfully.")
    else:
        print("Not enough stock available to sell.")


def ViewAllSales():
    sql = "SELECT pr.Pname, pr.brand, s.no_of_items_sold, s.sale_date " \
          "FROM sales s " \
          "JOIN product pr ON pr.product_id = s.item_id"
    mycursor.execute(sql)
    all_sales = mycursor.fetchall()
    for sale in all_sales:
        print(sale)



def MenuSet():
    print("Enter 1: To Add Product")
    print("Enter 2: To Edit Product")
    print("Enter 3: To Delete Product")
    print("Enter 4: To View Product")
    print("Enter 5: To Purchase Product")
    print("Enter 6: To View Purchases")
    print("Enter 7: To View Stock Details")
    print("Enter 8: To Sell Product")
    print("Enter 9: To View Sales")
    print("Enter 0: To Exit")
    return int(input("Enter your choice: "))

# Existing code

def MainMenu():
    choice = MenuSet()
    while choice != 0:
        if choice == 1:
            add_product()
        elif choice == 2:
            update_product()
        elif choice == 3:
            DelProduct()
        elif choice == 4:
            ViewProduct()
        elif choice == 5:
            PurchaseProduct()
        elif choice == 6:
            ViewUserPurchases()
        elif choice == 7:
            ViewStock()
        elif choice == 8:
            SellProduct()
        elif choice == 9:
            ViewAllSales()
        choice = MenuSet()

# Add the call to MainMenu() to initiate the menu-driven functionality
MainMenu()