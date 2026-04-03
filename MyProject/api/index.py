import os
from fastapi import FastAPI
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware

# --- YE LINE SABSE ZAROORI HAI (Top-Level) ---
app = FastAPI()

# CORS allow karna zaroori hai
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    # Aiven Cloud MySQL connection using Environment Variables
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 11557))
    )

@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Data Engineering Pipeline API is Live!",
        "endpoint": "/jobs"
    }

@app.get("/jobs")
def get_jobs():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Table name wahi rakhna jo tune database mein banaya hai
        cursor.execute("SELECT * FROM final_jfp LIMIT 100")
        
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return {
            "status": "success",
            "total_records": len(result),
            "data": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
