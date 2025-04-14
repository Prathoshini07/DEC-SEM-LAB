from flask import Flask, request, redirect, Response
import requests

app = Flask(__name__)
AUTH_SERVICE = "http://localhost:5001"
ORDER_SERVICE = "http://localhost:5002"
PRODUCT_SERVICE = "http://localhost:5003"


@app.route("/", methods=["GET"])
def home():
    print("Hit API gateway /")
    response = requests.get(f"{AUTH_SERVICE}/home")
    print("Auth-service responded with", response.status_code)
    return Response(response.content, status=response.status_code, headers=dict(response.headers))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        response = requests.post(f"{AUTH_SERVICE}/login", data=request.form)
    else:
        response = requests.get(f"{AUTH_SERVICE}/login")
    return Response(response.content, status=response.status_code, headers=dict(response.headers))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        response = requests.post(f"{AUTH_SERVICE}/register", data=request.form)
    else:
        response = requests.get(f"{AUTH_SERVICE}/register")
    return Response(response.content, status=response.status_code, headers=dict(response.headers))

@app.route("/products", methods=["GET"])
def products():
    response = requests.get(f"{PRODUCT_SERVICE}/")
    return Response(response.content, status=response.status_code, headers=dict(response.headers))

@app.route("/add_product", methods=["POST"])
def add_product():
    response = requests.post(f"{PRODUCT_SERVICE}/add_product", data=request.form)
    return Response(response.content, status=response.status_code, headers=dict(response.headers))

@app.route("/delete_product", methods=["POST"])
def delete_product():
    response = requests.post(f"{PRODUCT_SERVICE}/delete_product", data=request.form)
    return Response(response.content, status=response.status_code, headers=dict(response.headers))

@app.route("/edit_product", methods=["POST"])
def edit_product():
    response = requests.post(f"{PRODUCT_SERVICE}/edit_product", data=request.form)
    return Response(response.content, status=response.status_code, headers=dict(response.headers))
# Order service routes
@app.route("/orders", methods=["GET"])
def orders():
    response = requests.get(f"{ORDER_SERVICE}")
    return Response(response.content, status=response.status_code, headers=dict(response.headers))

@app.route("/create_order", methods=["GET", "POST"])
def create_order():
    if request.method == "POST":
        response = requests.post(f"{ORDER_SERVICE}/create_order", data=request.form)
    else:
        response = requests.get(f"{ORDER_SERVICE}/create_order")
    return Response(response.content, status=response.status_code, headers=dict(response.headers))

@app.route("/update_order_status/<order_id>", methods=["POST"])
def update_order_status(order_id):
    response = requests.post(f"{ORDER_SERVICE}/update_order_status/{order_id}", data=request.form)
    return Response(response.content, status=response.status_code, headers=dict(response.headers))

@app.route("/cancel_order/<order_id>", methods=["POST"])
def cancel_order(order_id):
    response = requests.post(f"{ORDER_SERVICE}/cancel_order/{order_id}")
    return Response(response.content, status=response.status_code, headers=dict(response.headers))
if __name__ == "__main__":
    app.run(port=5000)