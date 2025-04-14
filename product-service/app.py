from flask import Flask, render_template, request, redirect, url_for, flash,json
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'supersecret'

DATABASE = 'products.db'

# Initialize DB
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            )''')
    conn.commit()
    conn.close()


@app.route("/")
def home():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template("index.html", products=products)

@app.route("/add_product", methods=['POST'])
def add_product():
    name = request.form['name']
    description = request.form['description']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, description) VALUES (?, ?)", (name, description))
    conn.commit()
    conn.close()

    flash("Product added successfully!")
    return redirect(url_for("home"))

@app.route("/delete_product", methods=['POST'])
def delete_product():
    product_id = request.form['id']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

    flash("Product deleted successfully!")
    return redirect(url_for("home"))

@app.route("/edit_product", methods=['POST'])
def edit_product():
    product_id = request.form['id']
    name = request.form['name']
    description = request.form['description']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET name = ?, description = ? WHERE id = ?", (name, description, product_id))
    conn.commit()
    conn.close()

    flash("Product updated successfully!")
    return redirect(url_for("home"))
# Add these routes to your product service app.py

@app.route("/product/<int:product_id>", methods=['GET'])
def product_details(product_id):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    
    if product:
        return json.dumps(dict(product))
    else:
        return "Product not found", 404
    
if __name__ == "__main__":
    init_db()
    app.run(port=5003, debug=True)