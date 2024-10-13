from domain.transaction import Transaction
from infrastructure.csv_repository import CSVRepository
import os

def test_save_transaction():

    temp_csv= "temp.csv"
    repo= CSVRepository(csv_file=temp_csv)
    transaction = Transaction(date="12-12-2019", amount=8700, category="Egreso", description="Yamaha MT03")

    repo.save(transaction)

    df = repo.get_transactions_by_date("12-12-2019", "12-12-2019") 
    assert not df.empty
    assert df.iloc[0]["amount"] == 8700
    assert df.iloc[0]["category"] == "Egreso"
    assert df.iloc[0]["description"] == "Yamaha MT03"  
    os.remove(repo.CSV_FILE)

