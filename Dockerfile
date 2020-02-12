FROM python:3-slim-buster
    # copia el requirements a la carpeta base del contenedor
COPY requirements.txt /
    # Instala las dependencias de de la app
RUN pip install -r /requirements.txt
    # Copia todo el src a la carpeta del contenedor que le digamos
COPY src/ /app
    # Definimos una carpeta de trabajo
WORKDIR /app
    # Exponemos el puerto 5000
EXPOSE 5000
    # Arrancamos el proyecto
CMD ["python3", "main.py"]

VOLUME [ "./src", "./app" ]