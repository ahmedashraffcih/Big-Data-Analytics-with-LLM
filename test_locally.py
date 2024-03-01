import json 
import time 
import logging
import psycopg2
import threading
import pandas as pd
import numpy as np
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from kafka import KafkaProducer
from kafka import KafkaConsumer
from random import choices


def get_data():
    """
    Fetches random user data from the Random User Generator API and formats it.

    Returns:
        dict: user data.
    """
    import requests

    res = requests.get('https://randomuser.me/api/')
    res = res.json()
    res = res['results'][0]

    return res

def format_data(res):
    """
    Formats raw user data into a structured dictionary.

    Args:
        res (dict): Raw user data.

    Returns:
        dict: Formatted user data.
    """

    data = {}
    location = res['location']
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                      f"{location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']

    return data

def stream_data():
    """
    Continuously fetches and sends formatted user data to a Kafka topic.
    Stops after 1 minute or when an error occurs.
    """
    # Creating Kafka Producer
    producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000)
    curr_time = time.time()
    
    while True: 
        if time.time() > curr_time + 60: #1 minute
            break
        try:
            res = get_data()
            res = format_data(res)
            #Sending data to kafka
            producer.send('users_created', json.dumps(res).encode('utf-8'))
        except Exception as e:
            logging.error(f'An error occured: {e}')
            continue

def load_users_data():
    """
    Consumes user data from a Kafka topic and inserts it into a PostgreSQL table.
    """
    # Establishing connection to SQL Server
    conn = psycopg2.connect(
        dbname='cust_dwh',
        user='postgres',
        password='1234',
        host='localhost',
        port='5432'
    )
    cursor = conn.cursor()

    # Creating Kafka Consumer
    consumer = KafkaConsumer('users_created', bootstrap_servers=['broker:29092'])
    

    # Extracting data fields
    
    # Continuously consume messages from the topic
    for message in consumer:
        try:
            # Decode message value from bytes to string and parse as JSON
            message_data = json.loads(message.value.decode('utf-8'))

            # Extracting data fields
            first_name = message_data['first_name']
            last_name = message_data['last_name']
            gender = message_data['gender']
            address = message_data['address']
            post_code = message_data['post_code']
            email = message_data['email']
            username = message_data['username']
            dob = message_data['dob']
            registered_date = message_data['registered_date']
            phone = message_data['phone']
            picture = message_data['picture']

            # Inserting data into PostgreSQL table
            cursor.execute("INSERT INTO Users (first_name, last_name, gender, address, post_code, email, username, dob, registered_date, phone, picture) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (first_name, last_name, gender, address, post_code, email, username, dob, registered_date, phone, picture))
            conn.commit()
            print("Inserted data:", message_data)
        except Exception as e:
            logging.error(f'An error occurred while processing message: {e}')
            continue

    # Closing PostgreSQL connection
    conn.close()

def generate_dummy_df():
    """
    Generates a dummy DataFrame with simulated sales data.

    Returns:
        DataFrame: Dummy DataFrame with sales data.
    """
    np.random.seed(10)
    
    num_records=1000
    num_outlets=100
    num_products=30

    dates = pd.date_range(start='2023-01-01', end='2023-09-30')
    dates = choices(dates, k=num_records)

    outlets = ['Outlet_'+str(i+1) for i in range(num_outlets)]
    outlets = choices(outlets, k=num_records)

    products = ["Product_"+str(i+1) for i in range(num_products)]
    products = choices(products, k=num_records)

    units_sold = np.random.randint(1, 300, num_records)
    price_per_unit = np.random.uniform(10, 50, num_records)
    total_sales = units_sold * price_per_unit

    df = pd.DataFrame({
        'Date': dates,
        'outlets' : outlets,
        'Products' : products,
        'Unit_sold': units_sold,
        'Price_Per_Unit': price_per_unit,
        'Total_Sales' : total_sales
    })
    return df

def produce_messages_from_df(df):
    '''
    Produces JSON messages from DataFrame rows to a Kafka topic.
    Introduces a 1-second delay between messages.

    Args:
        df (DataFrame): Input DataFrame.
    '''
    # Convert DataFrame rows to JSON format
    messages = df.to_dict(orient='records')
    
    # Convert Timestamp objects to string representations
    for message in messages:
        message['Date'] = str(message['Date'])

    # Creating Kafka Producer
    producer = KafkaProducer(bootstrap_servers=['broker:29092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    for message in messages:
        # Convert Timestamp object to string representation
        message['Date'] = str(message['Date'])
        
        # Sending data to Kafka
        producer.send('products', message)
        time.sleep(0.1)  # Introduce a delay of 1 second between each message to simulate streaming from file

# Function to consume product data from Kafka and insert it into PostgreSQL   
def load_products_data():
    """
    Consumes product data from a Kafka topic and inserts it into a PostgreSQL database.
    """
    # Establishing connection to PG
    conn = psycopg2.connect(
        dbname='db_name',
        user='user',
        password='password',
        host='host',
        port='5432'
    )
    cursor = conn.cursor()

    # Creating Kafka Consumer
    consumer = KafkaConsumer('products', bootstrap_servers=['broker:29092'])
    
    # Extracting data fields
    
    # Continuously consume messages from the topic
    for message in consumer:
        try:
            # Decode message value from bytes to string and parse as JSON
            message_data = json.loads(message.value.decode('utf-8'))

            # Extracting data fields and perform any necessary transformations

            # Inserting data into PostgreSQL table
            cursor.execute("INSERT INTO sales_data (date, outlets, products, unit_sold, price_per_Unit, total_Sales) VALUES (%s, %s, %s, %s, %s, %s)",
                           (message_data['Date'], message_data['outlets'], message_data['Products'], message_data['Unit_sold'], message_data['Price_Per_Unit'], message_data['Total_Sales']))
            conn.commit()
            print("Inserted data:", message_data)
        except Exception as e:
            logging.error(f'An error occurred while processing message: {e}')
            continue

    # Closing PostgreSQL connection
    conn.close()



# Main function to run producer and consumer
if __name__ == "__main__":
    # Start the producers in a separate threads
    producer_thread_1 = threading.Thread(target=stream_data)
    producer_thread_1.daemon = True
    producer_thread_1.start()

    df = generate_dummy_df()
    producer_thread_2 = threading.Thread(target=produce_messages_from_df, args=(df,))
    producer_thread_2.daemon = True
    producer_thread_2.start()

    # Start the consumers in separate threads
    consumer_thread_1 = threading.Thread(target=load_users_data)
    consumer_thread_1.start()

    consumer_thread_2 = threading.Thread(target=load_products_data)
    consumer_thread_2.start() 