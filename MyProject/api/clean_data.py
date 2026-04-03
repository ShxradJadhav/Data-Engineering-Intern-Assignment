import pandas as pd
import os

# 1. Load the data
# Using 'r' for raw string to avoid path errors on Windows
path = r"C:/Users/User/Desktop/Web_Scrapper_project/jobs_fake_python.csv"
df = pd.read_csv(path)

# 2. Remove exact duplicates
df.drop_duplicates(inplace=True)

# 3. Clean up whitespace (leading/trailing) and normalize text
# We use .astype(str) to prevent errors if there are unexpected numbers
df["title"] = df["title"].astype(str).str.strip().str.lower()
df["company"] = df["company"].astype(str).str.strip()
df["location"] = df["location"].astype(str).str.strip()

# 4. Fill null values 
# Replaces any empty cells with 'Unknown'
df.fillna("Unknown", inplace=True)

# 5. Extract Region (The 2-letter code at the end of the location)
# This looks for two capital letters at the very end of the string
df['region'] = df['location'].str.extract(r'([A-Z]{2})$')

# 6. Final check: Remove any invisible newlines that might break the CSV layout
df = df.replace(r'\n', ' ', regex=True)

# 7. Save the cleaned data
output_dir = "data/clean"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

df.to_csv(f"{output_dir}/jobs_clean.csv", index=False)

# Display the results
print("Cleaning complete! Here is a preview:")
print(df.head())