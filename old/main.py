import csv
import pandas as pd
import matplotlib.pyplot as plt
from data_entry import get_amount, get_category, get_date, get_description
from datetime import datetime


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initalize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=["date", "amount", "category", "description"])
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def get_transaction(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No hay transacciones para el rango de fechas solicitado")
        else:
            print(
                f"Transacciones desde {start_date.strftime(CSV.FORMAT)} hasta {end_date.strftime(CSV.FORMAT)}"
            )
            print(
                filtered_df.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}
                )
            )
            total_ingresos = filtered_df[filtered_df["category"] == "Ingreso"][
                "amount"
            ].sum()
            total_egresos = filtered_df[filtered_df["category"] == "Egreso"][
                "amount"
            ].sum()

            print("\nResumen:")
            print(f"Total Ingresos : ${total_ingresos:.2f}")
            print(f"Total Egresos: ${total_egresos:.2f}")
            print(f"Ahorro Neto: ${(total_ingresos - total_egresos):.2f}")

        return filtered_df


def add():
    CSV.initalize_csv()
    date = get_date(
        "Ingrese la fecha de la transacción (DD-MM-AAAA) o 'Enter' para la Fecha de Hoy: ",
        allow_default=True,
    )
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)


def plot_transactions(df):
    df.set_index("date", inplace=True)

    income_df = (
        df[df["category"] == "Ingreso"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["category"] == "Egreso"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Ingresos", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Egresos", color="r")
    plt.xlabel("Fecha")
    plt.ylabel("Monto")
    plt.title("Ingresos y Egresos Sobre el Tiempo")
    plt.legend()
    plt.grid(True)
    print("placeholder2")
    plt.show()


def main():
    while True:
        print("\n1. Agregar transaccion")
        print("2. Ver transacciones y resumen por rango de fechas")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Ingrese Fecha Desde (DD-MM-AAAAA): ")
            end_date = get_date("Ingrese Fecha Hasta (DD-MM-AAAAA): ")
            df = CSV.get_transaction(start_date, end_date)
            if input("Queres Graficar tu consulta? ('S' o 'N'): ").lower() == "s":
                plot_transactions(df)
        elif choice == "3":
            break
        else:
            print("Invalid, Ingresar 1,2 o 3.")


if __name__ == "__main__":
    main()
