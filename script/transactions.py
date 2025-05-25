import random
import csv
import mysql.connector
from datetime import datetime
import time
import os

connection = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE") 
)
cursor = connection.cursor()

employees = []
suppliers = {}
products = {}
def take_data():
    with open('employees.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            EmployeeID = row[0]
            employees.append(EmployeeID)
    
    with open('products.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            Product, Price, Supplier = row
            products[Product] = Price

            if (Supplier not in suppliers):
                suppliers[Supplier] = []
            suppliers[Supplier].append(Product)

def generate_invoice(n):
    for _ in range(n):
        now = datetime.now()
        InvoiceID = now.strftime("%Y%m%d%H%M%S")
        EmployeeID = random.choice(employees)
        PurchaseDate = now.strftime("%Y-%m-%d %H:%M:%S")
        Total = 0

        sql = """
        INSERT INTO INVOICE (InvoiceID, EmployeeID, PurchaseDate, Total)
        VALUES (%s, %s, %s, %s)
        """
        values = (InvoiceID, EmployeeID, PurchaseDate, Total)
        cursor.execute(sql, values)

        items = random.choice([1, 3, 5])
        orders = random.sample(list(products.keys()), k=items)
        for i in range(items):
            Quantity = random.choice([1, 2, 3])
            SubTotal = round(float(products[orders[i]]) * Quantity, 2)
            Total += SubTotal
            sql = """
            INSERT INTO INVOICE_DETAIL (InvoiceID, Number, ProductID, Quantity, SubTotal)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (InvoiceID, i + 1, orders[i], Quantity, SubTotal)
            cursor.execute(sql, values)

            sql = """
            UPDATE PRODUCT
            SET Stock = Stock - %s
            Where ProductID = %s
            """
            values = (Quantity, orders[i])
            cursor.execute(sql, values)
        
        sql = """
        UPDATE INVOICE
        SET total = %s
        WHERE InvoiceID = %s
        """
        values = (Total, InvoiceID)
        cursor.execute(sql, values)

        time.sleep(1)

def generate_import(n):
    for _ in range(n):
        now = datetime.now()
        ImportOrderID = now.strftime("%Y%m%d%H%M%S")
        SupplierID = random.choice(list(suppliers))
        ImportDate = now.strftime("%Y-%m-%d %H:%M:%S")
        Total = 0

        sql = """
        INSERT INTO IMPORT_ORDER (ImportOrderID, SupplierID, ImportDate, Total)
        VALUES (%s, %s, %s, %s)
        """
        values = (ImportOrderID, SupplierID, ImportDate, Total)
        cursor.execute(sql, values)

        items = random.choice([3, 5, 7, 9])
        items = min(items, len(suppliers[SupplierID]))
        orders = random.sample(suppliers[SupplierID], k=items)
        for i in range(items):
            Quantity = random.choice([50, 60, 70, 80, 100])
            SubTotal = round(float(products[orders[i]]) * Quantity * 0.6, 2)
            Total += SubTotal
            sql = """
            INSERT INTO IMPORT_ORDER_DETAIL (ImportOrderID, Number, ProductID, Quantity, SubTotal)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (ImportOrderID, i + 1, orders[i], Quantity, SubTotal)
            cursor.execute(sql, values)

            sql = """
            UPDATE PRODUCT
            SET Stock = Stock + %s
            Where ProductID = %s
            """
            values = (Quantity, orders[i])
            cursor.execute(sql, values)
        
        sql = """
        UPDATE IMPORT_ORDER
        SET total = %s
        WHERE ImportOrderID = %s
        """
        values = (Total, ImportOrderID)
        cursor.execute(sql, values)

        time.sleep(1)

take_data()
generate_invoice(20)
generate_import(10)

connection.commit()
cursor.close()
connection.close()
