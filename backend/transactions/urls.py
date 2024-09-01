from django.urls import path
from .views import AddTransaction, GetTransactions, TransactionSummaryView


urlpatterns = [
    path("add/", AddTransaction.as_view(), name="add_transaction"),
    path("transactions/", GetTransactions.as_view(), name="get_transactions"),
    path(
        "summary/",
        TransactionSummaryView.as_view(),
        name="transaction-summary",
    ),
]
