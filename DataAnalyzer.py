#Will analyze a CSV file once it's been manually edited 
#(because it's unrealistic to expect auto categorizing every purchase)

import csv
from datetime import datetime, timedelta
import json
import time
from Purchase import Purchase
import os

class DataAnalyzer:
    def __init__(self):
        self.ideas = "idk"

        #Date formatting
        self.TODAY = datetime.now().date()
        self.dateFormatString = "%m/%d/%Y"

        #This will hold the Purchases made
        self.currentPurchases = list()
        #This will hold the totals for each category, with the key being the category
        #Will contain [Total, Total Post-M]
        self.categoryTotals = dict()

        self.historicalPurchases = list()

        with open("budget.json") as f:
            self.budget = json.load(f)

    def importCSV(self, filename: str):
        with open(filename, 'r') as f:
            csvReader = csv.reader(f)
            for row in csvReader:
                #Skips the header row
                if (row[0] == "DATE"):
                    continue

                #Fills in the empty categories with a catch-all MISC
                CATEGORY = row[4]

                #Checks if it's one of a few budget categories that get cut to 1/2 or 2/3 because I'm splitting with M
                if (CATEGORY in self.budget):
                    POSTM = float(row[2]) * self.budget[CATEGORY][1]
                else:
                    POSTM = float(row[2])

                #Add to the list
                self.currentPurchases.append(Purchase(row[0], row[1], float(row[2]), POSTM, CATEGORY))

    def validateCurrentAgainstBudget(self, days: int = 30, costThreshold: int = 0):
        #When we should stop reading the entries from the CSV against the budget
        dateCutoff = self.TODAY - timedelta(days=days)
        
        #Fill in the totals we have per category
        for pur in self.currentPurchases:
            if (pur.getDateClass() <= dateCutoff):
                break #We can assume the data is sorted on date - if it's changed to not be, this should be a continue

            if (pur.category not in self.categoryTotals):
                self.categoryTotals[pur.category] = [pur.amount, pur.postm]
            else:
                self.categoryTotals[pur.category] = [pur.amount + self.categoryTotals[pur.category][0], \
                                                     pur.postm + self.categoryTotals[pur.category][1]]

        print("TOTAL\t\tBUDGETED\tDELTA\t\t| CATEGORY |\t\tPM TOTAL\tPM BUDGETED\tPM DELTA")
        print("\t\t{} days".format(days))
        print("-"*64) #What a niche feature but I LOVE multiplying strings with integers

        for cat in self.categoryTotals.keys():
            if (cat in self.budget):
                #Budget contains [Budgeted Amount, Split with M ratio]
                budgeted = self.budget[cat][0] * days / 30
                budgetedM = self.budget[cat][0] * self.budget[cat][1] * days / 30
            else:
                0

            catTotal = self.categoryTotals[cat][0]
            catTotalM = self.categoryTotals[cat][1]

            difference = budgeted - catTotal
            differenceM = budgetedM - catTotalM

            #Using input parameter to skip over rows that aren't
            if (abs(difference) < costThreshold):
                continue

            print("{:.2f}\t\t{:.2f}\t\t{:.2f}\t\t{}\t\t\t{:.2f}\t\t{:.2f}\t\t{:.2f}".format(catTotal, budgeted, difference, cat, catTotalM, budgetedM, differenceM))



    def exportToCSV(self):
        #Two modes: historical file already exists locally OR it needs to be created
        if (os.path.isfile('HISTORICAL.csv')):
            #Read in existing historical file
            self.historicalPurchases = []
            with open('HISTORICAL.csv', 'r', newline='') as f:
                csvReader = csv.reader(f)
                for r in csvReader:
                    #Skip reading over a header row
                    if (r[0] == "DATE"):
                        continue
                    self.historicalPurchases.append(Purchase(r[0], r[1], float(r[2]), float(r[3], r[4])))
            
            self.removeDupes()
            #Now that dupes are cleared up, we can append all the currentPurchases remaining
            #(reverse order needed for correct insertion order)
            for cRow in self.currentPurchases[::-1]:
                self.historicalPurchases.insert(1, cRow)

            #And now we export
            with open('HISTORICAL.csv', 'w', newline='') as f:
                csvWriter = csv.writer(f)
                csvWriter.writerow(['DATE', 'DESCRIPTION', 'AMOUNT', 'POST M AMOUNT', 'CATEGORY'])
                for hRow in self.historicalPurchases:
                    csvWriter.writerow(hRow.toCSVRow())

        #File doesn't already exist, let's make one
        else:
            with open('HISTORICAL.csv', 'w', newline='') as f:
                csvWriter = csv.writer(f)
                csvWriter.writerow(['DATE', 'DESCRIPTION', 'AMOUNT', 'POST M AMOUNT', 'CATEGORY'])
                for cRow in self.currentPurchases:
                    csvWriter.writerow(cRow.toCSVRow())

    def removeDupes(self):
        for cRow in self.currentPurchases:
            #Easy check - if currentPurchases[x] is a later date than the first in historicalPurchases, 
            #it's later than everything in historicalPurchases, therefore it's not a dupe
            if (cRow.getDateClass() > self.historicalPurchases[0].getDateClass()):
                continue
            #Entries with a date BEFORE the latest in historicalPurchases should already have been
            #included, therefore cRow is a dupe we can remove
            elif (cRow.getDateClass() < self.historicalPurchases[0].getDateClass()):
                self.currentPurchases.remove(cRow)
            #Granular check if date equals the latest in historicalPurchases - could be a distinct purchase
            else:
                for hRow in self.historicalPurchases:
                    #Gotten far enough into historicalPurchases that we know cRow came after anything left
                    if (cRow.getDateClass() > hRow.getDateClass()):
                        break

                    if (cRow.getDateClass() == hRow.getDateClass() and \
                        cRow.description == hRow.description and \
                        cRow.amount == hRow.amount):
                        #Dupe detected, OBLITERATE THAT TWINK
                        self.currentPurchases.remove(cRow)


    def visualize(self):
        time.sleep(1)

#MAIN
def main():
    time.sleep(1)
    DA = DataAnalyzer()
    DA.importCSV("test.csv")
    DA.validateCurrentAgainstBudget(days = 120, costThreshold=2)
    DA.exportToCSV()

if __name__ == "__main__":
    main()
    
