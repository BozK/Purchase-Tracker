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
                CATEGORY = "MISC" if row[3] == "" else row[3]

                #Add to the list
                self.purchases.append(Purchase(row[0], row[1], float(row[2]), CATEGORY))

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
                self.categoryTotals[pur.category] = pur.amount
            else:
                self.categoryTotals[pur.category] = pur.amount + self.categoryTotals[pur.category]

        print("TOTAL\t\tBUDGETED\tDELTA\t\tCATEGORY")
        print("\t\t{} days".format(days))
        print("-"*64) #What a niche feature but I LOVE multiplying strings with integers
        for cat in self.categoryTotals.keys():
            budgeted = (self.budget[cat] * days / 30) if (cat in self.budget) else 0
            catTotal = self.categoryTotals[cat]
            difference = budgeted - catTotal

            #Using input parameter to skip over rows that aren't
            if (abs(difference) < costThreshold):
                continue

            print("{:.2f}\t\t{:.2f}\t\t{:.2f}\t\t{}".format(catTotal, budgeted, difference, cat))

    def visualize(self):
        time.sleep(1)

#MAIN
def main():
    time.sleep(1)
    DA = DataAnalyzer()
    DA.importCSV("test.csv")
    DA.validateAgainstBudget(days = 15, costThreshold=2)

if __name__ == "__main__":
    main()