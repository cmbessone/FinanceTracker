from datetime import datetime

class Transaction:
    def __init__(self, date:str, amount: float, category: str, description: str):
        """
        Initialize a Transaction object.

        Parameters
        ----------
        date : str
            The date of the transaction in the format DD-MM-YYYY.
        amount : float
            The amount of the transaction.
        category : str
            The category of the transaction.
        description : str
            A description of the transaction.

        """
        self.date = datetime.strptime(date, "%d-%m-%Y")
        self.amount = amount
        self.category = category
        self.description = description