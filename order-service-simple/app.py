from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import requests
import os

app = Flask(__name__)
app.secret_key = 'supersecret'

DATABASE = 'orders.db'
PRODUCT_SERVICE = "http://localhost:5003"

# Initialize DB
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                customer_name TEXT NOT NULL
            )''')
    conn.commit()
    conn.close()

@app.route("/", methods=['GET'])
def home():
    # Get all orders
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    conn.close()
    
    # Process orders and get product names
    orders_with_products = []
    for order in orders:
        order_dict = dict(order)
        
        # Get product name from product service
        product_response = requests.get(f"{PRODUCT_SERVICE}/product/{order['product_id']}")
        if product_response.status_code == 200:
            product_data = product_response.json()
            order_dict['product_name'] = product_data['name']
        else:
            order_dict['product_name'] = "Unknown Product"
        
        orders_with_products.append(order_dict)
    # Get products for the form
    products = []
    products_response = requests.get(f"{PRODUCT_SERVICE}/products")
    if products_response.status_code == 200:
        products = products_response.json()

    
    return render_template("orders.html", orders=orders_with_products, products=products)

@app.route("/create_order", methods=['POST'])
def create_order():
    product_id = request.form['product_id']
    quantity = request.form['quantity']
    customer_name = request.form['customer_name']
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (product_id, quantity, customer_name) VALUES (?, ?, ?)",
        (product_id, quantity, customer_name)
    )
    conn.commit()
    conn.close()
    
    flash("Order created successfully!")
    return redirect(url_for("home"))

if __name__ == "__main__":
    init_db()
    app.run(port=5002, debug=True)