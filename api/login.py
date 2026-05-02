import hashlib
import os
import json
import psycopg2
import psycopg2.extras

DB_URL = os.environ.get("DATABASE_URL", "postgres://user:password@localhost:5432/hoteldb?sslmode=require")

def get_conn():
    return psycopg2.connect(DB_URL, cursor_factory=psycopg2.extras.RealDictCursor)

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def handler(request):
    method = request.method
    
    if method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "POST,OPTIONS", "Access-Control-Allow-Headers": "Content-Type"},
            "body": ""
        }
    
    if method != "POST":
        return {"statusCode": 405, "body": json.dumps({"error": "Method not allowed"})}
    
    try:
        body = json.loads(request.body) if isinstance(request.body, str) else request.body
        email = body.get("email")
        password = body.get("password")
        
        if not email or not password:
            return {"statusCode": 400, "body": json.dumps({"error": "Email and password required"})}
        
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM hotels WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if not user or user["password_hash"] != hash_password(password):
            return {"statusCode": 401, "body": json.dumps({"error": "Invalid email or password"})}
        
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({
                "message": "Login successful",
                "hotelName": user["hotel_name"],
                "hotelType": user["hotel_type"],
                "starRating": user["star_rating"],
                "acType": user["ac_type"],
                "hotelLocation": user["hotel_location"],
                "ownerName": user["owner_name"],
                "email": user["email"],
            })
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}