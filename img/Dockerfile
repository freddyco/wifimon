# Utiliza la imagen base de Python
FROM python:3.10.13

# Crear un grupo y un usuario no root
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Agregar los archivos de la aplicaciÃ³n al contenedor
ADD /wifimon /wifimon/

# Actualizar pip y instalar las dependencias
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./wifimon/requirements.txt

# Cambiar permisos del directorio de trabajo al usuario no root
RUN chown -R appuser:appgroup /wifimon

# Establecer el directorio de trabajo
WORKDIR /wifimon/

# Establecer el usuario no root para ejecutar el contenedor
USER appuser

# Comando para ejecutar la aplicaciÃ³n
CMD ["python", "app.py"]