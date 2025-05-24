import csv
import mysql.connector
import os

connection = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE") 
)
cursor = connection.cursor()

from faker import Faker
import random
fake = Faker()

employees = []
def generate_employee(n):
    for i in range(n):
        EmployeeID = f"E{i + 1:03d}"
        EmployeeName = fake.unique.name()
        EmployeePhone = fake.unique.basic_phone_number()
        EmployeePosition = random.choices(['cashier', 'manager'], weights=[0.9, 0.1])[0]
        sql = """
        INSERT INTO EMPLOYEE (EmployeeID, EmployeeName, EmployeePhone, EmployeePosition)
        VALUES (%s, %s, %s, %s)
        """
        values = (EmployeeID, EmployeeName, EmployeePhone, EmployeePosition)
        cursor.execute(sql, values)

        employees.append([EmployeeID])

    with open('employees.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["EmployeeID"])
        writer.writerows(employees)

products = []
categories = {}
suppliers = {}
def generate_product():
    with open('data.csv', mode= 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        p = c = s = 1
        for row in reader:
            CategoryName, ProductName, Price, SupplierName, SupplierPhone, SupplierAddress = row

            if (CategoryName in categories):
                p += 1
            else:
                p = 1
                categories[CategoryName] = f"{c:03d}"
                c += 1
            
            if (SupplierName not in suppliers):
                suppliers[SupplierName] = [f"{s:03d}", SupplierPhone, SupplierAddress]
                s += 1

            ProductID = f"{CategoryName[:2]}{p:03d}"

            products.append({
                'Product': ProductID,
                'Price': Price,
                'Supplier': suppliers[SupplierName][0]
            })

            Stock = 500
            sql = """
            INSERT INTO PRODUCT (ProductID, ProductName, Category, Price, Stock)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (ProductID, ProductName, categories[CategoryName], Price, Stock)
            cursor.execute(sql, values)
    
    with open('products.csv', 'w', newline='') as file:
        fieldnames = ['Product', 'Price', 'Supplier']
        writer = csv.DictWriter(file, fieldnames = fieldnames)
        writer.writeheader()
        writer.writerows(products)
    
    
def generate_categories():
    for CategoryName in categories.keys():
        CategoryID = categories[CategoryName]
        sql = """
        INSERT INTO CATEGORY (CategoryID, CategoryName)
        VALUES (%s, %s)
        """
        values = (CategoryID, CategoryName)
        cursor.execute(sql, values)
    
    sql = """
    ALTER TABLE PRODUCT
    ADD FOREIGN KEY (Category) REFERENCES CATEGORY(CategoryID)
    """
    cursor.execute(sql)

def generate_suppliers():
    for SupplierName in suppliers.keys():
        SupplierID = suppliers[SupplierName][0]
        SupperlierPhone = suppliers[SupplierName][1]
        SupplierAddress = suppliers[SupplierName][2]
        sql = """
        INSERT INTO SUPPLIER (SupplierID, SupplierName, SupplierPhone, SupplierAddress)
        VALUES (%s, %s, %s, %s)
        """
        values = (SupplierID, SupplierName, SupperlierPhone, SupplierAddress)
        cursor.execute(sql, values)

generate_employee(10)
generate_product()
generate_categories()
generate_suppliers()

connection.commit()
cursor.close()
connection.close()