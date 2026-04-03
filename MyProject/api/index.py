import os
from fastapi import FastAPI
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS allow karna zaroori hai taaki koi bhi website tera data fetch kar sake
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    # Ye saari details Vercel ke "Environment Variables" settings se aayengi
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT", 3306) # Default port 3306 agar set na ho
    )

@app.get("/")
def home():
    return {"message": "Data Engineering Pipeline API is Live!", "endpoint": "/jobs"}

@app.get("/jobs")
def get_jobs():
    try:
        conn = get_db_connection()
        # dictionary=True se data {'column': 'value'} ke format mein aata hai
        cursor = conn.cursor(dictionary=True)
        
        # SQL query tere table name ke hisaab se (final_jfp)
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
        return {"status": "error", "message": str(e)}

# Vercel ko batane ke liye ki app yahan hai
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
