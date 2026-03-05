import psycopg2
import os
from dotenv import load_dotenv

###connect to the PostgreSQL database
def main(): 
    ##load environment variables from .env file
    load_dotenv()

    try: 
        db_url = os.getenv("DB_URL")

        if not db_url:
            raise Exception("DB_URL not found in environment variables")
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()  
        # Create the users table
        query_sql = 'SELECT VERSION()'

        cursor.execute(query_sql)

        version = cursor.fetchone()[0]
        print(f"Connected to PostgreSQL database. Version: {version}")

        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
    
###Execute the DDL commands to create the tables
def execute_ddl(conn, table_name, column):
    """
    Create a table in the database with the specified name and column definition.
    column: list of tuples (column_name, data_type)
    """
    cols = ', '.join([f"{name} {data_type}" for name, data_type in column])
    sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({cols});"
    with conn.cursor() as cursor:
        cursor.execute(sql)
        conn.commit()

###create table for course
def create_table_course(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Courses(
                course_id SERIAL PRIMARY KEY,
                course_name VARCHAR(100) UNIQUE NOT NULL,  
                credits INT,          
                instructor VARCHAR(100),
                price NUMERIC(10, 2),
                duration INT 
            );
        """)
        conn.commit()
###Query to table for course
def execute_ddl(conn, query, params=None):
    """
    Execute query with all results
    """
    with conn.cursor() as cursor:
        cursor.execute(query, params or ())
        if cursor.description:  # Check if the query returns results
            return cursor.fetchall()    
        return None
### Insert data into table for course
def execute_dml(conn, data):
    with conn.cursor() as cursor:
        for course_data, details in data.items():
            cursor.execute("""
                INSERT INTO Courses (course_name, credits, instructor, price, duration)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (course_name) DO NOTHING;
            """, (course_data, details['credits'], details['instructor'], details['price'], details['duration']))
        conn.commit()


if __name__ == "__main__":
    main()