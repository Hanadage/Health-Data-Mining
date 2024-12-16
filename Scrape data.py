import requests
from bs4 import BeautifulSoup

# Base URL from Wayback Machine
BASE_URL = "https://web.archive.org/web/20120915002844/https://www.nejmcareercenter.org/jobs/"


# Function to scrape the entire page content
def scrape_entire_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return None

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    return soup


# Scrape the base page
soup = scrape_entire_page(BASE_URL)

if soup:
    # Save the entire HTML content to a file
    with open("nejm_jobs_full_page.html", "w", encoding="utf-8") as file:
        file.write(str(soup))

    print("Scraping complete. HTML saved to 'nejm_jobs_full_page.html'")
else:
    print("Failed to scrape the page.")
