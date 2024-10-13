from domain.transaction_repository import TransactionRepository

class ViewTransaction:
    def __init__ (self, repository: TransactionRepository):
        self.repository = repository
    
    def execute(self, start_date: str, end_date: str):
        return self.repository.get_transactions_by_date(start_date, end_date)
    
