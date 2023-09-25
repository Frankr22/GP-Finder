from bs4 import BeautifulSoup
import requests, sqlite3, time, re

# Function to create SQLite table
def create_table():
    conn = sqlite3.connect('gp_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS gp_info
                 (Name TEXT, Address TEXT, Phone TEXT, 
                 Accepting_New_Patients BOOLEAN, 
                 Accepts_Out_of_Area_Registrations BOOLEAN, 
                 Online_Registration_Available BOOLEAN,
                 Average_Rating REAL)''')
    conn.commit()
    conn.close()

# Function to insert data into SQLite table
def insert_data(gp_data):
    conn = sqlite3.connect('gp_data.db')
    c = conn.cursor()
    for data in gp_data:
        c.execute("INSERT INTO gp_info VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (data['Name'], data['Address'], data['Phone'],
                   data['Accepting New Patients'], 
                   data['Accepts Out of Area Registrations'], 
                   data['Online Registration Available'],
                   data.get('Average Rating', None)))
    conn.commit()
    conn.close()

# Function to scrape data
def scrape_data():
    # Hardcoded URL for a specific postcode
    url = "https://www.nhs.uk/service-search/find-a-gp/results/SW12%209LQ"

    # Send GET request
    response = requests.get(url)

    # Initialize BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate each GP info using 'results__details' class
    gp_blocks = soup.find_all('div', {'class': 'results__details'})

    gp_data = []
    for block in gp_blocks:
        name = block.find('h2', {'id': lambda x: x and x.startswith('orgname_')}).text.strip()
        address = block.find('p', {'id': lambda x: x and x.startswith('address_')}).text.strip()
        phone = block.find('p', {'id': lambda x: x and x.startswith('phone_')}).text.strip()
        
        tags = block.find_all('strong', {'id': lambda x: x and x.startswith('result_item_')})
        tags_text = [tag.text.strip() for tag in tags]

        gp_data.append({
            'Name': name,
            'Address': address,
            'Phone': phone,
            'Accepting New Patients': 'Accepting new patients' in tags_text,
            'Accepts Out of Area Registrations': 'Accepts out of area registrations' in tags_text,
            'Online Registration Available': 'Online registration available' in tags_text
        })
    
    return gp_data

# Create the table
create_table()

# Perform the scrape
result = scrape_data()

# Insert data into SQLite database
insert_data(result)

# Function to scrape initial GP URLs
def scrape_gp_links():
    url = "https://www.nhs.uk/service-search/find-a-gp/results/SW12%209LQ"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    gp_links = []
    
    # Locate each GP details link
    for link in soup.find_all('a', {'class': 'nhsapp-open-in-webview'}):
        href = link.get('href')
        if not (href.startswith('javascript') or href.startswith('#')):
            gp_links.append(href)

    return gp_links

# Existing scrape_reviews function
def scrape_reviews(gp_links):
    for gp_url in gp_links:
        review_url = f"{gp_url}/ratings-and-reviews"
        ratings = []
        try:
            response = requests.get(review_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            review_blocks = soup.find_all('div', {'class': 'org-review'})
            
            for block in review_blocks:
                rating_text = block.find('p', {'id': re.compile(r'star-rating-.*')}).text.strip()
                rating_value = float(rating_text.split(' ')[1])
                ratings.append(rating_value)
            
            if ratings:
                average_rating = sum(ratings) / len(ratings)
                update_db(gp_url.split('/')[-1], average_rating)
            
        except requests.HTTPError as e:
            print(f"Could not fetch reviews for {gp_url}: {e}")

        time.sleep(2)

# Function to update database
def update_db(gp_name, avg_rating):
    conn = sqlite3.connect('gp_data.db')
    c = conn.cursor()
    c.execute("UPDATE gp_info SET 'Average_Rating' = ? WHERE Name = ?", (avg_rating, gp_name))
    conn.commit()
    conn.close()

# Create the table
create_table()

# Perform the scrape
result = scrape_data()

# Insert data into SQLite database
insert_data(result)

# Scrape the GP links
gp_links = scrape_gp_links()

# Scrape the reviews
scrape_reviews(gp_links)