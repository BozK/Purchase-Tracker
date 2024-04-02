class Purchase:
    def __init__(self, DATE: str, DESCRIPTION: str, AMOUNT: str, CATEGORY: str):
        self.date = DATE
        self.description = DESCRIPTION
        self.amount = AMOUNT
        self.category = CATEGORY

    def toCSVRow(self) -> list:
        return [self.date, self.description, self.amount, self.category]