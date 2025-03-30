import mysql.connector
import pandas as pd
from mysql.connector import Error

# Connection details
hostname = 'localhost'
database = 'olist_ecommerce'
username = 'root'
password = '1234'

# CSV file path
csv_file_path = r"D:\Data Engineering Projects\Olist E-Commerce Azure Data Engineering Project\olist-ecommerce-azure-data-engineering-project\dataset\olist_order_payments_dataset.csv"

# Table name
table_name = "olist_order_payments"

try:
    # Step 1: Establish a connection to MySQL server
    connection = mysql.connector.connect(
        host=hostname,
        user=username,
        password=password,
        database=database
    )


    if connection.is_connected():
        print("Connection established successfully to MySQL Database")

        # Step 2: Create a cursor to execute SQL queries
        cursor = connection.cursor()

        # Step 3: Drop table if it already exists (for clean insertion)
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        print(f"Table `{table_name}` dropped if it existed.")

        # Step 4: Create a table structure to match CSV file
        create_table_query = f"""
            CREATE TABLE {table_name} (
                order_id VARCHAR(50),
                payment_sequential INT,
                payment_type VARCHAR(20),
                payment_installments INT,
                payment_value FLOAT
            )
            """
        cursor.execute(create_table_query)
        print(f"Table `{table_name}` created successfully!")

        # Step 5: Load the CSV data into pandas DataFrame
        df = pd.read_csv(csv_file_path)
        print("CSV data loaded into pandas DataFrame.")

        # Step 6: Insert data in batches of 1000 records
        batch_size = 1000
        total_records = len(df)
        print(f"Starting data ingestion to table `{table_name}` in batches of {batch_size} records.")
        for start in range(0, total_records, batch_size):
            end = start + batch_size
            batch = df[start:end] # Get the current batch of records

            # Convert the batch data into a list of tuples
            batch_records = list(batch.itertuples(index=False, name=None))

            # Prepare the insert query
            insert_query = f"""
                INSERT INTO {table_name} (order_id, payment_sequential, payment_type, payment_installments, payment_value)
                VALUES (%s, %s, %s, %s, %s)
            """

            # Execute the insert query with the current batch of records
            cursor.executemany(insert_query, batch_records)
            connection.commit()
            print(f"Inserted records {start + 1} to {end} records into table `{table_name}`.")

        print(f"All {total_records} records inserted successfully into table `{table_name}`.")

except Error as e:
    # Step 7: Handle any errors that occurred
    print("Error while connecting to MySQL", e)

finally:
    # Step 8: Close the cursor and connection
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")