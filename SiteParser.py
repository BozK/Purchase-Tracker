#This will hold logic for login, navigation, and retrieving statements.
#The categorizing, and outputting results to CSV.
#Stretch: change CSV to update a big historical ledger tracking all of my cc statements

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class SiteParser:
    def __init__(self, url: str):
        self.url = url
        self.username = "GET FROM CONFIG FILE"
        self.password = "GET FROM CONFIG FILE"

        #This will hold the statement deets
        self.entries = dict()

        #Stores the webdriver that we'll be navigating with
        self.webdriver = None

        #Not sure how impl will work yet, but add this keyword to category mapper
        self.keywordToCategoryMapper = None

    #Opens a web browser, logs in, navigates to the credit card page
    def startup(self) -> webdriver.Chrome:

    #Parses the site
    def parse(self):

    def mapEntries(self):

    def exportToCSV(self, filename: str):


#MAIN
def main():

if __name__ == "__main__":
    main()