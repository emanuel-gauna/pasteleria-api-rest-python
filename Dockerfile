# Usa una imagen base de Python
FROM python:3.12.4-slim

# Instalar wget y wait-for-it
RUN apt-get update && \
    apt-get install -y wget && \
    rm -rf /var/lib/apt/lists/* && \
    wget -O /usr/local/bin/wait-for-it.sh \
    https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
    && chmod +x /usr/local/bin/wait-for-it.sh

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de requisitos a la carpeta de trabajo
COPY requirements.txt requirements.txt

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de la aplicación
COPY . .

# Establece la variable de entorno para Flask
ENV FLASK_APP=app

# Expone el puerto que usará Flask
EXPOSE 5000

# Define el comando por defecto para ejecutar la aplicación
CMD ["wait-for-it.sh", "mysql-server:3306", "--timeout=180", "--", "sh", "-c", "python create_database.py && python update_image_paths.py && flask run --host=0.0.0.0 --port=5000"]
