from flask import Flask,request,url_for,redirect,Response,flash,render_template,json
import sqlite3

app=Flask(__name__)
app.secret_key="secret"

DATABASE="products.db"

def init_db():
    conn=sqlite3.connect(DATABASE)
    c=conn.cursor()
    c.execute('''create table if not exists products(
        product_id integer primary key autoincrement,
        product_name text,
        product_desc text
    )''')
    conn.commit()
    conn.close()

@app.route("/home",methods=["GET"])
def home():
    conn=sqlite3.connect(DATABASE)
    conn.row_factory=sqlite3.Row
    c=conn.cursor()
    c.execute("Select * from products")
    products=c.fetchall()
    conn.close()
    return render_template("index.html",products=products)

@app.route("/add_product",methods=["POST","GET"])
def add_product():
    if request.method=="POST":
        name=request.form["product_name"]
        desc=request.form["product_desc"]
        conn=sqlite3.connect(DATABASE)
        c=conn.cursor()
        c.execute("insert into products(product_name,product_desc) values(?,?)",(name,desc))
        conn.commit()
        conn.close()
        
        flash("Product added")
        return redirect(url_for("home"))
    return render_template("index.html")

@app.route("/product",methods=["POST","GET"])
def product():
    conn=sqlite3.connect(DATABASE)
    conn.row_factory=sqlite3.Row
    c=conn.cursor()
    c.execute("select product_id,product_name from products")
    products=c.fetchall()
    conn.close()
    return json.dumps([dict(product ) for product in products])


if __name__=="__main__":
    init_db()
    app.run(port=5003,debug=True)
    

    