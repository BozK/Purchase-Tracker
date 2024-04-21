#Will analyze a CSV file once it's been manually edited 
#(because it's unrealistic to expect auto categorizing every purchase)

import csv
from datetime import datetime, timedelta
import json
import time
from Purchase import Purchase

class DataAnalyzer:
    def __init__(self):
        self.ideas = "idk"

        #Date formatting
        self.TODAY = datetime.now().date()
        self.dateFormatString = "%m/%d/%Y"

        #This will hold the Purchases made
        self.purchases = list()
        #This will hold the totals for each category, with the key being the category
        #Will contain [Total, Total Post-M]
        self.categoryTotals = dict()

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
                self.purchases.append(Purchase(row[0], row[1], float(row[2]), POSTM, CATEGORY))

    def validateAgainstBudget(self, days: int = 30, costThreshold: int = 0):
        # for cat in self.budget.keys():
        #     self.categoryTotals[cat] = 0
        
        #When we should stop reading the entries from the CSV against the budget
        dateCutoff = self.TODAY - timedelta(days=days)
        
        #Fill in the totals we have per category
        for pur in self.purchases:
            if (datetime.strptime(pur.date, self.dateFormatString).date() <= dateCutoff):
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
        with open('HISTORICAL.csv', 'w+', newline='') as f:
            csvWriter = csv.writer(f)
            csvWriter.writerow(['DATE', 'DESCRIPTION', 'AMOUNT', 'POST M AMOUNT', 'CATEGORY'])
            for p in self.purchases:
                csvWriter.writerow(p.toCSVRow())

    def visualize(self):
        time.sleep(1)

#MAIN
def main():
    time.sleep(1)
    DA = DataAnalyzer()
    DA.importCSV("test.csv")
    DA.validateAgainstBudget(days = 120, costThreshold=2)
    DA.exportToCSV()

if __name__ == "__main__":
    main()
    
