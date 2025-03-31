import pandas as pd
from pymongo import MongoClient

# CSV file path
csv_file_path = r"D:\Data Engineering Projects\Olist E-Commerce Azure Data Engineering Project\olist-ecommerce-azure-data-engineering-project\dataset\product_category_name_translation.csv"

# Load the product_category CSV file into a pandas DataFrame
try:
    product_category_df = pd.read_csv(csv_file_path)
except FileNotFoundError:
    print(f"File not found at location: {csv_file_path}")
    exit()  # Exit the script if the file is not found

# MongoDB connection string
username = "sonawaneketan1993"
password = "Br4Bvpx6ytt0MQb2"
database = "olist_ecommerce"
collection_name = "product_category_name_translation"
conn_string = f"mongodb+srv://{username}:{password}@olist-ecomm-cluster.qmqybdb.mongodb.net/"

try:
    # Step 1: Establish a connection to MongoDB server
    client = MongoClient(conn_string)
    print("Connection established successfully to MongoDB Database")

    # Step 2: Create a database
    db = client[database]

    # Step 3: Create a collection
    collection = db[collection_name]
    print("Collection `product_category_name_translation` created successfully!")

    # Step 4: Insert data into the collection
    records = product_category_df.to_dict(orient='records')
    collection.insert_many(records)
    print("Data inserted successfully into MongoDB collection `product_category_name_translation`")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the MongoDB connection
    if client:
        client.close()
