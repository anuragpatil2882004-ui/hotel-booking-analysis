import hashlib
import os
import psycopg2
import psycopg2.extras
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Make app available for Vercel as the handler
handler = app

DB_URL = os.environ.get("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DB_URL, cursor_factory=psycopg2.extras.RealDictCursor)

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

@app.route("/api/register", methods=["POST", "OPTIONS"])
def register():
    if request.method == "OPTIONS":
        return "", 200
    data = request.json or {}
    required = ["hotelName","hotelType","starRating","acType","hotelLocation","ownerName","email","password"]
    for f in required:
        if not data.get(f):
            return jsonify({"error": f"Missing field: {f}"}), 400
    
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO hotels (hotel_name, hotel_type, star_rating, ac_type, hotel_location,
               total_rooms, owner_name, email, phone, password_hash)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (data["hotelName"], data["hotelType"], data["starRating"],
              data["acType"], data["hotelLocation"], data.get("totalRooms"),
              data["ownerName"], data["email"], data.get("phone",""),
              hash_password(data["password"])))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Registration successful"}), 201
    except psycopg2.errors.UniqueViolation:
        return jsonify({"error": "Email already registered"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return "", 200
    data = request.json or {}
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM hotels WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if not user or user["password_hash"] != hash_password(password):
            return jsonify({"error": "Invalid email or password"}), 401
        
        return jsonify({
            "message": "Login successful",
            "hotelName": user["hotel_name"],
            "hotelType": user["hotel_type"],
            "starRating": user["star_rating"],
            "acType": user["ac_type"],
            "hotelLocation": user["hotel_location"],
            "ownerName": user["owner_name"],
            "email": user["email"],
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500