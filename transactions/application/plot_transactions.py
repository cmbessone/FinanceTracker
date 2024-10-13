from domain.transaction_repository import TransactionRepository
from infrastructure.matplotlib_plotter import MatplotlibPlotter

class PlotTransactions:
    def __init__(self, repository: TransactionRepository):
        self.repository = repository
    
    def execute(self, start_date: str, end_date: str):
        return self.repository.get_transaction_by_date(start_date, end_date)

    @staticmethod
    def plot(df):
        MatplotlibPlotter.plot(df)