from datetime import datetime, date

class Purchase:
    def __init__(self, DATE: str, DESCRIPTION: str, AMOUNT: float, POSTM: float, CATEGORY: str = "MISC"):
        self.dateFormatString = "%m/%d/%Y"

        self.date = DATE
        self.description = DESCRIPTION
        self.amount = AMOUNT
        self.category = CATEGORY
        self.postm = POSTM

    def getDateClass(self) -> date:
        return datetime.strptime(self.date, self.dateFormatString).date()

    def toCSVRow(self) -> list:
        return [self.date, self.description, round(self.amount, 2), round(self.postm, 2), self.category]

    def toString(self) -> str:
        output = self.date + " " + self.description + " " + str(self.amount) + " " + str(self.postm) + " " + self.category
        return output