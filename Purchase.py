class Purchase:
    def __init__(self, DATE: str, DESCRIPTION: str, AMOUNT: float, CATEGORY: str = "MISC"):
        self.date = DATE
        self.description = DESCRIPTION
        self.amount = AMOUNT
        self.category = CATEGORY

    def toCSVRow(self) -> list:
        return [self.date, self.description, self.amount, self.category]

    def toString(self) -> str:
        output = self.date + " " + self.description + " " + str(self.amount) + " " + self.category
        return output