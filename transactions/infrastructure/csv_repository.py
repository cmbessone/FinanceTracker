import csv
import pandas as pd
from domain.transaction import Transaction
from domain.transaction_repository import TransactionRepository

class CSVRepository(TransactionRepository):
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]

    def __init__(self):
        self.initalize_csv()

    def initalize_csv(self):
        try:
            pd.read_csv(self.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=self.COLUMNS)
            df.to_csv(self.CSV_FILE, index=False)

    def save(self, transaction: Transaction):
        new_entry = {
            "date": transaction.date.strftime("%d-%m-%Y"),
            "amount": transaction.amount,
            "category": transaction.category,
            "description": transaction.description,
        }
        with open(self.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.COLUMNS)
            writer.writerow(new_entry)

    def get_transactions_by_date(self, start_date: str, end_date: str):
        df = pd.read_csv(self.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
        start = pd.to_datetime(start_date, format="%d-%m-%Y")
        end = pd.to_datetime(end_date, format="%d-%m-%Y")
        return df[(df["date"] >= start) & (df["date"] <= end)]