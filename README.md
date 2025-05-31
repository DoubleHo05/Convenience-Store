# Convenience Store
A DE project which uses Python to build, generate and extract data for a MySQL database of a small convenience store

## Prerequisites
- Python 3.11+
- MySQL Server

## Features
- SQL code for creating tables.
- Creating sample data using Python.
- Add sample data from Python to the database.
- Python code for extracting the data daily.

## Requirements
- Python 3.x
- MySQL 5.x 
- `mysql-connector-python` library
- `Faker` library for generating fake data

## Documentation: [Check my documentation here](https://docs.google.com/document/d/1Vjy4Qsx-DsaLgSjiEALoNJPPyocEA90FyKWRs5tjWQc/edit?tab=t.4je3qo5c3r6d)

## How to run the project with Docker
- Step 1: Clone this repo: git clone https://github.com/DoubleHo05/Convenience-Store
- Step 2: Run this in terminal: docker compose up (There will be "extracted" folder in your working directory which contains csv files with data from the database)