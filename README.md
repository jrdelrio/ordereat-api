# Documentación de la API de OrderEAT

## Introducción

La API de OrderEAT permite gestionar solicitudes de contacto realizadas a través del formulario web. Esta API está construida en Flask, es ligera y está pensada para manejar un volumen bajo de tráfico. Envía dos correos electrónicos utilizando el servicio de Resend: uno interno al equipo de OrderEAT y otro de agradecimiento al remitente.

---

## Base URL

- Producción: `https://landing-api.ordereat.com`

---

## Instrucciones para correr la API

### 1. Clonar el repositorio

```bash
git clone https://github.com/jrdelrio/ordereat-api.git
cd ordereat-api
```

### 2. Crear y activar entorno virtual

```bash
sudo apt update
sudo apt install python3-venv -y
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Crear archivo `.env`

Crea un archivo `.env` con la siguiente variable:

```env
RESEND_API_KEY=tu_clave_de_resend_aqui
```

### 5. Ejecutar la API

```bash
python api.py
```

Por defecto corre en el puerto `5000`. Puedes acceder a `http://localhost:5000/test-connection` para verificar que esté funcionando.

---

## Endpoints

### `GET /test-connection`

Prueba de conexión para verificar si la API está corriendo correctamente.

#### Respuesta

```json
{
    "status": "ok",
    "message": "Conexión exitosa con la API de OrderEat 🚀"
}
```

---

### `POST /send-intern-email`

Envía un correo electrónico interno al equipo de OrderEAT con los datos del formulario de contacto.

#### Headers

```
Content-Type: application/json
```

#### Body (JSON)

```json
{
    "fromName": "Nombre del remitente",
    "fromEmail": "email@ejemplo.com",
    "fromPhone": "+56912345678",
    "fromSchool": "Nombre del colegio",
    "fromPosition": "Cargo del remitente",
    "fromMessage": "Mensaje enviado desde el formulario"
}
```

#### Respuesta exitosa

```json
{
    "message": "Correo interno enviado a ordereat ✅",
    "status": "ok"
}
```

#### Respuesta con error

```json
{
    "error": "❌ No se pudo enviar el correo interno"
}
```

---

### `POST /send-thanks-email`

Envía un correo de agradecimiento al remitente después de completar el formulario de contacto.

#### Headers

```
Content-Type: application/json
```

#### Body (JSON)

```json
{
    "fromName": "Nombre del remitente",
    "fromEmail": "email@ejemplo.com"
}
```

#### Respuesta exitosa

```json
{
    "message": "Correo de agradecimiento enviado correctamente ✅"
}
```

#### Respuesta con error

```json
{
    "error": "No se pudo enviar el correo de agradecimiento ❌. Error: {str(e)}"
}
```

---

## Variables de entorno necesarias

La API requiere las siguientes variables de entorno:

- `RESEND_API_KEY`: Clave API para autenticar el envío de correos mediante Resend.

Estas variables deben ser definidas en un archivo `.env` en el mismo directorio que el script principal.

---

## Templates de correo

- `templates/intern-email/intern-email.html`: HTML para el correo interno al equipo OrderEAT.
- `templates/thanks-email/thanks-email.html`: HTML para el correo de agradecimiento al remitente.

---

## Logs útiles

La API imprime en consola el **Origin** de cada solicitud recibida y confirma el envío de correos o los errores correspondientes.

---

## Seguridad y CORS

La API permite solicitudes desde los siguientes orígenes (configurado vía `flask_cors`):

```python
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5001", "null"]}})
```

---

## Licencia

Esta API es propiedad de OrderEAT y está diseñada para su uso exclusivo dentro del ecosistema de productos de OrderEAT.

---

## Autoría

Esta API está creada y desarrollada por [🌶️chilisites](https://chilisites.com/)