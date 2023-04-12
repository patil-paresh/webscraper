import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

html = requests.get('https://www.theverge.com/')
soup = BeautifulSoup(html.content, 'html5lib')

articles = soup.find_all('div', class_='lg:relative')

#Scrapping the required data 
for article in articles:
   
    headline = article.h2.a.get_text()

    link = article.h2.a['href']

    author = article.find(class_='text-gray-31 hover:shadow-underline-inherit dark:text-franklin mr-8').get_text()
    
    date = article.find(class_='text-gray-63 dark:text-gray-94').get_text()

#Creating Dictionary to store the data  
data=[]
dict={'url':link, 'headline':headline, 'author':author,'date':date}
data.append(dict)

#Saving the data in Csv file
df= pd.DataFrame(data)
csv=df.to_csv('ddmmyyy_verge.csv',index=False)


# Connect to the database
db = sqlite3.connect('mydatabase.db')

# Create a cursor object
cursor = db.cursor()

# Creating table
cursor.execute('''CREATE TABLE IF NOT EXISTS mytable
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                headline TEXT,
                author TEXT,
                date TEXT)''')

#Open CSV file and read the lines
with open('ddmmyyy_verge.csv', 'r') as csv_file:
    lines = csv_file.readlines()


for line in lines[1:]:  # Skip the header row

    fields = line.strip().split(',')

    # Extract the values from the fields
    url_value = fields[0]
    headline_value = fields[1]
    author_value = fields[2]
    date_value = fields[3]

    # Insert the row into the table
    cursor.execute('''INSERT INTO mytable (url, headline, author, date)
                        VALUES (?, ?, ?, ?)''', (url_value, headline_value, author_value, date_value))

# Commit the changes and close the connection
db.commit()
db.close()