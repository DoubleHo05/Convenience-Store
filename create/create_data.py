import os
import csv
import random

from faker import Faker
import mysql.connector

# Database environment variables for connection
DB_HOST = os.getenv("MYSQL_HOST")
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_NAME = os.getenv("MYSQL_DATABASE")

INPUT_DATA_CSV = 'data.csv'
EMPLOYEES_CSV = 'employees.csv'
PRODUCTS_CSV = 'products.csv'

categories = {}
suppliers = {}

fake = Faker()


def generate_employees(db_cursor, count):
    """Generate employees using faker.
    
    Keyword arguments:
    db_cursor -- the database cursor
    count -- the number of employees
    """
    temp_employee_ids_for_csv = []
    for i in range(count):
        employee_id = f"E{i + 1:03d}"
        employee_name = fake.unique.name()
        employee_phone = fake.unique.basic_phone_number()
        employee_position = random.choices(['cashier', 'manager'], weights=[0.9, 0.1])[0]

        sql = """
        INSERT INTO EMPLOYEE (EmployeeID, EmployeeName, EmployeePhone, EmployeePosition)
        VALUES (%s, %s, %s, %s)
        """
        values = (employee_id, employee_name, employee_phone, employee_position)
        db_cursor.execute(sql, values)

        temp_employee_ids_for_csv.append([employee_id])

    with open('./ft/employees.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["employee_id"])
        writer.writerows(temp_employee_ids_for_csv)


def generate_products(db_cursor, file_path):
    """From csv file, the data is processed and put in suitable dictionaries. Then data of product 
    is put into PRODUCT table.
    
    Keyword arguments:
    db_cursor -- the database cursor
    file_path -- csv file path
    """
    products = []
    
    with open(file_path, mode= 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)

        product_id_counter = 1 
        category_id_counter = 1 
        supplier_id_counter = 1

        for row in reader:
            category_name, product_name, price, supplier_name, supplier_phone, supplier_address = row

            if (category_name in categories):
                product_id_counter += 1
            else:
                product_id_counter = 1
                categories[category_name] = f"{category_id_counter:03d}"
                category_id_counter += 1
            
            if (supplier_name not in suppliers):
                suppliers[supplier_name] = [f"{supplier_id_counter:03d}", supplier_phone, supplier_address]
                supplier_id_counter += 1

            product_id = f"{category_name[:2]}{product_id_counter:03d}"

            products.append({
                'product': product_id,
                'price': price,
                'supplier': suppliers[supplier_name][0]
            })

            stock = 500
            sql = """
            INSERT INTO PRODUCT (ProductID, ProductName, Category, Price, Stock)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (product_id, product_name, categories[category_name], price, stock)
            db_cursor.execute(sql, values)
    
    with open('./ft/products.csv', 'w', newline='') as file:
        fieldnames = ['product', 'price', 'supplier']
        writer = csv.DictWriter(file, fieldnames = fieldnames)
        writer.writeheader()
        writer.writerows(products)
    
    
def generate_categories(db_cursor):
    """Populate CATEGORY table with data in 'categories'
    
    Keyword arguments:
    db_cursor -- the database cursor
    """
    for category_name in categories.keys():
        category_id = categories[category_name]
        sql = """
        INSERT INTO CATEGORY (CategoryID, CategoryName)
        VALUES (%s, %s)
        """
        values = (category_id, category_name)
        db_cursor.execute(sql, values)
    
    sql = """
    ALTER TABLE PRODUCT
    ADD FOREIGN KEY (Category) REFERENCES CATEGORY(CategoryID)
    """
    db_cursor.execute(sql)


def generate_suppliers(db_cursor):
    """Populate SUPPLIER table with data in 'suppliers'
    
    Keyword arguments:
    db_cursor -- the database cursor
    """
    for supplier_name in suppliers.keys():
        supplier_id = suppliers[supplier_name][0]
        supplier_phone = suppliers[supplier_name][1]
        supplier_address = suppliers[supplier_name][2]
        sql = """
        INSERT INTO SUPPLIER (SupplierID, SupplierName, SupplierPhone, SupplierAddress)
        VALUES (%s, %s, %s, %s)
        """
        values = (supplier_id, supplier_name, supplier_phone, supplier_address)
        db_cursor.execute(sql, values)


def main():
    """
    Main function to orchestrate data generation, database insertion,
    and CSV writing.
    """
    db_connection = None  # Initialize to ensure it's defined in finally block
    try:
        db_connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if not db_connection.is_connected():
            print("Database connection failed.")
            return

        cursor = db_connection.cursor()
        print("Successfully connected to the database.")

        generate_employees(cursor, 10)
        
        generate_products(cursor, INPUT_DATA_CSV)

        generate_categories(cursor)
        generate_suppliers(cursor)

        db_connection.commit()
        print("All data committed to the database.")

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        if db_connection and db_connection.is_connected():
            db_connection.rollback()
            print("Database transaction rolled back.")
    except IOError as e:
        print(f"File I/O error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
            print("Database cursor closed.")
        if db_connection and db_connection.is_connected():
            db_connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()