import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(
 host="localhost",
 user="root",
 password="t15ha",
 database="ecommerce"
)
mycursor = mydb.cursor()
now = datetime.now()


def AddProduct():
    L = []
    stk = []
    pid = input("Enter the Product ID: ")
    L.append(pid)
    IName = input("Enter the Product Name: ")
    L.append(IName)
    brnd = input("Enter the Product Brand Name: ")
    L.append(brnd)
    rate = int(input("Enter the Price for Product: "))
    L.append(rate)
    product = tuple(L)
    sql = "INSERT INTO product (product_id, PName, brand, rate) VALUES (%s, %s, %s, %s)"
    mycursor.execute(sql, product)
    mydb.commit()
    stk.append(pid)
    stk.append(0)
    stk.append("No")
    st = tuple(stk)
    sql = "INSERT INTO stock (item_id, Instock, status) VALUES (%s, %s, %s)"
    mycursor.execute(sql, st)
    mydb.commit()
    print("One Product inserted")


def EditProduct():
    pid = input("Enter product ID to be edited: ")
    sql = "SELECT * FROM product WHERE product_id = %s"
    ed = (pid,)
    mycursor.execute(sql, ed)
    res = mycursor.fetchall()
    for x in res:
        print(x)
    print("")
    fld = input("Enter the field which you want to edit: ")
    val = input("Enter the value you want to set: ")

    sql = "UPDATE product SET " + fld + " = %s WHERE product_id = %s"
    sq = (val, pid)
    mycursor.execute(sql, sq)
    print("Editing Done:")
    print("After correction, the record is:")
    sql = "SELECT * FROM product WHERE product_id = %s"
    ed = (pid,)
    mycursor.execute(sql, ed)
    res = mycursor.fetchall()
    for x in res:
        print(x)
    mydb.commit()


def DelProduct():
    pid = input("Enter the Product ID to be deleted: ")
    sql = "DELETE FROM sales WHERE item_id = %s"
    id = (pid,)
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


def ViewPurchase():
    item = input("Enter Product Name: ")
    sql = "SELECT product.product_id, product.PName, product.brand, \
           sales.no_of_item_sold, sales.date_of_sale, sales.amount \
           FROM sales, product WHERE product.product_id = sales.item_id \
           AND product.PName = %s"
    itm = (item,)
    mycursor.execute(sql, itm)
    res = mycursor.fetchall()
    for x in res:
        print(x)
def ViewStock():
    item = input("Enter Product Name: ")
    sql = "SELECT product.product_id, product.PName, stock.instock, \
           stock.status FROM stock, product WHERE \
           product.product_id = stock.item_id AND product.PName = %s"
    itm = (item,)
    mycursor.execute(sql, itm)
    res = mycursor.fetchall()
    for x in res:
        print(x)
def SaleProduct():
    now = datetime.datetime.now()
    saleID = "S" + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second)
    L = []
    L.append(saleID)
    itemId = input("Enter Product ID: ")
    L.append(itemId)
    itemNo = int(input("Enter the number of Items: "))
    L.append(itemNo)
    sql = "SELECT rate FROM product WHERE product_id = %s"
    pid = (itemId,)
    mycursor.execute(sql, pid)
    res = mycursor.fetchall()
    for x in res:
        print("The rate of item is:", x)
    dis = int(input("Enter the discount: "))
    saleRate = x[0] - (x[0] * dis / 100)
    L.append(saleRate)
    amount = itemNo * saleRate
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
    sql = "INSERT INTO sales (sale_id, item_id, no_of_item_sold, \
           sale_rate, amount, date_of_sale) VALUES (%s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, tp)
    mydb.commit()
    sql = "SELECT Instock FROM stock WHERE item_id = %s"
    mycursor.execute(sql, pid)
    res = mycursor.fetchall()
    for x in res:
        print("Total Items in Stock are:", x)
    instock = x[0] - itemNo
    if instock > 0:
        status = "Yes"
    tp = (instock, status, itemId)
    sql = "UPDATE stock SET instock = %s, status = %s WHERE item_id = %s"
    print("Remaining Items in Stock are:", instock)
    mycursor.execute(sql, tp)
    mydb.commit()


def ViewSales():
    item = input("Enter Product Name: ")
    sql = "SELECT product.product_id, product.PName, product.brand, \
           sales.no_of_item_sold, sales.date_of_sale, sales.amount \
           FROM sales, product WHERE product.product_id = sales.item_id \
           AND product.PName = %s"
    itm = (item,)
    mycursor.execute(sql, itm)
    res = mycursor.fetchall()
    for x in res:
        print(x)

def CustomerMenu():
    print("Enter 1: To Add Product")
    print("Enter 2: To Edit Product")
    print("Enter 3: To Delete Product")
    print("Enter 4: To View Product")
    print("Enter 5: To Purchase Product")
    print("Enter 6: To View Purchases")
    print("Enter 0: To Exit")
    return int(input("Enter your choice: "))

def EmployeeMenu():
    print("Enter 7: To View Purchases")
    print("Enter 8: To View Stock Details")
    print("Enter 9: To Sell Product")
    print("Enter 10: To View Sales")
    print("Enter 0: To Exit")
    return int(input("Enter your choice: "))

def handleCustomerChoice(choice):
    if choice == 1:
        AddProduct()
    elif choice == 2:
        EditProduct()
    elif choice == 3:
        DelProduct()
    elif choice == 4:
        ViewProduct()
    elif choice == 5:
        PurchaseProduct()
    elif choice == 6:
        ViewPurchase()

def handleEmployeeChoice(choice):
    if choice == 7:
        ViewPurchase()
    elif choice == 8:
        ViewStock()
    elif choice == 9:
        SaleProduct()
    elif choice == 10:
        ViewSales()

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

