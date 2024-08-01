# import required libraries
import datetime

# define bill format and layout
header = "Vaishali Dairy Farm\n\nInvoice Date: {}\nInvoice Number: {}\n\n"
columns = ["Product", "Quantity", "Price", "Total"]
row_format = "{:<20}" + "{:<10}" + "{:<10}" + "{:<10}\n"

# collect customer and product data
customer_name = input("Customer Name: ")
customer_address = input("Customer Address: ")
product_name = input("Product Name: ")
quantity = float(input("Quantity: "))
price = float(input("Price per unit: "))

# calculate total amount due
total = quantity * price

# generate bill
invoice_number = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
bill = header.format(datetime.datetime.now().strftime("%Y-%m-%d"), invoice_number)
bill += "Customer Name: {}\nCustomer Address: {}\n\n".format(customer_name, customer_address)
bill += row_format.format(columns[0], columns[1], columns[2], columns[3])
bill += row_format.format(product_name, quantity, price, total)
bill += "\nTotal Amount Due: {}".format(total)

# print bill
print(bill)
