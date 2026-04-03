import requests
from bs4 import BeautifulSoup
import pandas as pd

jobs = []

base_url = "https://realpython.github.io/fake-jobs/"

response = requests.get(base_url)
soup = BeautifulSoup(response.text, "html.parser")

listings = soup.find_all("div", class_="card-content")

for job in listings:

    title = job.find("h2", class_="title")
    company = job.find("h3", class_="company")
    location = job.find("p", class_="location")
    link = job.find("a")

    jobs.append({
        "title": title.text.strip() if title else None,
        "company": company.text.strip() if company else None,
        "location": location.text.strip() if location else None,
        "job_link": link["href"] if link else None
    })

df = pd.DataFrame(jobs)

df.to_csv("jobs_fake_python.csv", index=False)

print("Data saved successfully")