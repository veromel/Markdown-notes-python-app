# Usa la imagen oficial de Python
FROM python:3.10-slim

# Instala Java y otras dependencias
RUN apt-get update && apt-get install -y default-jre && apt-get clean

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . /app

# Instala Poetry y configura para que no cree un entorno virtual
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

# Expone el puerto en el que corre FastAPI
EXPOSE 8000

# Comando para iniciar el servidor
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]



