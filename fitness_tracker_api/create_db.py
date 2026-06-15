import psycopg2

try:
    # Connect to default 'postgres' database to create the new one
    conn = psycopg2.connect(
        dbname='postgres', 
        user='postgres', 
        password='Alie', 
        host='localhost', 
        port='5432'
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Execute the database creation
    cursor.execute("CREATE DATABASE fitness_db;")
    print("🎉 Success! 'fitness_db' has been created.")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f"❌ Error occurred: {e}")