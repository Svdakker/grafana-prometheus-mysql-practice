from prometheus_client import start_http_server, Counter
import mysql.connector
from mysql.connector import Error
import time, random


# Define Prometheus metrics
QUERY_COUNTER = Counter('mysql_queries_total', 'Total number of queries executed')

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
            column1 INT,
            column2 VARCHAR(255),
            column3 INT
        )
    """)
    print("Table 'test_data' checked/created.")

def insert_data(cursor, num_rows=10000):
    cursor.execute("SELECT COUNT(*) FROM test_data")
    count = cursor.fetchone()[0]
    if count == 0:
        print("Inserting large dataset...")
        insert_query = """
        INSERT INTO test_data (column1, column2, column3)
        VALUES (%s, %s, %s)
        """
        
        # Inserting random data for the dataset
        data_to_insert = []
        for _ in range(num_rows):
            # For example, random data for column1, column2, and column3
            column1 = random.randint(1, 100)
            column2 = random.choice(['A', 'B', 'C', 'D', 'E'])
            column3 = random.random()  # Random float for column3
            data_to_insert.append((column1, column2, column3))

        cursor.executemany(insert_query, data_to_insert)
        print(f"Inserted {num_rows} rows.")

def execute_simple_query(cursor):
    query = "SELECT COUNT(*) FROM test_data"  # Simple query: counting rows
    cursor.execute(query)
    result = cursor.fetchone()
    print(f"Simple query result: {result[0]} rows")

# Function to execute complex queries on the large dataset
def execute_complex_query(cursor):
    query = """
    SELECT column2, AVG(column3) 
    FROM test_data 
    WHERE column1 > %s
    GROUP BY column2
    HAVING AVG(column3) > %s
    ORDER BY AVG(column3) DESC
    LIMIT 5
    """
    condition1 = random.randint(50, 100)  # Random condition for column1
    condition2 = random.random()  # Random average condition for column3
    cursor.execute(query, (condition1, condition2))
    results = cursor.fetchall()
    print("Complex query results:")
    for row in results:
        print(row)

# Function to simulate different query complexities
def run_queries(cursor):
    query_types = ['simple', 'complex']
    for _ in range(10):  # Run 10 queries for example
        query_type = random.choice(query_types)
        if query_type == 'simple':
            execute_simple_query(cursor)
            QUERY_COUNTER.inc()
        else:
            execute_complex_query(cursor)
            QUERY_COUNTER.inc()

def main():
    # Start Prometheus metric server
    start_http_server(8000)
    
    connection = connect_to_mysql()
    if connection:
        cursor = connection.cursor()
        
        schema_name = "grafana"
        create_schema(cursor, schema_name)
        cursor.execute(f"USE {schema_name}")
        create_table(cursor)
        insert_data(cursor, num_rows=10000)
        connection.commit()
        start_time = time.time()

        while time.time() - start_time < 600:
            run_queries(cursor)
            time.sleep(random.uniform(1,3))
        
        cursor.close()
        connection.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
