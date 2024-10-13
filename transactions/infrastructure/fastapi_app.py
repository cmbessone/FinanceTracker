from fastapi import FastAPI, HTTPException
from infrastructure.csv_repository import CSVRepository
from application.add_transaction import AddTransaction
from application.view_transaction import ViewTransaction
from application.plot_transactions import PlotTransactions
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

class TransactionInput(BaseModel):
    date: str
    amount: float
    category: str
    description: str

repository = CSVRepository()

@app.post("/transaction")
async def add_transaction(transaction: TransactionInput):
    case = AddTransaction(repository)
    try:
        case.execute(transaction.date, transaction.amount, transaction.category, transaction.description)
        return {"message": "Transacción agregada con éxito"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/transactions")
async def get_transactions(start_date: str, end_date: str):
    case = ViewTransaction(repository)
    try:
        transactions = case.execute(start_date, end_date)
        return transactions.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/transactions/plot")
async def plot_transactions(start_date: str, end_date: str):
    case = PlotTransactions(repository)
    try:
        df = case.execute(start_date, end_date)
        PlotTransactions.plot(df)
        return {"message": "Gráfico generado con éxito"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))