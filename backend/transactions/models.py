# Crear clase para el modelo de base de datos que quiero persistir en este caso
# El model va a tener los datos que voy a guardar en la base de datos
# Se hace de la siguiente manera
#
# se crea la case que en cuestion que recibe models.Model
# se asigna el tipo de dato de cada campo DateField, DecimalField, CharField, TextField
#
# # se define un metodo string
#  Ejemplo
#  def __str__ (self)
#        return f"{self.field1}  - {self.field2} - {self.field3}"
#
# #
from django.db import models


class Transaction(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return f"{self.date} - {self.amount} - {self.category} - {self.description}"
