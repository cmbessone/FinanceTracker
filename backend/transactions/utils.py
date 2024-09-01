import matplotlib.pyplot as plt
from datetime import datetime
from django.db import models
from .models import Transaction

FORMAT = "%d-%m-%Y"


class TransactionUtils:
    @classmethod
    def get_transaction(self, start_date, end_date):
        start_date = datetime.strptime(start_date, FORMAT)
        end_date = datetime.strptime(end_date, FORMAT)

        transactions = Transaction.objects.filter(date__range=[start_date, end_date])

        if not transactions.exists():
            print("No hay transacciones para el rango de fechas solicitados")
            return None
        else:
            print(
                f"Transacciones desde {start_date.strftime(FORMAT)} hasta {end_date.strftime(FORMAT)}"
            )
