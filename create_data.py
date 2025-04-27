import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='welcome',
    database='my_store' 
)
cursor = connection.cursor()

from faker import Faker
import random
fake = Faker()

used_phone = set()
def get_unique_phone():
    while True:
        phone = fake.basic_phone_number()
        if phone not in used_phone:
            used_phone.add(phone)
            return phone

customer_ids = set()
def generate_customers(n):
    for _ in range(n):
        CustomerID = fake.unique.random_int(min = 1, max = 9999999999)
        customer_ids.add(CustomerID)
        CustomerName = fake.unique.name()
        CustomerPhone = get_unique_phone()
        sql = """
        INSERT INTO CUSTOMER (CustomerID, CustomerName, CustomerPhone)
        VALUES (%s, %s, %s)
        """
        values = (CustomerID, CustomerName, CustomerPhone)
        cursor.execute(sql, values)

employee_ids = set()
def generate_employee(n):
    for _ in range(n):
        EmployeeID = fake.unique.random_int(min = 1, max = 9999999999)
        employee_ids.add(EmployeeID)
        EmployeeName = fake.unique.name()
        EmployeePhone = get_unique_phone()
        EmployeePosition = "cashier"
        sql = """
        INSERT INTO EMPLOYEE (EmployeeID, EmployeeName, EmployeePhone, EmployeePosition)
        VALUES (%s, %s, %s, %s)
        """
        values = (EmployeeID, EmployeeName, EmployeePhone, EmployeePosition)
        cursor.execute(sql, values)

categories = {
    'Beverages': [
        'Coca-Cola', 'Pepsi', 'Sprite', 'Mountain Dew', 'Dr Pepper',
        'Fanta Orange', 'Gatorade', 'Red Bull', 'Monster Energy', 'Lipton Iced Tea',
        'Nestle Pure Life', 'Aquafina Water', 'Tropicana Orange Juice', 'Minute Maid Apple Juice', 'Starbucks Frappuccino',
        'V8 Vegetable Juice', 'Powerade', '7UP', 'Canada Dry Ginger Ale', 'Vitaminwater'
    ],
    
    'Snacks': [
        'Lays Classic Chips', 'Doritos Nacho Cheese', 'Cheetos Crunchy', 'Ruffles Sour Cream', 'Pringles Original',
        'Oreos', 'KitKat', 'Snickers', 'Twix',
        'M&Ms', 'Skittles', 'Milky Way', 'Butterfinger',
        'Goldfish Crackers', 'Trail Mix', 'Granola Bar', 'Pop-Tarts', 'Slim Jim'
    ],
    
    'Dairy': [
        'Whole Milk', '2% Milk', 'Almond Milk', 'Oat Milk', 'Greek Yogurt',
        'Cheddar Cheese', 'Mozzarella Cheese', 'String Cheese', 'Butter', 'Cottage Cheese',
        'Cream Cheese', 'Sour Cream', 'Chocolate Milk', 'Half and Half', 'Coffee Creamer',
        'Vanilla Yogurt', 'Go-Gurt', 'Parmesan Cheese', 'Swiss Cheese', 'Heavy Whipping Cream'
    ],
    
    'Bakery': [
        'White Bread', 'Whole Wheat Bread', 'Bagels', 'English Muffins', 'Croissant',
        'Donuts', 'Pound Cake', 'Banana Bread', 'Tortillas', 'Brioche Buns',
        'Hamburger Buns', 'Hot Dog Buns', 'Pita Bread', 'Cinnamon Rolls', 'Blueberry Muffins',
        'Cupcakes', 'Brownies', 'Pretzels', 'Garlic Bread', 'Fruit Cake'
    ],
    
    'Frozen Foods': [
        'Frozen Pizza', 'Frozen Burrito', 'Frozen Vegetables', 'Frozen French Fries', 'Frozen Chicken Nuggets',
        'Ice Cream', 'Frozen Waffles', 'Frozen Pancakes', 'Frozen Lasagna', 'Frozen Meatballs',
        'Frozen Fish Sticks', 'Frozen Corn Dogs', 'Frozen Breakfast Sandwich', 'Frozen Smoothie Packs', 'Frozen Shrimp',
        'Frozen Edamame', 'Frozen Mozzarella Sticks', 'Frozen Broccoli', 'Frozen Onion Rings', 'Frozen Garlic Bread'
    ],
    
    'Canned Goods': [
        'Canned Corn', 'Canned Green Beans', 'Canned Tuna', 'Canned Chicken', 'Canned Beans',
        'Canned Soup', 'Canned Tomatoes', 'Canned Fruit Cocktail', 'Canned Peaches', 'Canned Pineapple',
        'Canned Chili', 'Canned Beef Stew', 'Canned Spaghetti', 'Canned Pasta Sauce', 'Canned Mushroom Soup',
        'Canned Pumpkin', 'Canned Sweet Potatoes', 'Canned Coconut Milk', 'Canned Beets', 'Canned Salsa'
    ],
    
    'Personal Care': [
        'Shampoo', 'Conditioner', 'Body Wash', 'Bar Soap', 'Toothpaste',
        'Toothbrush', 'Mouthwash', 'Floss', 'Deodorant', 'Hand Sanitizer',
        'Face Wash', 'Face Moisturizer', 'Sunscreen', 'Razor Blades', 'Shaving Cream',
        'Lotion', 'Lip Balm', 'Cotton Swabs', 'Hair Gel', 'Nail Clippers'
    ],
    
    'Household': [
        'Paper Towels', 'Toilet Paper', 'Dish Soap', 'Laundry Detergent', 'Fabric Softener',
        'All-Purpose Cleaner', 'Glass Cleaner', 'Sponges', 'Trash Bags', 'Aluminum Foil',
        'Plastic Wrap', 'Laundry Baskets', 'Brooms', 'Mops', 'Air Freshener',
        'Disinfectant Wipes', 'Bleach', 'Rubber Gloves', 'Light Bulbs', 'Matches'
    ],
    
    'Pet Supplies': [
        'Dry Dog Food', 'Canned Dog Food', 'Dog Treats', 'Dog Chew Toys', 'Dog Leash',
        'Dry Cat Food', 'Canned Cat Food', 'Cat Treats', 'Cat Litter', 'Cat Scratching Post',
        'Bird Seed', 'Fish Food', 'Dog Shampoo', 'Cat Collar', 'Small Animal Bedding',
        'Pet Bowls', 'Pet Carrier', 'Flea Treatment', 'Pet Dental Treats', 'Hamster Wheel'
    ],
    
    'Baby Products': [
        'Baby Wipes', 'Diapers', 'Baby Lotion', 'Baby Shampoo', 'Baby Powder',
        'Baby Formula', 'Baby Bottles', 'Pacifiers', 'Baby Food Jars', 'Baby Snacks',
        'Baby Bibs', 'Teething Toys', 'Baby Monitor', 'Changing Pads', 'Baby Nail Clippers',
        'Baby Clothes', 'Baby Blankets', 'Sippy Cups', 'Stroller Toys', 'Diaper Rash Cream'
    ]
}

product_ids = {}
def generate_product(n):
    for _ in range(n):
        ProductID = fake.unique.random_int(min = 1, max = 9999999999)
        Category = random.choice(list(categories.keys()))
        ProductName = random.choice(categories[Category])
        Price = round(random.uniform(1.00, 20.00), 2)
        Stock = random.randint(200, 1000)
        product_ids[ProductID] = Price
        sql = """
        INSERT INTO PRODUCT (ProductID, ProductName, Category, Price, Stock)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (ProductID, ProductName, Category, Price, Stock)
        cursor.execute(sql, values)

invoice_ids = set()
def generate_invoice(n):
    for _ in range(n):
        InvoiceID = fake.unique.random_int(min = 1, max = 9999999999)
        invoice_ids.add(InvoiceID)
        CustomerID = random.choice(list(customer_ids))
        EmployeeID = random.choice(list(employee_ids))
        PurchaseDate = fake.date_time()
        sql = """
        INSERT INTO INVOICE (InvoiceID, CustomerID, EmployeeID, PurchaseDate)
        VALUES (%s, %s, %s, %s)
        """
        values = (InvoiceID, CustomerID, EmployeeID, PurchaseDate)
        cursor.execute(sql, values)

def generate_invoice_detail(n):
    for InvoiceID in list(invoice_ids):
        for i in range(1, 4):
            Ordinal = i
            ProductID = random.choice(list(product_ids))
            Quantity = random.randint(1, 5)
            Cost = round(Quantity * product_ids[ProductID], 2)
            sql = """
            INSERT INTO INVOICE_DETAIL (InvoiceID, Ordinal, ProductID, Quantity, Cost)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (InvoiceID, Ordinal, ProductID, Quantity, Cost)
            cursor.execute(sql, values)

supplier_ids = set()
def generate_supplier(n):
    for _ in range(n):  
        SupplierID = fake.unique.random_int(min = 1, max = 9999999999)
        supplier_ids.add(SupplierID)
        SupplierName = fake.unique.company()
        SupplierPhone = get_unique_phone()
        SupplierAddress = fake.unique.address()
        sql = """
        INSERT INTO SUPPLIER (SupplierID, SupplierName, SupplierPhone, SupplierAddress)
        VALUES (%s, %s, %s, %s)
        """
        values = (SupplierID, SupplierName, SupplierPhone, SupplierAddress)
        cursor.execute(sql, values)

importOrder_ids = set()
def generate_importOrder(n):
    for _ in range(n):
        ImportOrderID = fake.unique.random_int(min = 1, max = 9999999999)
        importOrder_ids.add(ImportOrderID)
        SupplierID = random.choice(list(supplier_ids))
        ImportDate = fake.date_time()
        sql = """
        INSERT INTO IMPORT_ORDER (ImportOrderID, SupplierID, ImportDate)
        VALUES (%s, %s, %s)
        """
        values = (ImportOrderID, SupplierID, ImportDate)
        cursor.execute(sql, values)

def generate_import_order_detail(n):
    for ImportOrderID in list(importOrder_ids):
        for i in range(1, 4):
            Ordinal = i
            ProductID = random.choice(list(product_ids))
            Quantity = random.randint(1, 100)
            CostPerUnit = round(product_ids[ProductID] * 4 / 5, 2)
            sql = """
            INSERT INTO IMPORT_ORDER_DETAIL (ImportOrderID, Ordinal, ProductID, Quantity, CostPerUnit)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (ImportOrderID, Ordinal, ProductID, Quantity, CostPerUnit)
            cursor.execute(sql, values)

generate_customers(10)
generate_employee(10)
generate_product(10)
generate_invoice(10)
generate_invoice_detail(10)
generate_supplier(5)
generate_importOrder(10)
generate_import_order_detail(10)

# Commit the changes to the database
connection.commit()

# Close the connection
cursor.close()
connection.close()