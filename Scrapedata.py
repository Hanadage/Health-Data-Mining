import requests
from bs4 import BeautifulSoup
import csv
import subprocess
import os
from tqdm import tqdm
import time
import sys

# Path to the CSV file
csv_file_path = "wayback_links.csv"

# Function to scrape the entire page content
def scrape_entire_page(url, output_file):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch {url} (Status code: {response.status_code})")
            return False

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Save the entire HTML content to a file
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(str(soup))

        print(f"HTML content saved to {output_file}")
        return True
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return False

# Debug: Check the Python executable being used
print(f"Using Python executable: {sys.executable}")

# Read links from the CSV file
with open(csv_file_path, "r", encoding="utf-8") as csv_file:
    reader = csv.reader(csv_file)
    links = [row[0].strip() for row in reader if
             row and row[0].startswith("http") and "#" not in row[0] and "*" not in row[0]]

# Loop through each link and process it
for i, link in enumerate(tqdm(links, desc="Processing links")):
    # Extract the year from the link
    year = link.split("/")[4][:4]

    # Save HTML with a unique name
    html_file = f"page_{year}_{i + 1}.html"

    # Scrape the page and save the HTML
    if scrape_entire_page(link, html_file):
        # Call JobExtraction.py to process the saved HTML
        try:
            subprocess.run(
                [r"C:\Users\justi\PycharmProjects\DataMiningInHealth\.venv\Scripts\python.exe", "JobExtraction.py", html_file, year],
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Error running JobExtraction.py for {html_file}: {e}")

    time.sleep(5)  # Add delay to avoid rate limiting

print("Scraping and extraction complete.")
