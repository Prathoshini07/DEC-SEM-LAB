from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import requests
import json
import re

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
                customer_name TEXT NOT NULL,
                status TEXT DEFAULT 'pending'
            )''')
    conn.commit()
    conn.close()

@app.route("/")
def home():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    conn.close()
    
    # Fetch product details for each order
    orders_with_products = []
    for order in orders:
        order_dict = dict(order)
        try:
            product_response = requests.get(f"{PRODUCT_SERVICE}/product/{order['product_id']}")
            if product_response.status_code == 200:
                product = product_response.json()
                order_dict['product_name'] = product['name']
            else:
                order_dict['product_name'] = "Unknown Product"
        except:
            order_dict['product_name'] = "Error fetching product"
        
        orders_with_products.append(order_dict)
    
    return render_template("orders_index.html", orders=orders_with_products)

@app.route("/create_order", methods=['GET', 'POST'])
def create_order():
    if request.method == 'POST':
        product_id = request.form['product_id']
        quantity = request.form['quantity']
        customer_name = request.form['customer_name']
        
        # Verify product exists
        try:
            product_response = requests.get(f"{PRODUCT_SERVICE}/product/{product_id}")
            if product_response.status_code != 200:
                flash("Product does not exist!")
                return redirect(url_for("create_order"))
                
            # Product exists, create order
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
        except Exception as e:
            flash(f"Error verifying product: {str(e)}")
            return redirect(url_for("create_order"))
    
    # For GET request, fetch all products to populate dropdown
    try:
        # Ask the product service for JSON instead of HTML
        products_response = requests.get(f"{PRODUCT_SERVICE}/products_json")
        if products_response.status_code == 200:
            # Use the JSON API endpoint directly
            products = products_response.json()
        else:
            # Fallback to parsing the HTML response if JSON endpoint isn't available
            products_html_response = requests.get(f"{PRODUCT_SERVICE}/")
            if products_html_response.status_code == 200:
                html_content = products_html_response.text
                # Simple regex pattern to extract product IDs and names
                # This is a basic approach and might not work for all HTML structures
                products = []
                product_items = re.findall(r'<div class="product-item">(.*?)</div>', html_content, re.DOTALL)
                for item in product_items:
                    id_match = re.search(r'ID: (\d+)', item)
                    name_match = re.search(r'<strong>(.*?)</strong>', item)
                    if id_match and name_match:
                        product_id = id_match.group(1)
                        product_name = name_match.group(1)
                        products.append({'id': product_id, 'name': product_name})
            else:
                products = []
    except Exception as e:
        print(f"Error fetching products: {str(e)}")
        products = []
    
    return render_template("create_order.html", products=products)

@app.route("/update_order_status/<int:order_id>", methods=['POST'])
def update_order_status(order_id):
    status = request.form['status']
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
    conn.commit()
    conn.close()
    
    flash("Order status updated successfully!")
    return redirect(url_for("home"))

@app.route("/cancel_order/<int:order_id>", methods=['POST'])
def cancel_order(order_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = 'cancelled' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()
    
    flash("Order cancelled successfully!")
    return redirect(url_for("home"))

@app.route("/product/<int:product_id>", methods=['GET'])
def product_details(product_id):
    # This is a convenience method to get product details
    try:
        response = requests.get(f"{PRODUCT_SERVICE}/product/{product_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Product not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    init_db()
    app.run(port=5002, debug=True)