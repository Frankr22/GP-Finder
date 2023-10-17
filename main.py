from bs4 import BeautifulSoup
import requests
import sqlite3
import logging

# Initialize logging
logging.basicConfig(filename='gp_finder.log', level=logging.INFO)

def db_connect():
    return sqlite3.connect('gp_data.db')

def create_table():
    with db_connect() as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS gp_info
                     (ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                     Name TEXT, Address TEXT, Phone TEXT, 
                     Accepting_New_Patients BOOLEAN,
                     Accepts_Out_of_Area_Registrations BOOLEAN, 
                     Online_Registration_Available BOOLEAN,
                     Average_Rating REAL)''')
        conn.commit()

def insert_data(gp_data):
    with db_connect() as conn:
        c = conn.cursor()
        for data in gp_data:
            c.execute("INSERT INTO gp_info (Name, Address, Phone, Accepting_New_Patients, Accepts_Out_of_Area_Registrations, Online_Registration_Available) VALUES (?, ?, ?, ?, ?, ?)",
                      (data['Name'], data['Address'], data['Phone'], data['Accepting New Patients'], data['Accepts Out of Area Registrations'], data['Online Registration Available']))
        conn.commit()

def scrape_data(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
    except requests.HTTPError as e:
        logging.error(f"HTTP Error: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
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

def analyze_data():
    with db_connect() as conn:
        c = conn.cursor()
        c.execute("SELECT Name, Average_Rating FROM gp_info WHERE Accepting_New_Patients = 1 ORDER BY Average_Rating DESC LIMIT 10")
        top_10_gps = c.fetchall()
    return top_10_gps

if __name__ == "__main__":
    create_table()
    url = "https://www.nhs.uk/service-search/find-a-gp/results/SW12%209LQ"
    gp_data = scrape_data(url)
    insert_data(gp_data)

    # Analyze and get the top 10 GPs
    top_10_gps = analyze_data()
    print("Top 10 GPs accepting new patients sorted by rating:")
    for i, (name, rating) in enumerate(top_10_gps, 1):
        print(f"{i}. {name} - Rating: {rating}")
