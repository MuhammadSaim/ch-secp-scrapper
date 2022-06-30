from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from pathlib import Path
import os
import mysql.connector
import datetime
import re

# load the .env file
load_dotenv(dotenv_path=Path('./.env'))

# search keywords for the companies
search_keys = [
    'Air',
    'Technologies'
]

# set the MySQL DB connection
mysql_connect = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    user=os.getenv('DB_USERNAME'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_DATABASE')
)


# function for scrape the date from the SECP companies list
def scrape():

    for tag in search_keys:

        records = 1

        # set the chrome driver
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        browser.get('https://eservices.secp.gov.pk/eServices/NameSearch.jsp')

        # check "Including Exact String" radio
        browser.find_element(By.CSS_SELECTOR, "input[type='radio'][value='Including Exact String']").click()

        # find the searchbar in the page
        search_bar = browser.find_element(By.NAME, 'searchName')
        search_bar.clear()
        search_bar.send_keys(tag)
        search_bar.send_keys(Keys.RETURN)

        # find the table and iterate through the table
        companies_table = browser.find_element(By.CSS_SELECTOR, 'div#body > table > tbody')
        trs = companies_table.find_elements(By.TAG_NAME, 'tr')
        # tds = trs[1871].find_elements(By.TAG_NAME, 'td')
        # print(tds[5].text == ' ')
        # exit()
        for row in trs:
            count = 1
            company = {}
            for td in row.find_elements(By.TAG_NAME, 'td'):
                if count == 2:
                    company.update({'name': td.text})
                if count == 3:
                    company.update({'status': td.text})
                if count == 4:
                    company.update({'cro_id': td.text})
                if count == 5:
                    company.update({'registration_number': td.text})
                if count == 6:
                    company.update({'registration_date': td.text})
                count = count + 1

            # store this company to the DB
            if is_word_in_text(tag, company['name']):
                store_company_to_db(company)

            print("{record}/{total} => {tag}".format(record=records, total=len(trs), tag=tag))
            records = records + 1

        # close the selenium browser connection
        browser.close()


# store company to the db
def store_company_to_db(company):
    cro_id = create_or_return_cro(company['cro_id'])
    company['cro_id'] = cro_id
    date_time = datetime.datetime.now()
    my_cursor = mysql_connect.cursor()
    registration_date = ''
    if company['registration_date'] != ' ':
        registration_date = parsing_date(company['registration_date'])
        registration_date = registration_date.strftime("%Y-%m-%d %I:%M:%S")
    sql = "INSERT INTO companies (cro_id, registration_number, name, status, registration_date, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (company['cro_id'], company['registration_number'], company['name'], company['status'], registration_date, date_time.strftime("%Y-%m-%d %I:%M:%S"), date_time.strftime("%Y-%m-%d %I:%M:%S"))
    my_cursor.execute(sql, val)
    mysql_connect.commit()


# check date value has correct format
def parsing_date(date):
    for fmt in ('%d-%m-%Y %H:%M:%S', '%d/%m/%Y'):
        try:
            return datetime.datetime.strptime(date, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')


# find word in the string
def is_word_in_text(word, text):
    pattern = r'(^|[^\w]){}([^\w]|$)'.format(word)
    pattern = re.compile(pattern, re.IGNORECASE)
    matches = re.search(pattern, text)
    return bool(matches)


# create CRO if not exists
def create_or_return_cro(cro):
    my_cursor = mysql_connect.cursor()
    sql = "SELECT * FROM cros WHERE name = '{name}'".format(name=cro)
    my_cursor.execute(sql)
    result = my_cursor.fetchone()
    if result:
        return result[0]
    else:
        date_time = datetime.datetime.now()
        sql = "INSERT INTO cros (name, created_at, updated_at) VALUES (%s, %s, %s)"
        val = (cro, date_time.strftime("%Y-%m-%d %I:%M:%S"), date_time.strftime("%Y-%m-%d %I:%M:%S"))
        my_cursor.execute(sql, val)
        mysql_connect.commit()
        return my_cursor.lastrowid


if __name__ == '__main__':
    scrape()
