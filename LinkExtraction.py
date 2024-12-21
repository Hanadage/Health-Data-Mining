from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
import time

# Initialize Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run browser in headless mode (no GUI)
options.add_argument('--disable-gpu')  # Disable GPU for headless mode

# Set up the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Wayback Machine snapshot URL
wayback_url = "https://web.archive.org/web/20131215000000*/https://www.nejmcareercenter.org/jobs/"

# Open the Wayback Machine snapshot
driver.get(wayback_url)

# Wait for the page to load fully
time.sleep(5)

# Filter and collect relevant links
filtered_links = [    "https://web.archive.org/web/20120901000000*/https://www.nejmcareercenter.org/jobs/",
    "https://web.archive.org/web/20130501000000*/https://www.nejmcareercenter.org/jobs/",
    "https://web.archive.org/web/20140401000000*/https://www.nejmcareercenter.org/jobs/",
    "https://web.archive.org/web/20160515000000*/https://www.nejmcareercenter.org/jobs/",
    "https://web.archive.org/web/20170315000000*/https://www.nejmcareercenter.org/jobs/",
    "https://web.archive.org/web/20180401000000*/https://www.nejmcareercenter.org/jobs/",
    "https://web.archive.org/web/20190301000000*/https://www.nejmcareercenter.org/jobs/",
    "https://web.archive.org/web/20201101000000*/https://www.nejmcareercenter.org/jobs/",
    "https://web.archive.org/web/20211001000000*/https://www.nejmcareercenter.org/jobs/",
    "https://web.archive.org/web/20220501000000*/https://www.nejmcareercenter.org/jobs/",
    "https://web.archive.org/web/20230501000000*/https://www.nejmcareercenter.org/jobs/",
    "https://web.archive.org/web/20240401000000*/https://www.nejmcareercenter.org/jobs/"]

# Print the filtered links
for fl in tqdm(filtered_links, desc="Processing filtered links"):
    print(f"Opening link: {fl}")
    try:
        driver.get(fl)
        time.sleep(5)  # Allow the page to load
        sub_links = driver.find_elements(By.TAG_NAME, 'a')
        for sub_link in sub_links:
            sub_href = sub_link.get_attribute('href')
            if sub_href and "web.archive.org" in sub_href and any(char.isdigit() for char in sub_href):
                print(sub_href)
    except Exception as e:
        print(f"Failed to process link {fl}: {e}")

# Close the browser
driver.quit()
