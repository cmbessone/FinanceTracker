# Dockerfile
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de dependencias
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente de la aplicación
COPY transactions/ .

# Exponer el puerto 8000 para FastAPI
EXPOSE 8000

# Comando para correr FastAPI
CMD ["uvicorn", "infrastructure.fastapi_app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
