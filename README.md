# GP-Finder: Evaluate & Select GPs in Your Area

**GP-Finder** is a personal project designed to facilitate the process of evaluating General Practitioners (GPs) available through the NHS website within a specific area. This tool aids users in making an informed decision when selecting a GP based on various criteria.

## Project Overview

The project aims to accomplish the following:

- Scrape data from the NHS website to identify GPs available in a user-specified area.
- Enrich the data with precise geolocation using advanced geocoding techniques.
- Store the enriched data in a SQL database for robust data handling.
- Perform comprehensive data analysis using Python and SQL.
- Visualize the data interactively using both Tableau and PowerBI to highlight data visualization skills.

## Technologies Used

- **Python**
- **SQLite** (SQL Database)
- **Tableau** (Data Visualization)
- **PowerBI** (Data Visualization)
- **BeautifulSoup** (Web Scraping)
- **Pandas** (Data Analysis)
- **Geopy** (Geocoding)

## How it Works

1. **Data Collection**
   - Utilize Python libraries like BeautifulSoup to scrape GP surgery data from the NHS website.
   - Collect data such as GP Name, Address, Phone, Accepting New Patients, and Reviews.

2. **Data Enrichment**
   - Parse addresses to extract postcodes, then use these for accurate geocoding.

3. **Data Storage**
   - Store the scraped and geocoded data in a SQLite database.

4. **Data Analysis & Visualization**
   - Clean and transform data using Python and Pandas.
   - Use SQL for data querying based on user-defined criteria.
   - Create interactive visualizations with Tableau and PowerBI for an intuitive data exploration experience.

## Setup Instructions

1. Clone this repository to your local machine.
2. Run `pip install -r requirements.txt` to install the required Python packages.
3. Follow the database setup instructions provided in `database_setup.md`.
4. Execute `data_scraper.py`, inputting your postcode when prompted, to scrape data from the NHS website.
5. `geocode_address.py` will enrich the data with latitude and longitude based on the extracted postcodes.
6. Explore the visualizations by opening the provided Tableau and PowerBI dashboard files.

## Future Improvements

- Implement dynamic data updates within the Tableau dashboard through user input for postcodes.
- Extend the project's scope to encompass additional healthcare providers and facilities.
- Introduce advanced filtering options like GP specialties and performance ratings.

## Visualizations

- View a comprehensive visualization of GP data in **Tableau** to interact with the data.
- Explore similar insights in **PowerBI** for comparative analysis and visualization techniques.

## Author

Robert Franklin - 2023
