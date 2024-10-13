import matplotlib.pyplot as plt


class MatplotlibPlotter:
    @staticmethod
    def plot(df):
        df.set_index("date", inplace=True)

        income_df = df[df["category"] == "Ingreso"].resample("D").sum().reindex(df.index, fill_value=0)
        expense_df = df[df["category"] == "Egreso"].resample("D").sum().reindex(df.index, fill_value=0)

        plt.figure(figsize=(10, 5))
        plt.plot(income_df.index, income_df["amount"], label="Ingresos", color="g")
        plt.plot(expense_df.index, expense_df["amount"], label="Egresos", color="r")
        plt.xlabel("Fecha")
        plt.ylabel("Monto")
        plt.title("Ingresos y Egresos Sobre el Tiempo")
        plt.legend()
        plt.grid(True)
        plt.show()