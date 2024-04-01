#This will hold logic for login, navigation, and retrieving statements.
#The categorizing, and outputting results to CSV.
#Stretch: change CSV to update a big historical ledger tracking all of my cc statements

from selenium import webdriver
from datetime import datetime, timedelta
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

        #Date formatting
        self.TODAY = datetime.now().date()
        self.dateFormatString = "%m/%d/%Y"

        #This will hold the statement deets
        self.entries = list()

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
    def parse(self, days: int = 30):
        #Load seems required
        time.sleep(4)

        #This should roughly be enough to scroll proportionally
        scrolls = 3 * (days // 30 + 1)
        for i in range(0, scrolls):
            #Per scroll times, we move down 1000 pixels
            self.driver.execute_script("window.scrollBy(0, {});".format(1000))
        
        #When we should stop adding to the entries list
        dateCutoff = self.TODAY - timedelta(days=days)
        
        #Load seems required
        time.sleep(3)
        entryRows = self.driver.find_elements(By.TAG_NAME, "tr")
        if (len(entryRows) < 40):
            print("ERROR: Elements didn't load in time")

        #Skip the header row
        entryRows = entryRows[1:]
        #Filter out the date 
        entryRows = [entry for entry in entryRows if entry.get_attribute("style") != "height: 0px;"]

        for entry in entryRows:
            entryCols = entry.find_elements(By.TAG_NAME, "td")
            
            DATE = entryCols[0].text
            if (not datetime.strptime(DATE, self.dateFormatString).date() > dateCutoff):
                break
            DESCRIPTION = entryCols[2].find_element(By.TAG_NAME, 'p').text
            AMOUNT = entryCols[3].find_element(By.TAG_NAME, 'tru-core-text').text
            self.entries.append((DATE, DESCRIPTION, AMOUNT))
            
            print(DATE, " --- ", DESCRIPTION, " --- ", AMOUNT)

        print("{} items in last {} days".format(len(self.entries), days))

    def mapEntries(self):
        time.sleep(1)

    def exportToCSV(self, filename: str):
        time.sleep(1)


#MAIN
CON = "config.ini"
def main():
    siteParser = SiteParser(CON)
    siteParser.startup()
    siteParser.parse(30)

if __name__ == "__main__":
    main()