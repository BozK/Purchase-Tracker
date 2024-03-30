#This will hold logic for login, navigation, and retrieving statements.
#The categorizing, and outputting results to CSV.
#Stretch: change CSV to update a big historical ledger tracking all of my cc statements

from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
import time
import configparser

class SiteParser:
    def __init__(self, configFile: str):
        config = configparser.ConfigParser()
        config.read(configFile)

        self.url = config['login']['url']
        self.username = config['login']['username']
        self.password = config['login']['password']

        #This will hold the statement deets
        self.entries = dict()

        #Stores the webdriver that we'll be navigating with
        self.webdriver = None

        #Not sure how impl will work yet, but add this keyword to category mapper
        self.keywordToCategoryMapper = None

    #Opens a web browser, logs in, navigates to the credit card page
    def startup(self) -> webdriver.Chrome:
        driver = webdriver.Chrome()
        #If stuff's loading slowly this helps
        driver.implicitly_wait(10)
        driver.get(self.url)

        username_field = driver.find_element(By.ID, value = "userId")
        password_field = driver.find_element(By.ID, value = "idpassword")
        signIn_button = driver.find_element(By.ID, value = "loginSubmit")

        username_field.send_keys(self.username)
        password_field.send_keys(self.password)
        #I think Truist is wonky without this
        time.sleep(1)
        signIn_button.click()

        time.sleep(5)
        #Navigates us to the main credit card 
        driver.find_elements(By.CLASS_NAME, "tru-core-container")[2].find_elements(By.TAG_NAME, "a")[2].click()

        time.sleep(10)

    #Parses the site
    def parse(self):
        time.sleep(1)

    def mapEntries(self):
        time.sleep(1)

    def exportToCSV(self, filename: str):
        time.sleep(1)


#MAIN
CON = "config.ini"
def main():
    P = SiteParser(CON)
    D = P.startup()

if __name__ == "__main__":
    main()