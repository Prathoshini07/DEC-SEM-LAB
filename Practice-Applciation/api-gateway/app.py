from flask import Flask,Response,request,redirect
import requests

app=Flask(__name__)
AUTH_SERVICE="http://localhost:5001"

@app.route("/",methods=["GET"])
def home():
    response=requests.get(f"{AUTH_SERVICE}/home")
    return Response(response.content,status=response.status_code,headers=dict(response.headers))

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=='POST':
        response=requests.post(f"{AUTH_SERVICE}/login",data=request.form)
    else:
        response=requests.get(f"{AUTH_SERVICE}/login")
    return Response(response.content,status=response.status_code,headers=dict(response.headers))

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        response=requests.post(f"{AUTH_SERVICE}/register",data=request.form)
    else:
        response=requests.get(f"{AUTH_SERVICE}/register")
    return Response(response.content,status=response.status_code,headers=dict(response.headers))

if __name__=="__main__":
    app.run(port=5000,debug=True)