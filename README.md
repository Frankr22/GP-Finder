# GP-Finder: Evaluate & Select GPs in Your Area

A personal project to evaluate General Practitioners (GPs) available in a specific area through the NHS website, making it easier to select a suitable GP.

## Project Overview

This project aims to:
- Scrape data from the NHS website about available GPs in a specific area
- Store the data in a SQL database
- Perform data analysis using Python and SQL
- Visualize findings using PowerBI

## Technologies Used

- Python
- SQL
- PowerBI
- BeautifulSoup (for Web Scraping)

## How it Works

### 1. Data Collection

- Use Python libraries like `BeautifulSoup` or `Scrapy` to scrape data about available GP surgeries.
  - Data to scrape: GP Name, Accepting Patients (Y/N), Opening Times, Reviews

### 2. Data Storage

- Store the scraped data in a SQL database.

### 3. Data Analysis

- Use Python (`Pandas`) for data cleaning and transformation.
- Perform SQL queries to filter the surgeries based on various criteria.

### 4. Data Visualization

- Import the cleaned and analyzed data into PowerBI.
- Create interactive dashboards to make the selection process more intuitive.

## Setup Instructions

1. Clone this repo to your local machine.
2. Run `pip install -r requirements.txt` to install necessary Python packages.
3. Follow database setup instructions in `database_setup.md`.
4. Run the `data_scraper.py` to scrape the NHS website.
5. Execute `data_analysis.py` for data analysis.
6. Open PowerBI file to see visualizations.

## Future Improvements

- Include more advanced filters like GP specialties.
- Extend the project to include other healthcare providers.

## Author
Robert Franklin 2023
