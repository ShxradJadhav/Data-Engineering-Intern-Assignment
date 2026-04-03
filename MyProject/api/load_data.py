import pandas as pd
import mysql.connector

# Load cleaned data
path = "C:\\Users\\User\\Desktop\\Web_Scrapper_project\\data\\clean\\jobs_clean.csv"
df = pd.read_csv(path)

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="CleanDB"
)

cursor = conn.cursor()

# Insert query
query = """
INSERT INTO final_jfp (title, company, location, job_link,  region)
VALUES (%s, %s, %s, %s, %s)
"""

# Insert rows
for index, row in df.iterrows():
    cursor.execute(query, (
        row["title"],
        row["company"],
        row["location"],
        row["job_link"],
        row["region"]
    ))

# Commit changes
conn.commit()

print(cursor.rowcount, "records inserted.")

# Close connection
cursor.close()
conn.close()