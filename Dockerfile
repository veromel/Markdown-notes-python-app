# Usa la imagen oficial de Python
FROM python:3.10-slim

# Instala Java y otras dependencias
RUN apt-get update && apt-get install -y default-jre && apt-get clean

# Establece el directorio de trabajo
WORKDIR /app

# Copia primero solo los archivos necesarios para la instalación de dependencias
COPY pyproject.toml poetry.lock* /app/

# Instala Poetry y las dependencias
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Copia el archivo .env.example
COPY .env.example /app/.env

# Copia el resto de la aplicación
COPY . /app/

# Expone el puerto en el que corre FastAPI
EXPOSE 8000

# Comando para iniciar el servidor usando uvicorn directamente
CMD ["poetry", "run", "uvicorn", "apps.http.app:create_app", "--host", "0.0.0.0", "--port", "8000", "--factory"]



