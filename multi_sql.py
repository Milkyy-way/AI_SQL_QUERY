import sqlite3

# Function to create and populate a database
def setup_database(db_name, table_name, create_table_sql, data):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # Create table
    cur.execute(create_table_sql)

    # Insert data
    cur.executemany(f"INSERT INTO {table_name} VALUES (?, ?, ?, ?)", data)

    conn.commit()
    conn.close()
    print(f"Database {db_name} setup complete!")

# Setup Student Database
setup_database(
    "student.db",
    "STUDENT",
    """
    CREATE TABLE IF NOT EXISTS STUDENT(
        NAME VARCHAR(25), 
        CLASS VARCHAR(25), 
        AGE INT, 
        MARKS INT
    );
    """,
    [
        ('avsai', 'AI', 24, 25), ('vy', 'ML', 23, 24),
        ('virat', 'DL', 22, 33), ('raina', 'AI', 24, 31),
        ('john', 'ML', 22, 28), ('emma', 'DL', 21, 35),
        ('liam', 'AI', 26, 40), ('olivia', 'ML', 27, 38),
        ('noah', 'DL', 25, 29), ('sophia', 'AI', 22, 33),
        ('jackson', 'ML', 23, 30), ('ava', 'DL', 24, 27),
        ('aiden', 'AI', 28, 32), ('isabella', 'ML', 26, 31),
        ('lucas', 'DL', 22, 34), ('mia', 'AI', 29, 29),
        ('elijah', 'ML', 30, 36), ('amelia', 'DL', 21, 37),
        ('benjamin', 'AI', 24, 39), ('harper', 'ML', 25, 35),
        ('ethan', 'DL', 28, 31), ('evelyn', 'AI', 27, 30),
        ('mason', 'ML', 26, 28), ('abigail', 'DL', 24, 40),
        ('logan', 'AI', 23, 34), ('ella', 'ML', 22, 37),
        ('alexander', 'DL', 30, 32), ('scarlett', 'AI', 25, 36),
        ('james', 'ML', 27, 33), ('chloe', 'DL', 29, 38)
    ]
)

# Setup Employee Database
setup_database(
    "employees.db",
    "EMPLOYEES",
    """
    CREATE TABLE IF NOT EXISTS EMPLOYEES(
        NAME VARCHAR(25), 
        DEPARTMENT VARCHAR(25), 
        SALARY INT, 
        EXPERIENCE INT
    );
    """,
    [
        ('John', 'IT', 70000, 5), ('Jane', 'HR', 65000, 6),
        ('Bob', 'Finance', 80000, 8), ('Alice', 'IT', 75000, 7),
        ('David', 'Marketing', 72000, 4), ('Emma', 'HR', 68000, 7),
        ('Michael', 'IT', 85000, 10), ('Sophia', 'Finance', 90000, 12),
        ('Daniel', 'Sales', 65000, 5), ('Olivia', 'Marketing', 78000, 8),
        ('James', 'IT', 87000, 9), ('Charlotte', 'HR', 70000, 6),
        ('William', 'Finance', 92000, 13), ('Amelia', 'Sales', 69000, 4),
        ('Ethan', 'IT', 83000, 10), ('Isabella', 'Marketing', 74000, 5),
        ('Mason', 'HR', 66000, 6), ('Mia', 'Finance', 89000, 11),
        ('Alexander', 'Sales', 72000, 7), ('Harper', 'IT', 79000, 8),
        ('Benjamin', 'Marketing', 81000, 9), ('Evelyn', 'HR', 75000, 7),
        ('Henry', 'Finance', 91000, 14), ('Abigail', 'Sales', 68000, 5),
        ('Liam', 'IT', 86000, 9), ('Ella', 'Marketing', 77000, 6),
        ('Lucas', 'HR', 73000, 7), ('Scarlett', 'Finance', 88000, 12),
        ('Daniel', 'Sales', 70000, 6), ('Victoria', 'IT', 80000, 10)
    ]
)

# Setup Sales Database
setup_database(
    "sales.db",
    "SALES",
    """
    CREATE TABLE IF NOT EXISTS SALES(
        PRODUCT VARCHAR(25), 
        REGION VARCHAR(25), 
        SALES INT, 
        REVENUE INT
    );
    """,
    [
        ('Laptop', 'North', 50, 100000), ('Phone', 'South', 100, 200000),
        ('Tablet', 'East', 30, 60000), ('Monitor', 'West', 20, 40000),
        ('Desktop', 'North', 40, 80000), ('Smartwatch', 'South', 90, 150000),
        ('Headphones', 'East', 70, 70000), ('Speakers', 'West', 25, 50000),
        ('Keyboard', 'North', 80, 160000), ('Mouse', 'South', 120, 180000),
        ('Camera', 'East', 45, 85000), ('Printer', 'West', 35, 75000),
        ('Smart TV', 'North', 55, 110000), ('Gaming Console', 'South', 95, 250000),
        ('Router', 'East', 60, 90000), ('Power Bank', 'West', 30, 60000),
        ('Monitor', 'North', 20, 50000), ('Projector', 'South', 75, 140000),
        ('SSD', 'East', 100, 220000), ('Hard Drive', 'West', 90, 180000),
        ('Graphics Card', 'North', 15, 300000), ('Motherboard', 'South', 35, 85000),
        ('RAM', 'East', 25, 65000), ('Processor', 'West', 55, 275000),
        ('VR Headset', 'North', 12, 48000), ('Fitness Band', 'South', 85, 90000),
        ('Bluetooth Speaker', 'East', 50, 95000), ('Smart Glasses', 'West', 22, 110000),
        ('Drone', 'North', 18, 200000), ('E-Reader', 'South', 65, 120000)
    ]
)