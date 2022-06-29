from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

search_keys = [
    'Air',
    'Technologies'
]


def scrape():
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    browser.get('https://eservices.secp.gov.pk/eServices/NameSearch.jsp')

    # check "Including Exact String" radio
    browser.find_element(By.CSS_SELECTOR, "input[type='radio'][value='Including Exact String']").click()

    # find the searchbar in the page
    search_bar = browser.find_element(By.NAME, 'searchName')
    search_bar.clear()
    search_bar.send_keys('Air')
    search_bar.send_keys(Keys.RETURN)
    browser.close()


if __name__ == '__main__':
    scrape()
