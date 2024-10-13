from abc import ABC, abstractmethod
from domain.transaction import Transaction

class TransactionRepository(ABC):

    @abstractmethod
    def save(self, transaction: Transaction):
        NotImplementedError

    @abstractmethod
    def get_transactions_by_date(self, start_date: str, end_date: str):
        NotImplementedError
