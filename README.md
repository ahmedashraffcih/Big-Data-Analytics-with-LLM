# Real-time Data Streaming Pipeline | Data Analytics With LLM

## 🪄 Introduction

This project serves as a comprehensive guide to building an end-to-end data engineering pipeline. 
It covers each stage from data ingestion to processing and finally to storage, utilizing a robust tech stack that includes Apache Airflow, Python, Apache Kafka, Apache Zookeeper, and Posgres. 
Everything is containerized using Docker for ease of deployment and scalability.

Upon completing the pipeline, we will proceed with data analysis using LLM models leveraging the PandasAI library.
The provided notebook generates synthetic sales data for a fictional company. 
It randomly generates sales records for different outlets, products, and dates within a specified time period. 
After generating the data, it performs basic analysis to answer questions such as which product has the highest total sales and do some plot chart, and you can do many more with it.

## ⚡ System Architecture

![System Architecture](https://github.com/ahmedashraffcih/Big-Data-Analytics-with-LLM/blob/main/imgs/newboard.png)

The project is designed with the following components:

- **Data Source**: We use `randomuser.me` API to generate random user data for our pipeline and a python dataframe with dummy data.
- **Apache Airflow**: Responsible for orchestrating the pipeline and storing fetched data in a PostgreSQL database.
- **Apache Kafka and Zookeeper**: Used for streaming data from directly to postgres.
- **Control Center and Schema Registry**: Helps in monitoring and schema management of our Kafka streams.
- **Postgres**: Where the processed data will be stored.
- **LLM**: Used for data analytics
---

## Features
- Real-time streaming of user data from a public API to Kafka topics.
- Parsing and formatting of user data before insertion into a PostgreSQL database.
- Generation of simulated sales data and publishing to a Kafka topic.
- Consumption of data from Kafka topics and insertion into PostgreSQL tables.
- Perform data analytics and visualization using LLM

---


## 💿 Getting Started

1. Clone the repository:
    ```bash
    git clone https://github.com/ahmedashraffcih/Big-Data-Analytics-with-LLM.git
    ```

2. Navigate to the project directory:
    ```bash
    cd Big-Data-Analytics-with-LLM
    ```

3. Run Docker Compose to spin up the services:
    ```bash
    docker-compose up
    ```
`Note that sequential executor will not work with the current DAG`

To use this notebook, follow these instructions:

1. Make sure you have Python installed on your system.
2. Install the required libraries using pip:
   ```bash
   pip install pandas numpy pandasai

3. Obtain an API key for OpenAI's language model from OpenAI.
   `Replace 'your-key' with your OpenAI API key in the script.`

---
## Examples
![Users Topic](https://github.com/ahmedashraffcih/Big-Data-Analytics-with-LLM/blob/main/imgs/users_topic.png)
![Products Topic](https://github.com/ahmedashraffcih/Big-Data-Analytics-with-LLM/blob/main/imgs/products_topic.png)
![Products Sink](https://github.com/ahmedashraffcih/Big-Data-Analytics-with-LLM/blob/main/imgs/products_sink.png)
![Airflow Dag](https://github.com/ahmedashraffcih/Big-Data-Analytics-with-LLM/blob/main/imgs/dag.png)
---

## ✨ Contribution

Contributions and feedback are welcome! If you have any ideas, suggestions, or improvements, feel free to open an issue or submit a pull request.


To contribute to this project, see the GitHub documentation on **[creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request)**.

---

## 👏 Support

Give a ⭐️ if you like this project!
___________________________________

<p>&copy; 2024 Ahmed Ashraf</p>

