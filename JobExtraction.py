from bs4 import BeautifulSoup
import pandas as pd
import sys

# Get the HTML file path and year from the command-line arguments
if len(sys.argv) < 3:
    print("Usage: python JobExtraction.py <html_file_path> <year>")
    sys.exit(1)

html_file_path = sys.argv[1]
year = sys.argv[2]

# Read the HTML content from the file
with open(html_file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Find all job listings based on the pattern you provided
job_listings = soup.find_all("li", class_="topjob topLine")

# Initialize lists to store extracted data
job_titles = []
locations = []
employers = []
years = []  # To store the year
links = []  # To store the links

# Loop through each job listing and extract the data
for job in job_listings:
    # Extract Job Title
    job_title = job.find("h4").find("a").get_text(strip=True)

    # Extract the link above the job title
    job_link_tag = job.find("h4").find("a")
    job_link = job_link_tag["href"] if job_link_tag and "href" in job_link_tag.attrs else "Not Available"

    # Prepend 'web.archive.org' to the link
    full_job_link = f"https://web.archive.org{job_link}" if job_link != "Not Available" else "Not Available"

    # Extract Location with error handling
    location_tag = job.find("ul", class_="horiz")
    if location_tag:
        location = location_tag.find("li", class_="last")
        if location:
            location = location.find("strong").get_text(strip=True)
        else:
            location = "Not Available"
    else:
        location = "Not Available"

    # Extract Employer with error handling
    employer_tag = job.find("ul", class_="recruiterDetails")
    if employer_tag:
        employer = employer_tag.find("li").get_text(strip=True).replace("Employer: ", "")
    else:
        employer = "Not Available"

    # Append the extracted data to the lists
    job_titles.append(job_title)
    links.append(full_job_link)
    locations.append(location)
    employers.append(employer)
    years.append(year)  # Add the year to the list

# Create a DataFrame using pandas
df = pd.DataFrame({
    "Job Title": job_titles,
    "Job Link": links,  # Include the job link
    "Location": locations,
    "Employer": employers,
    "Year": years
})

# Display the DataFrame
print(df)

# Save the DataFrame to a CSV file
csv_file_path = "nejm_jobs_extracted.csv"
if not pd.io.common.file_exists(csv_file_path):
    df.to_csv(csv_file_path, index=False)  # Write with headers if file doesn't exist
else:
    df.to_csv(csv_file_path, mode='a', header=False, index=False)  # Append if file exists

print(f"Data saved to {csv_file_path}")
