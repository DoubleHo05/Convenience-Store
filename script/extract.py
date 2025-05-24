import mysql.connector
import csv
import os

connection = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE") 
)
cursor = connection.cursor()

def extract_categories():
    query = """SELECT * FROM CATEGORY"""
    cursor.execute(query)
    result = cursor.fetchall()
    
    with open('extracted/categories.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(i[0] for i in cursor.description)
        writer.writerows(result)

def extract_products():
    query = """SELECT * FROM PRODUCT"""
    cursor.execute(query)
    result = cursor.fetchall()
    
    with open('extracted/products.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(i[0] for i in cursor.description)
        writer.writerows(result)

def extract_employees():
    query = """SELECT * FROM EMPLOYEE"""
    cursor.execute(query)
    result = cursor.fetchall()

    with open('extracted/employees.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(i[0] for i in cursor.description)
        writer.writerows(result)

def extract_invoices():
    query = """SELECT * FROM INVOICE"""
    cursor.execute(query)
    result = cursor.fetchall()
    
    with open('extracted/invoices.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(i[0] for i in cursor.description)
        writer.writerows(result)

def extract_invoices_detail():
    query = """SELECT * FROM INVOICE_DETAIL"""
    cursor.execute(query)
    result = cursor.fetchall()

    with open('extracted/invoices_detail.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(i[0] for i in cursor.description)
        writer.writerows(result)

def extract_suppliers():
    query = """SELECT * FROM SUPPLIER"""
    cursor.execute(query)
    result = cursor.fetchall()
    
    with open('extracted/suppliers.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(i[0] for i in cursor.description)
        writer.writerows(result)

def extract_import_orders():
    query = """SELECT * FROM IMPORT_ORDER"""
    cursor.execute(query)
    result = cursor.fetchall()
    
    with open('extracted/import_orders.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(i[0] for i in cursor.description)
        writer.writerows(result)

def extract_import_orders_detail():
    query = """SELECT * FROM IMPORT_ORDER_DETAIL"""
    cursor.execute(query)
    result = cursor.fetchall()
    
    with open('extracted/import_orders_detail.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(i[0] for i in cursor.description)
        writer.writerows(result)

os.makedirs('extracted', exist_ok=True)
extract_categories()
extract_products()
extract_employees()
extract_invoices()
extract_invoices_detail()
extract_suppliers()
extract_import_orders()
extract_import_orders_detail()

cursor.close()
connection.close()