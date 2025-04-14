from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3
app=Flask(__name__)
app.secret_key='supersecret'
def init_db():
    conn=sqlite3.connect("auth.db")      
    c=conn.cursor()
    c.execute('''Create table if not exists users(
        id integer primary key autoincrement,
        username text,
        password text
    )''')
    conn.commit()
    conn.close()
    
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        
        conn=sqlite3.connect("auth.db")
        c=conn.cursor()
        c.execute("select * from users where username=? and password=?",(username,password))
        user=c.fetchone()
        conn.close()
        if user:
            return "Login successfull"
        else:
            flash("Invalid")
            return redirect(url_for("login"))
    return render_template("login.html")
        
        

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        
        conn=sqlite3.connect("auth.db")
        c=conn.cursor()
        c.execute("insert into users(username,password) values(?,?)",(username,password))
        conn.commit()
        conn.close()
        flash("Successfully registered")
        return redirect(url_for("login"))
    return render_template("register.html")

if __name__=="__main__":
    init_db()
    app.run(port=5001,debug=True)
    


