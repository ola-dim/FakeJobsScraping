import os
import logging
from datetime import datetime # to extract datetime object
import requests # make a request to retrieve the page
from bs4 import BeautifulSoup  # html parser
import pandas as pd


logging.basicConfig(filename=os.path.join('..','logs','bot.log'),
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(messages)s')
logger =logging.getLogger(__name__)

def request_parse(base_url,header):
    logger.info('Making Requests')
    try:
        response_page = requests.get(base_url,headers=header, timeout=30)
        if response_page.status_code == 200:
            logger.info("Connection to %s successful!", base_url)
        else:
            logger.error("Could not connect to %s", base_url)
        parsed_page = BeautifulSoup(response_page.text, 'html.parser')
        return parsed_page
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        print(f"Could not proceed! - {e}")
        logger.info("Could not proceed! - %s", e)
        return None
    

def extract_transform(web_page):
    logger.info('Extracting from web page....')
    jobs = web_page.find_all('div', class_="column is-half")

    fake_jobs_listing=[] # temporary storage

    for job in jobs:
        job_title = job.find('h2', class_="title is-5").text
        company_name = job.find('h3', class_="subtitle is-6 company").text
        location = job.find('p', class_="location").text.strip().split(',')
        city = location[0]
        state = location[1]
        date_posted = job.find('time').text
        date_object = datetime.strptime(date_posted, "%Y-%m-%d")
        date_posted_day = date_object.strftime("%A")
        date_posted_month = date_object.strftime("%#d %B")
        date_posted_year = date_object.year

        jobs_listing = {
        'Job Title': job_title,
        'Company Name': company_name,
        'City': city,
        'State': state,
        'Date_Posted':f"{date_posted_day}, {date_posted_month}",
        'Year': date_posted_year  
        }
        fake_jobs_listing.append(jobs_listing)
        logger.info("Added %s to temporary storage", jobs_listing)
    logger.info("All jobs Extracted and Transformed")
    return fake_jobs_listing

def load_to_file(data,filename="Fake_Jobs_Data"):
    logger.info('Loading data...')
    Fake_jobs_data = pd.DataFrame(data)
    Fake_jobs_data.to_csv(f"{filename}.csv", index=False)
    logger.info('DATA LOADED---Preparing to round up scipts runtime')


def main():
    base_url = "https://realpython.github.io/fake-jobs/"
    header= {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko Chrome/133.0.0.0 Safari/537.36"}
    
    logger.info('Start...')
    page = request_parse(base_url=base_url,header=header)
    jbd = extract_transform(web_page=page)
    load_to_file(jbd)


if __name__ == "__main__":
    main()


