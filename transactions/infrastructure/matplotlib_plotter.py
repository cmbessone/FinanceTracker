import matplotlib.pyplot as plt

class MatplotlibPlotter:
    @staticmethod
    def plot(df):
        # Asegurarse de que hay transacciones para mostrar
        if df.empty:
            print("No hay datos disponibles para graficar.")
            return

        # Convertimos la columna 'date' en el índice
        df.set_index("date", inplace=True)

        # Dividimos los ingresos y egresos
        income_df = df[df["category"] == "Ingreso"]
        expense_df = df[df["category"] == "Egreso"]

        plt.figure(figsize=(10, 5))

        # Graficar solo si hay datos
        if not income_df.empty:
            plt.plot(income_df.index, income_df["amount"], label="Ingresos", color="g", marker="o")
        if not expense_df.empty:
            plt.plot(expense_df.index, expense_df["amount"], label="Egresos", color="r", marker="o")

        plt.xlabel("Fecha")
        plt.ylabel("Monto")
        plt.title("Ingresos y Egresos en el Rango de Fechas Seleccionado")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Mostrar el gráfico
        plt.show()