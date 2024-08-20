from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORIES = {"I": "Ingreso", "E": "Egreso"}


def get_date(promt, allow_default=False):
    date_str = input(promt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)
    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print(
            "Formato de Fecha Invalida, Por favor ingresar la fecha en formato DD-MM-AAAA "
        )
        return get_date(promt, allow_default)


def get_amount():
    try:
        amount = float(input("Ingrese el Monto: "))
        if amount <= 0:
            raise ValueError("El monto no puede ser 0 o menor que 0")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()


def get_category():
    category = input(
        "Ingrese la Categoria ('I' para Ingreso 'E' para Expensa/Egreso): "
    ).upper()
    if category in CATEGORIES:
        return CATEGORIES[category]

    print("Categoria Invalida. Por favor ingrese 'I' para Ingreso 'E' para Egreso.")
    return get_category


def get_description():
    return input("Ingrese alguna descripcion (Opcional): ")
