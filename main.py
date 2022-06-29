from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

search_keys = [
    'Air',
    'Technologies'
]


def scrape():
    driver = webdriver.Chrome('./drivers/chromedriver')
    driver.get('https://eservices.secp.gov.pk/eServices/NameSearch.jsp')

    # find the searchbar in the page
    search_bar = driver.find_element(By.NAME, 'searchName')
    search_bar.clear()
    search_bar.send_keys('Air')
    search_bar.send_keys(Keys.RETURN)
    driver.close()


if __name__ == '__main__':
    scrape()
