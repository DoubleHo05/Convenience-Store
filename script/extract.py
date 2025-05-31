import csv
import os
import mysql.connector

# Database environment variables for connection
DB_HOST = os.getenv("MYSQL_HOST")
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_NAME = os.getenv("MYSQL_DATABASE")

OUTPUT_DIRECTORY = "extracted"


def extract_table_to_csv(cursor, table_name, filename):
    """Extracts all data from a given table and writes it to a CSV file.

    Keyword arguments:
    cursor -- The database cursor object.
    table_name -- The name of the table to extract data from.
    filename -- The name of the CSV file to write to.
    """
    query = f"select * from {table_name}"
    try:
        cursor.execute(query)
        result = cursor.fetchall()

        os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
        
        file_path = os.path.join(OUTPUT_DIRECTORY, filename)

        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if cursor.description:
                writer.writerow([desc[0] for desc in cursor.description])
            writer.writerows(result)
        print(f"Successfully extracted {table_name} to {file_path}")

    except mysql.connector.Error as err:
        print(f"Error executing query for table {table_name}: {err}")
    except IOError as e:
        print(f"Error writing file {filename}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while processing {table_name}: {e}")


def main():
    """
    Main function to connect to the database and extract all specified tables.
    """

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

        tables_to_extract = {
            "CATEGORY": "categories.csv",
            "PRODUCT": "products.csv",
            "EMPLOYEE": "employees.csv",
            "INVOICE": "invoices.csv",
            "INVOICE_DETAIL": "invoices_detail.csv",
            "SUPPLIER": "suppliers.csv",
            "IMPORT_ORDER": "import_orders.csv",
            "IMPORT_ORDER_DETAIL": "import_orders_detail.csv"
        }

        for table_name, csv_filename in tables_to_extract.items():
            extract_table_to_csv(cursor, table_name, csv_filename)

    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
    except Exception as e:
        print(f"An unexpected error occurred in main: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("Database connection closed.")


if __name__ == "__main__":
    main()