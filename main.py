import sqlite3
from bs4 import BeautifulSoup
import requests

# TODO connect to data base

conn = sqlite3.connect("countries.db")
cruser = conn.cursor()

cruser.execute("""
               CREATE TABLE IF NOT EXISTS countries(
                   id INTEGER PRIMARY KEY AUTOINCREMENT ,
                   country_name TEXT NOT NULL ,
                   capital TEXT ,
                   population INTEGER,
                   area INTEGER 
                   )
                    """)

# TODO conect to url
url = "https://www.scrapethissite.com/pages/simple/"
respones = requests.get(url)
respones.encoding = "utf-8"

soup = BeautifulSoup(respones.text, "html.parser")

countries = soup.find_all("div", class_="country")[:20]

#todo save data
for country in countries:

    name = country.find("h3", class_='country-name').text.strip()

    capital = country.find("span", class_="country-capital").text.strip()

    population = country.find("span", class_="country-population").text.strip()
    population = int(population)

    area = country.find("span", class_="country-area").text.strip()
    area = int(float(area))

    cruser.execute("""
                   INSERT INTO countries(country_name , capital , population , area )
                   VALUES (?,?,?,?)
                   """, (name, capital, population, area))

conn.commit()
#TODO 5 country name and sum population of 20 countries
print("اطلاعات 20 کشور با موفقیت ذخیره شد \n")

print("پنج کشور اول :")

cruser.execute("""
               SELECT country_name , capital , population , area 
               FROM countries 
               LIMIT 5 
            
               """)
rows = cruser.fetchall()

for row in rows:

    print(row)

cruser.execute("""
               SELECT SUM(population)
               FROM countries
               """)
total_population = cruser.fetchone()[0]

print(f"جمع 20 کشور : \n {total_population} ")


conn.close()
