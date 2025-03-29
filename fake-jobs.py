import requests # make a request to retrieve the page
from bs4 import BeautifulSoup # html parser
import pandas as pd 
from datetime import date, datetime # to extract datetime object


base_url = "https://realpython.github.io/fake-jobs/"
header= {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
"(KHTML, like Gecko Chrome/133.0.0.0 Safari/537.36"}
response_page = requests.get(base_url,headers=header, timeout=30)

print("connecting...")
if response_page.status_code == 200:
    print("connection successful")
else:
    print("Connection failed!")

# To parse the html page
parsed_page = BeautifulSoup(response_page.text, 'html.parser')
# Extracting all jobs listing
target = parsed_page.find('div', id="ResultsContainer")
job_listing = target.find_all('div', class_="column is-half")

# Scraping and Transformation of unstructured data
fake_jobs_listing=[]
for job in job_listing:
    job_title = job.find('h2', class_="title is-5").text
    company_name = job.find('h3', class_="subtitle is-6 company").text
    location = job.find('p', class_="location").text
    location = " ".join(location.split())
    city = location.split(',',maxsplit=1)[0]
    state = location.split(',',maxsplit=1)[1].strip()
    date_posted = job.find('p', class_="is-small has-text-grey").text
    date_posted =" ".join(date_posted.split())
    date_object = datetime.strptime(date_posted, "%Y-%m-%d")
    date_posted_dmd = date_object.strftime("%A, %#d %B")
    date_posted_yr = date_object.year

    # Finally Transformed data for temporary storage
    jobs_listing = {
        'Job Title': job_title,
        'Company Name': company_name,
        'Location (City)': city,
        'Location (State)': state,
        'Date Posted (Day, Month, Day of Week)': date_posted_dmd,
        'Date Posted (Year)': date_posted_yr,   
    }

    fake_jobs_listing.append(jobs_listing)

fake_job_df = pd.DataFrame(fake_jobs_listing)  # Convert to dataframe
fake_job_df.to_csv("fake_jobs.csv")  # save to csv



    

    