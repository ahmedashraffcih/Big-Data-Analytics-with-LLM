# Sales Data Analysis

This repository contains Python code for generating synthetic sales data and performing basic analysis using pandas and numpy libraries.

## Introduction

The provided notebook generates synthetic sales data for a fictional company. 
It randomly generates sales records for different outlets, products, and dates within a specified time period. 
After generating the data, it performs basic analysis to answer questions such as which product has the highest total sales and formatting specific columns.

## Getting Started

To use this notebook, follow these instructions:

1. Make sure you have Python installed on your system.
2. Install the required libraries using pip:
   ```bash
   pip install pandas numpy pandasai

3. Obtain an API key for OpenAI's language model from OpenAI.
   `Replace 'your-key' with your OpenAI API key in the script.`

## Code Explanation
- The script generates synthetic sales data for a specified time period, outlets, and products.
- It calculates total sales for each record based on units sold and price per unit.
- It utilizes the PandasAI library to perform natural language queries on the data.
- It answers questions such as identifying the product with the highest total sales, formatting specific columns and you can also generate charts.