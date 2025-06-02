import csv
import os
import random
import time
from datetime import datetime

import mysql.connector

# Database environment variables for connection
DB_HOST = os.getenv("MYSQL_HOST")
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_NAME = os.getenv("MYSQL_DATABASE")

employees_list = []
suppliers_products = {}  
product_prices = {}      


def take_data():
    """Reads data from CSV files to populate global data structures."""
    global employees_list, product_prices, suppliers_products

    try:
        with open('employees.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                employee_id = row[0]
                employees_list.append(employee_id)

        with open('products.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                product_id, price, supplier_name = row
                product_prices[product_id] = price
                if supplier_name not in suppliers_products:
                    suppliers_products[supplier_name] = []
                suppliers_products[supplier_name].append(product_id)

    except FileNotFoundError as e:
        print(f"Error: {e}. Please ensure 'employees.csv' and 'products.csv' exist.")
        exit()
    except Exception as e:
        print(f"An error occurred while reading CSV files: {e}")
        exit()

    if not employees_list:
        print("Warning: No employees loaded. Invoices cannot be generated correctly.")
    if not product_prices:
        print("Warning: No products loaded. Invoices and imports cannot be generated correctly.")
    if not suppliers_products:
        print("Warning: No suppliers loaded. Imports cannot be generated correctly.")


def generate_invoice(cursor, num_invoices):
    """Generates a specified number of invoices and their details.
    
    Keyword arguments:
    cursor -- the database cursor
    num_invoices -- the number of invoices will be created
    """
    if not employees_list or not product_prices:
        print("Cannot generate invoices: Employee or product data is missing.")
        return

    for _ in range(num_invoices):
        now = datetime.now()
        invoice_id = now.strftime("%Y%m%d%H%M%S")
        employee_id = random.choice(employees_list)
        purchase_date = now.strftime("%Y-%m-%d %H:%M:%S")
        total_amount = 0

        sql_invoice = """
        INSERT INTO INVOICE (InvoiceID, EmployeeID, PurchaseDate, Total)
        VALUES (%s, %s, %s, %s)
        """
        values_invoice = (invoice_id, employee_id, purchase_date, total_amount)
        cursor.execute(sql_invoice, values_invoice)

        num_items_in_invoice = random.choice([1, 3, 5])
        available_products = list(product_prices.keys())
        if not available_products:
            print(f"Warning: No products available to add to invoice {invoice_id}.")
            continue
        if len(available_products) < num_items_in_invoice:
            num_items_in_invoice = len(available_products)

        ordered_products = random.sample(available_products, k=num_items_in_invoice)

        for i, product_id in enumerate(ordered_products):
            quantity = random.choice([1, 2, 3])
            try:
                price = float(product_prices[product_id])
            except ValueError:
                print(f"Warning: Invalid price for product {product_id}. Skipping item.")
                continue
            sub_total = round(price * quantity, 2)
            total_amount += sub_total

            sql_invoice_detail = """
            INSERT INTO INVOICE_DETAIL (InvoiceID, Number, ProductID, Quantity, SubTotal)
            VALUES (%s, %s, %s, %s, %s)
            """
            values_detail = (invoice_id, i + 1, product_id, quantity, sub_total)
            cursor.execute(sql_invoice_detail, values_detail)

            sql_update_product_stock = """
            UPDATE PRODUCT
            SET Stock = Stock - %s
            WHERE ProductID = %s
            """
            values_stock = (quantity, product_id)
            cursor.execute(sql_update_product_stock, values_stock)

        sql_update_invoice_total = """
        UPDATE INVOICE
        SET Total = %s
        WHERE InvoiceID = %s
        """
        values_total_update = (round(total_amount, 2), invoice_id)
        cursor.execute(sql_update_invoice_total, values_total_update)

        time.sleep(1)


def generate_import(cursor, num_imports):
    """Generates a specified number of import orders and their details.
    
    Keyword arguments:
    cursor -- the database cursor
    num_imports -- the number of imports will be created
    """
    if not suppliers_products or not product_prices:
        print("Cannot generate imports: Supplier or product data is missing.")
        return

    all_supplier_ids = list(suppliers_products.keys())
    if not all_supplier_ids:
        print("Warning: No suppliers available to generate import orders.")
        return

    for _ in range(num_imports):
        now = datetime.now()
        import_order_id = now.strftime("%Y%m%d%H%M%S") 
        supplier_id = random.choice(all_supplier_ids)
        import_date = now.strftime("%Y-%m-%d %H:%M:%S")
        total_amount = 0

        sql_import_order = """
        INSERT INTO IMPORT_ORDER (ImportOrderID, SupplierID, ImportDate, Total)
        VALUES (%s, %s, %s, %s)
        """
        values_import_order = (import_order_id, supplier_id, import_date, total_amount)
        cursor.execute(sql_import_order, values_import_order)

        products_from_supplier = suppliers_products[supplier_id]

        num_items_to_import = random.choice([3, 5, 7, 9])
        num_items_to_import = min(num_items_to_import, len(products_from_supplier))

        ordered_products = random.sample(products_from_supplier, k=num_items_to_import)

        for i, product_id in enumerate(ordered_products):
            quantity = random.choice([50, 60, 70, 80, 100])
            try:
                price = float(product_prices[product_id])
            except ValueError:
                print(f"Warning: Invalid price for product {product_id} during import. Skipping item.")
                continue

            cost_factor = 0.6
            sub_total = round(price * quantity * cost_factor, 2)
            total_amount += sub_total

            sql_import_detail = """
            INSERT INTO IMPORT_ORDER_DETAIL (ImportOrderID, Number, ProductID, Quantity, SubTotal)
            VALUES (%s, %s, %s, %s, %s)
            """
            values_detail = (import_order_id, i + 1, product_id, quantity, sub_total)
            cursor.execute(sql_import_detail, values_detail)

            sql_update_product_stock = """
            UPDATE PRODUCT
            SET Stock = Stock + %s
            WHERE ProductID = %s
            """
            values_stock = (quantity, product_id)
            cursor.execute(sql_update_product_stock, values_stock)

        sql_update_import_total = """
        UPDATE IMPORT_ORDER
        SET Total = %s
        WHERE ImportOrderID = %s
        """
        values_total_update = (round(total_amount, 2), import_order_id)
        cursor.execute(sql_update_import_total, values_total_update)

        time.sleep(1)


def main():
    """Main function to connect to DB, process data, and generate records."""

    connection = None 
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = connection.cursor()
        print("Successfully connected to the database.")

        take_data()

        if not employees_list and not product_prices and not suppliers_products:
            print("No data loaded from CSVs. Exiting without generating records.")
            return

        print("Generating invoices...")
        generate_invoice(cursor, 20)
        print("Invoice generation complete.")

        print("Generating import orders...")
        generate_import(cursor, 10)
        print("Import order generation complete.")

        connection.commit()
        print("All changes committed to the database.")

    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        if connection and connection.is_connected():
            connection.rollback()
            print("Transaction rolled back.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        if connection and connection.is_connected():
            connection.rollback()
            print("Transaction rolled back due to unexpected error.")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("Database connection closed.")


if __name__ == "__main__":
    main()