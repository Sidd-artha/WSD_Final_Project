# WSD_Final_Project

This project is designed to set up and manage a customer order database using a JSON file (structured similarly to `examples_orders.json`) and provides endpoints for performing CRUD (Create, Read, Update, Delete) operations via FastAPI.

## Database Structure

The project uses a SQLite database with the following three tables:

### 1. Customers Table
Stores details about individual customers:
- `id`: Auto-incremented unique identifier.
- `name`: The customer's name (required, cannot be null).
- `phone`: The customer's phone number (required, cannot be null).
- **Unique Constraint**: Combination of `name` and `phone` must be unique.

### 2. Items Table
Contains information about items available for purchase:
- `id`: Auto-incremented unique identifier.
- `name`: The item's name (required, unique).
- `price`: The item's price (required).

### 3. Orders Table
Records all orders placed by customers:
- `id`: Auto-incremented unique identifier.
- `customer_id`: References the `id` in the `customers` table.
- `item_id`: References the `id` in the `items` table.
- `notes`: Optional field for additional details about the order.
- `timestamp`: Represents the time of the order. Defaults to the current timestamp if not provided.

---

## Features
- **Auto-Increment IDs**: Unique primary keys are auto-generated for all tables.
- **Referential Integrity**: Foreign keys in the `orders` table link to the `customers` and `items` tables to maintain data consistency.
- **Default Timestamp**: Automatically uses the current timestamp for orders if no timestamp is provided.
- **Unique Constraints**: 
  - The `name` field in the `items` table ensures no duplicate items.
  - The combination of `name` and `phone` in the `customers` table prevents duplicate customer entries.

---

## Setup Instructions

### 1. Initialize the Database

python init_db.py

### To run the API's

uvicorn main:app --reload

Use the http://127.0.0.1:8000/docs link to test the API's