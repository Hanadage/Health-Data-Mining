from bs4 import BeautifulSoup
import pandas as pd

html_file_path = "/Users/hanadage/PycharmProjects/PythonProject/nejm_jobs_full_page.html"

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

# Loop through each job listing and extract the data
for job in job_listings:
    # Extract Job Title
    job_title = job.find("h4").find("a").get_text(strip=True)

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
    locations.append(location)
    employers.append(employer)

# Create a DataFrame using pandas
df = pd.DataFrame({
    "Job Title": job_titles,
    "Location": locations,
    "Employer": employers
})

# Display the DataFrame
print(df)

# Save the DataFrame to a CSV file
csv_file_path = "nejm_jobs_extracted.csv"
df.to_csv(csv_file_path, index=False)

print(f"Data saved to {csv_file_path}")
