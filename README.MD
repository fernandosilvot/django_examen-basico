# Documentación del Proyecto

## Instalación

1. Clona el repositorio en tu máquina local:

    ```bash
    git clone https://github.com/fernandosilvot/django_examen-basico
    ```

2. Navega hasta el directorio del proyecto:

    ```bash
    cd django_examen-basico
    ```

3. Crea un entorno virtual e actívalo:

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

4. Instala las dependencias del proyecto:

    ```bash
    pip install -r requirements.txt
    ```

## Configuración


1. Ejecuta las migraciones para crear las tablas en la base de datos:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

2. Crea un superusuario para acceder al panel de administración:

    ```bash
    python manage.py createsuperuser 
    ```

    Sigue las instrucciones para establecer una contraseña para el superusuario.

## Ejecución

1. Inicia el servidor de desarrollo:

    ```bash
    python manage.py runserver
    ```

2. Abre tu navegador web y accede a `http://127.0.0.1:8000/` para ver tu aplicación en funcionamiento.

3. Accede al panel de administración en `http://127.0.0.1:8000/admin/` e inicia sesión con las credenciales del superusuario que creaste anteriormente.

## Uso

Aquí puedes describir cómo utilizar tu aplicación, incluyendo las funcionalidades principales y cualquier información adicional que sea relevante.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.