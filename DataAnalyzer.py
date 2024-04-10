#Will analyze a CSV file once it's been manually edited 
#(because it's unrealistic to expect auto categorizing every purchase)

import csv
import json
import time
from Purchase import Purchase

class DataAnalyzer:
    def __init__(self):
        self.ideas = "idk"

        #This will hold the statement deets Purchase class
        self.purchases = list()

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

    def validateAgainstBudget(self):
        categoryTotals = dict()
        for cat in self.budget.keys():
            categoryTotals[cat] = 0
        
        #Fill in the totals we have per category
        for pur in self.purchases:
            categoryTotals[pur.category] += pur.amount

        print("BUDGETED\t\tTOTAL\t\tDELTA\t\tCATEGORY")
        for cat in categoryTotals.keys():
            budgeted = self.budget[cat]
            print("{}\t\t\t{}\t\t{}\t\t{}".format(budgeted, categoryTotals[cat], budgeted - categoryTotals[cat], cat))

    def visualize(self):
        time.sleep(1)

#MAIN
def main():
    time.sleep(1)
    DA = DataAnalyzer()
    DA.importCSV("test.csv")
    DA.validateAgainstBudget()

if __name__ == "__main__":
    main()