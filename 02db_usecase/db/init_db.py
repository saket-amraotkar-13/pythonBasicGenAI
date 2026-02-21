
import psycopg2
import os
from dotenv import load_dotenv

##load or connection string from env file
load_dotenv()

try:
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(os.getenv("DB_URL"))
    cursor = conn.cursor()
    query_sql = 'SELECT version();'
    cursor.execute(query_sql)
    version = cursor.fetchone()[0]
    print(f"Connected to PostgreSQL version: {version}")
    # Create a new table called "users"
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS users (
        userid SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        salary NUMERIC(10, 2) NOT NULL,
        currency VARCHAR(3) NOT NULL
    );
    '''
    conn.commit()
    print("Table 'users' created successfully.")
    
    # Insert data from a list of dictionaries
    user_data = [
        {"name": "John Doe", "email": "john.doe@example.com", "salary": 50000.00, "currency": "USD"},
        {"name": "Jane Smith", "email": "jane.smith@example.com", "salary": 60000.00, "currency": "USD"},
        {"name": "Alice Johnson", "email": "alice.johnson@example.com", "salary": 70000.00, "currency": "USD"}
    ]

    insert_query = ''' 
        INSERT INTO users (name, email, salary, currency) VALUES
        (%s, %s, %s, %s)
        on conflict (email) do nothing;
    '''

    for user in user_data:
        cursor.execute(insert_query, (user["name"], user["email"], user["salary"], user["currency"]))
        conn.commit()
    
    print("All user data inserted successfully.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()