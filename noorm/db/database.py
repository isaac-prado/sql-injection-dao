import psycopg2


def getConnection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="northwind",
            user="root",
            password="root"
        )
        print("Connected to the database")
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None
