# :school: :blue_heart: :rocket: Ensaware
## :white_check_mark: Pre-requisitos
- [python >= 3.10](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started/) `recomendado`

Para ejecutar el proyecto **Código QR** se puede realizar de dos maneras:
1. [Localmente.](#Localmente)
2. [Docker. `recomendado`](#Docker)

Para ambos casos, se debe de crear un archivo en la raíz del proyecto con el nombre: `.env`. Dentro del archivo ingresar los valores de las variables:
```env
# Database
DATABASE_HOST=""
DATABASE_USERNAME=""
DATABASE_PASSWORD=""
DATABASE_PORT=3306
DATABASE_NAME=""

# Fernet
FERNET_PASS=""

# Google
CLIENT_ID_GOOGLE=""
CLIENT_SECRET_GOOGLE=""

# Debug
DEBUG=0

# JWT
JWT_SECRET_KEY=""
JWT_EXPIRE_MINUTES=60
```

## Localmente
Para ejecutar el proyecto localmente, sigue los siguientes pasos:
1. Clonar el repositorio.
2. Crear un entorno virtual:
   1. **Windows:** `python -m venv venv`
   2. **Linux/Mac:** `python3 -m venv venv`
3. Activar el entorno virtual:
   1. **Windows:** `venv\Scripts\activate`
   2. **Linux/Mac:** `source venv/bin/activate`
4. Instalar las librerías del archivo `requirements.txt` `pip install -r requirements.txt`
5. Lanzar el proyecto: `uvicorn main:app --reload`


## Docker
Para ejecutar el proyecto con docker, sigue los siguientes pasos:
1. Clonar el repositorio.
2. Construir la imagen: `docker build -t qr_code .`
3. Ejecutar la imagen: `docker run -t qr_code`