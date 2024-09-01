import pandas as pd

from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from transactions.serializers import TransactionSerializer
from transactions.models import Transaction
from .utils import TransactionUtils

"""Usamos el Decorator Protección CSRF

Utiliza @method_decorator(csrf_exempt) para desactivar la verificación CSRF en
las vistas API, pero asegúrate de manejar la autenticación 
y permisos adecuadamente para evitar vulnerabilidades."""


CSV_FILE = "/Users/cristianbessone/projects/Finance_Tracker/finance_data.csv"
FORMAT = "%d-%m-%Y"


# Voy a crear una subclase que herede de generic.CreateApiView
# voy a crear dos atributos de clase
#   queryset: obtener todos los objetos Django de la app transactions
#   serializer_class: la clase con TransactionSerializer
#
# definir el metodo post(self, request, *args, *kwargs):
#
#
#
#
# #
@method_decorator(csrf_exempt, name="dispatch")
class AddTransaction(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Utilizamos la Base SQLite3 del ORM. dejamos de utilizar CSV
            # transaction = serializer.save()
            # self.save_to_csv(transaction)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def save_to_csv(self, transaction):
        try:
            df = pd.read_csv(CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=["date", "amount", "category", "description"])

        new_entry = {
            "date": transaction.date.strftime("%d-%m-%Y"),
            "amount": transaction.amount,
            "category": transaction.category,
            "description": transaction.description,
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)


# class AddTransaction(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         # Serializar la data del request
#         serializer = TransactionSerializer(data=request.data)
#         if serializer.is_valid():
#             # Cargamos el Dataframe con la informacion (Fuente de Datos actual CSV) TODO migrar a Base de datos
#             data = serializer.validated_data
#             df = pd.read_csv(CSV_FILE)
#             # Agregamos al Dataframe la data nueva con Append
#             df = df.append(data, ignore_index=True)
#             # Convertimos el dataframe a CSV
#             df.to_csv(CSV_FILE, index=False)
#             # mostramos respuesta y HTTP 201
#             return Response(
#                 {"message: Transaction created successfully"},
#                 status=status.HTTP_201_CREATED,
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name="dispatch")
### This Method to get transactions use SQLite3 as ORM datasource
class GetTransactions(APIView):

    def get(self, request):
        startDate = request.query_params.get("start_date")
        endDate = request.query_params.get("end_date")

        transactions = Transaction.objects.all()

        if startDate and endDate:
            transactions = transactions.filter(date__range=[startDate, endDate])

        if not transactions.exists():
            return Response(
                {"message": "No transactions Found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


## This Method to get Transactions using CSV as datasource.

# class GetTransactions(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         df = pd.read_csv(CSV_FILE)
#         # obtener informacion de la fuente de datos para un rango de fechas
#         startDate = request.query_params.get("start_date")
#         endDate = request.query_params.get("end_date")
#         # estantarizar la fecha con el Formato
#         df["date"] = pd.to_datetime(df["date"], format=FORMAT)

#         # agregar Filtros de fechaDesde, FechaHasta
#         if startDate and endDate:
#             # estantarizar la fecha ingresadas por el usuario con el Formato %d%m%Y
#             startDate = datetime.strptime(startDate, FORMAT)
#             endDate = datetime.strptime(endDate, FORMAT)
#             # filtrar Dataframe
#             mask = (df["date"] >= startDate) & (df["date"] <= endDate)
#             filtered_df = df.lsoc[mask]
#         else:
#             filtered_df = df

#         if filtered_df.empty:
#             return Response(
#                 {"message": "No Transaction Found"}, status=status.HTTP_404_NOT_FOUND
#             )
#         return Response(
#             filtered_df.to_dict(orient="records"), status=status.HTTP_200_OK
#         )


#
#
class TransactionSummaryView(APIView):
    def get(self, request):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if not start_date or not end_date:
            return Response(
                {"error": "Please provide both start_date and end_date"}, status=400
            )

        transactions = TransactionUtils.get_transaction(start_date, end_date)

        if transactions is None:
            return Response(
                {"message": "No transactions found for the given date range"},
                status=404,
            )

        # Opcionalmente, podrías devolver los totales en la respuesta
        total_ingresos = (
            transactions.filter(category="Ingreso").aggregate(
                total=models.Sum("amount")
            )["total"]
            or 0.0
        )
        total_egresos = (
            transactions.filter(category="Egreso").aggregate(
                total=models.Sum("amount")
            )["total"]
            or 0.0
        )
        net_savings = total_ingresos - total_egresos

        return Response(
            {
                "total_ingresos": total_ingresos,
                "total_egresos": total_egresos,
                "net_savings": net_savings,
            },
            status=200,
        )
