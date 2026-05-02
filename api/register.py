import hashlib
import os
from http.server import BaseHTTPRequestHandler
import psycopg2
import psycopg2.extras
import json

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
        required = ["hotelName","hotelType","starRating","acType","hotelLocation","ownerName","email","password"]
        for f in required:
            if not body.get(f):
                return {"statusCode": 400, "body": json.dumps({"error": f"Missing field: {f}"})}
        
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO hotels
              (hotel_name, hotel_type, star_rating, ac_type, hotel_location,
               total_rooms, owner_name, email, phone, password_hash)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            body["hotelName"], body["hotelType"], body["starRating"],
            body["acType"], body["hotelLocation"], body.get("totalRooms"),
            body["ownerName"], body["email"], body.get("phone",""),
            hash_password(body["password"])
        ))
        conn.commit()
        cur.close()
        conn.close()
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"message": "Registration successful"})
        }
    except psycopg2.errors.UniqueViolation:
        return {"statusCode": 409, "body": json.dumps({"error": "Email already registered"})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}