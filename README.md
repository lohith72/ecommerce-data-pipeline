# E-Commerce Data Pipeline Using Python and MySQL

## About the Project

I built this project to practise how data moves from a raw source into a database that can be used for analysis.

I started with an Excel dataset containing over 10,000 e-commerce order records. While exploring the data, I found issues such as duplicate rows, missing values, inconsistent region names, and invalid quantities and discounts.

I used Python and Pandas to clean and validate the data. Instead of simply deleting every problematic record, I also created a quarantine file to keep track of rejected records and the reasons they were rejected.

After cleaning the data, I loaded it into MySQL and wrote SQL queries to explore order statuses, payment information, products, customers, and order values. I also added automated tests to check that the cleaned data meets the expected quality rules.

## What I Built

- An extraction script to read and inspect the source Excel data.
- A transformation script to clean the data and separate invalid records.
- A MySQL loading script that reads database credentials from a local environment file.
- A pipeline runner that executes each stage in sequence.
- Automated data-quality tests using Pytest.
- SQL queries for exploring the cleaned e-commerce data.

## Results So Far

- Started with 10,035 records.
- Produced 10,020 clean records.
- Quarantined 10 records with data-quality issues.
- Loaded 10,020 records into MySQL.
- Passed all 7 automated tests in the latest pipeline run.

This project helped me practise handling real-world data-quality problems, structuring a small ETL pipeline, and checking that the data remains consistent from extraction through to loading.