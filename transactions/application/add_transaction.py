from domain.transaction import Transaction
from domain.transaction_repository import TransactionRepository

class AddTransaction:
    def __init__(self, repository: TransactionRepository):
        self.repository = repository
        
    def execute(self, date: str, amount: float, category: str, description: str):
        transaction = Transaction(date, amount, category, description)
        self.repository.save(transaction)