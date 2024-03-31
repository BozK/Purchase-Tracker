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
        self.driver = None

        #Not sure how impl will work yet, but add this keyword to category mapper
        self.keywordToCategoryMapper = None

    #Opens a web browser, logs in, navigates to the credit card page
    def startup(self) -> webdriver.Chrome:
        self.driver = webdriver.Chrome()
        #If stuff's loading slowly this helps
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)

        username_field = self.driver.find_element(By.ID, value = "userId")
        password_field = self.driver.find_element(By.ID, value = "idpassword")
        signIn_button = self.driver.find_element(By.ID, value = "loginSubmit")

        username_field.send_keys(self.username)
        password_field.send_keys(self.password)
        #I think Truist is wonky without this
        time.sleep(1)
        signIn_button.click()

        time.sleep(5)
        #Navigates us to the main credit card 
        self.driver.find_elements(By.CLASS_NAME, "tru-core-container")[2].find_elements(By.TAG_NAME, "a")[2].click()

    #Parses the site
    def parse(self):
        time.sleep(5)
        entryRows = self.driver.find_elements(By.TAG_NAME, "tr")
        if (len(entryRows) < 40):
            print("ERROR: Elements didn't load in time")
        #Skip the header row
        entryRows = entryRows[1:]
        #Filter out the date 
        entryRows = [entry for entry in entryRows if entry.get_attribute("style") != "height: 0px;"]

        firstEntryCols = entryRows[0].find_elements(By.TAG_NAME, "td")

        DATE = firstEntryCols[0].text
        DESCRIPTION = firstEntryCols[2].find_element(By.TAG_NAME, 'p').text
        AMOUNT = firstEntryCols[3].find_element(By.TAG_NAME, 'tru-core-text').text

        print(DATE, " --- ", DESCRIPTION, " --- ", AMOUNT)

    def mapEntries(self):
        time.sleep(1)

    def exportToCSV(self, filename: str):
        time.sleep(1)


#MAIN
CON = "config.ini"
def main():
    siteParser = SiteParser(CON)
    siteParser.startup()
    siteParser.parse()

if __name__ == "__main__":
    main()