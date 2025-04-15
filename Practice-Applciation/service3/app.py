from flask import Flask,Response,request,redirect,render_template,url_for,flash,json
import requests
import sqlite3

app=Flask(__name__)
app.secret_key="secret"
DATABASE="orders.db"
PRODUCT="http://localhost:5003"


def init_db():
    conn=sqlite3.connect(DATABASE)
    c=conn.cursor()
    c.execute('''create table if not exists orders(
        order_id integer primary key autoincrement,
        product_id integer,
        quantity integer,
        customer_name text
    )''')
    conn.commit()
    conn.close()
    
    
@app.route("/",methods=["GET"])
def home():
    products=[]
    response=requests.get(f"{PRODUCT}/product")
    if response.status_code==200:
        products=response.json()
        
    return render_template("order.html",products=products)

@app.route("/create_order",methods=["POST","GET"])
def create_order():
    if request.method=="POST":
        product_id=request.form["product_id"]
        qty=request.form["quantity"]
        cusname=request.form["cusname"]
        conn=sqlite3.connect(DATABASE)
        c=conn.cursor()
        c.execute("insert into orders (product_id,quantity,customer_name) values(?,?,?)",(product_id,qty,cusname))
        conn.commit()
        conn.close()
        flash("Inserted order")
        return redirect(url_for("home"))
    
if __name__=="__main__":
    init_db()
    app.run(port=5002,debug=True)
    