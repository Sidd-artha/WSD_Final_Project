from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
import sqlite3

app = FastAPI()

# Models for Customer, Item, and Order data
class Customer(BaseModel):
    name: str
    phone: str

class Item(BaseModel):
    name: str
    price: float

class Order(BaseModel):
    customer_id: int
    item_id: int
    notes: str
    timestamp: int

# Helper function to establish a database connection
def establish_db_connection():
    database_connection = sqlite3.connect('db.sqlite', timeout=30, check_same_thread=False)
    database_connection.row_factory = sqlite3.Row
    return database_connection

# Endpoint to create a new customer
@app.post("/customers")
def add_customer(customer: Customer, conn: sqlite3.Connection = Depends(establish_db_connection)):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (customer.name, customer.phone))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Customer with the same name and phone already exists")
    except sqlite3.OperationalError as error:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(error)}")
    finally:
        conn.close()

    return {"message": "Customer created successfully"}

# Endpoint to retrieve a specific customer by ID
@app.get("/customers/{id}")
def retrieve_customer(id: int, conn: sqlite3.Connection = Depends(establish_db_connection)):
    cursor = conn.cursor()
    try:
        result = cursor.execute("SELECT * FROM customers WHERE id = ?", (id,)).fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Customer not found")
        return dict(result)
    except sqlite3.OperationalError as error:
        raise HTTPException(status_code=500, detail=f"Database error: {str(error)}")
    finally:
        conn.close()

@app.get("/all_customers")
def retrieve_all_customers(conn: sqlite3.Connection = Depends(establish_db_connection)):
    cursor = conn.cursor()
    try:
        results = cursor.execute("SELECT * FROM customers").fetchall()
        if not results:
            raise HTTPException(status_code=404, detail="No customers found")
        return {row["id"]: {"name": row["name"], "phone": row["phone"]} for row in results}
    except sqlite3.OperationalError as error:
        raise HTTPException(status_code=500, detail=f"Database error: {str(error)}")
    finally:
        conn.close()

@app.put("/customers/{id}")
def modify_customer(id: int, customer: Customer, conn: sqlite3.Connection = Depends(establish_db_connection)):
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE customers SET name = ?, phone = ? WHERE id = ?", (customer.name, customer.phone, id))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Customer not found")
    except sqlite3.OperationalError as error:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(error)}")
    finally:
        conn.close()

    return {"message": "Customer updated successfully"}

@app.delete("/customers/{id}")
def remove_customer(id: int, conn: sqlite3.Connection = Depends(establish_db_connection)):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM customers WHERE id = ?", (id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Customer not found")
    except sqlite3.OperationalError as error:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(error)}")
    finally:
        conn.close()

    return {"message": "Customer deleted successfully"}

@app.post("/items")
def add_item(item: Item, conn: sqlite3.Connection = Depends(establish_db_connection)):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", (item.name, item.price))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Item already exists")
    except sqlite3.OperationalError as error:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(error)}")
    finally:
        conn.close()

    return {"message": "Item created successfully"}

@app.get("/items/{id}")
def retrieve_item(id: int, conn: sqlite3.Connection = Depends(establish_db_connection)):
    cursor = conn.cursor()
    try:
        result = cursor.execute("SELECT * FROM items WHERE id = ?", (id,)).fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Item not found")
        return dict(result)
    except sqlite3.OperationalError as error:
        raise HTTPException(status_code=500, detail=f"Database error: {str(error)}")
    finally:
        conn.close()

@app.put("/items/{id}")
def modify_item(id: int, item: Item, conn: sqlite3.Connection = Depends(establish_db_connection)):
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE items SET name = ?, price = ? WHERE id = ?", (item.name, item.price, id))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item not found")
    except sqlite3.OperationalError as error:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(error)}")
    finally:
        conn.close()

    return {"message": "Item updated successfully"}

@app.delete("/items/{id}")
def remove_item(id: int, conn: sqlite3.Connection = Depends(establish_db_connection)):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM items WHERE id = ?", (id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item not found")
    except sqlite3.OperationalError as error:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(error)}")
    finally:
        conn.close()

    return {"message": "Item deleted successfully"}

@app.post("/orders")
def add_order(order: Order, conn: sqlite3.Connection = Depends(establish_db_connection)):
    cursor = conn.cursor()
    if not order.timestamp:
        order.timestamp = int(datetime.utcnow().timestamp())
    try:
        cursor.execute("INSERT INTO orders (customer_id, item_id, notes, timestamp) VALUES (?, ?, ?, ?)",
                       (order.customer_id, order.item_id, order.notes, order.timestamp))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Order already exists")
    except sqlite3.OperationalError as error:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(error)}")
    finally:
        conn.close()

    return {"message": "Order created successfully"}

@app.get("/orders/{id}")
def retrieve_order(id: int, conn: sqlite3.Connection = Depends(establish_db_connection)):
    cursor = conn.cursor()
    try:
        result = cursor.execute("SELECT * FROM orders WHERE id = ?", (id,)).fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Order not found")
        return dict(result)
    except sqlite3.OperationalError as error:
        raise HTTPException(status_code=500, detail=f"Database error: {str(error)}")
    finally:
        conn.close()

@app.put("/orders/{id}")
def modify_order(id: int, order: Order, conn: sqlite3.Connection = Depends(establish_db_connection)):
    cursor = conn.cursor()
    if not order.timestamp:
        order.timestamp = int(datetime.utcnow().timestamp())
    try:
        cursor.execute("UPDATE orders SET customer_id = ?, item_id = ?, notes = ?, timestamp = ? WHERE id = ?",
                       (order.customer_id, order.item_id, order.notes, order.timestamp, id))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Order not found")
    except sqlite3.OperationalError as error:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(error)}")
    finally:
        conn.close()

    return {"message": "Order updated successfully"}

@app.delete("/orders/{id}")
def remove_order(id: int, conn: sqlite3.Connection = Depends(establish_db_connection)):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM orders WHERE id = ?", (id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Order not found")
    except sqlite3.OperationalError as error:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(error)}")
    finally:
        conn.close()

    return {"message": "Order deleted successfully"}
