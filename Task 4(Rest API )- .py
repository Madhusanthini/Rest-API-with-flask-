from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# TEMP "database"
users = {}
students = []

# HOME ROUTE
@app.route("/")
def home():
    return "Flask API is working!"

#REGISTER
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username in users:
        return jsonify({"error": "User already exists!"}), 400

    hashed = generate_password_hash(password)
    users[username] = hashed

    return jsonify({"message": "User registered successfully!"})

#LOGIN
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username not in users:
        return jsonify({"error": "Invalid username"}), 400

    if not check_password_hash(users[username], password):
        return jsonify({"error": "Wrong password!"}), 400

    return jsonify({"message": "Login success!"})

# GET STUDENTS 
@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(students)

#ADD STUDENT
@app.route("/students", methods=["POST"])
def add_student():
    data = request.json
    students.append(data)
    return jsonify({"message": "Student Added", "data": data})

#DELETE STUDENT
@app.route("/students/<int:index>", methods=["DELETE"])
def delete_student(index):
    if index >= len(students):
        return jsonify({"error": "Not found"}), 404
    
    students.pop(index)
    return jsonify({"message": "Deleted"})


if __name__ == "__main__":
    app.run(debug=True)