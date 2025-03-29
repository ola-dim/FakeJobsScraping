# webscraping_data_extraction
Data engineering project on web scraping and data extraction.
 A Python script that scrapes job data from the provided website and organizes it into a structured format.
## Web Scraping Process
The following were the steps taken to gather data from [Fake Jobs website](https://realpython.github.io/fake-jobs/):

* Get the URL.
* connect using the `requests` module.
* Parse the html page and extract using `Beautifulsoup`.
* Scrape and Transform the unstructured data.
* Load the data.


## Instructions
The following are the instructions on how to run the script:

* Check the `requirements.txt` for the required dependencies.
* Clone the Repository.
* Create a Virtual Enviroment (Optional but Recommended).
* Install Dependencies.
* Run the Script
* Troubleshooting:

    * if running on windows and encountering datetime format issues, replace `%-d ` with `%#d`.