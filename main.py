import mysql.connector
from mysql.connector import Error

def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',  # Change if needed
            user='grafana',        # Change to your MySQL username
            password='grafana'  # Change to your MySQL password
        )
        if connection.is_connected():
            print("Connected to MySQL")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def create_schema(cursor, schema_name):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {schema_name}")
    print(f"Database '{schema_name}' checked/created.")

def create_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            value INT
        )
    """)
    print("Table 'test_data' checked/created.")

def insert_data(cursor):
    cursor.execute("SELECT COUNT(*) FROM test_data")
    count = cursor.fetchone()[0]
    if count == 0:
        data = [(f'Name{i}', i * 10) for i in range(10)]
        cursor.executemany("INSERT INTO test_data (name, value) VALUES (%s, %s)", data)
        print("Inserted initial dataset.")

def execute_queries(cursor):
    for i in range(1000):
        cursor.execute("SELECT * FROM test_data WHERE id = %s", (i % 10 + 1,))
        cursor.fetchall()
    print("Executed 1000 queries.")

def main():
    connection = connect_to_mysql()
    if connection:
        cursor = connection.cursor()
        
        schema_name = "grafana"
        create_schema(cursor, schema_name)
        cursor.execute(f"USE {schema_name}")
        create_table(cursor)
        insert_data(cursor)
        connection.commit()
        execute_queries(cursor)
        
        cursor.close()
        connection.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
