# API de Consulta de Unidad de Fomento (UF)

Una API REST desarrollada con FastAPI que permite consultar los valores históricos de la Unidad de Fomento chilena mediante scraping del sitio web oficial del SII (Servicio de Impuestos Internos).

## 📋 Descripción

Esta aplicación implementa una solución completa para consultar valores de la UF desde 2013 hasta la fecha actual. La API realiza scraping del sitio oficial del SII para obtener los datos en tiempo real, manteniendo la información siempre actualizada.

## ✨ Características

- **API REST** con FastAPI
- **Scraping dinámico** del sitio oficial del SII
- **Validación robusta** de fechas y parámetros
- **Manejo de errores** específicos por dominio
- **Dockerización** completa
- **Testing** unitario con pytest
- **Código limpio** y bien estructurado

## 🚀 Instalación y Uso

### Prerrequisitos

- Python 3.13+
- Docker y Docker Compose (opcional)

### Instalación Local

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/fapro-prueba-tecnica.git
cd fapro-prueba-tecnica
```

2. Crear entorno virtual e instalar dependencias:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Ejecutar la aplicación:
```bash
uvicorn app.main:app --reload --port 8000
```

### Uso con Docker

```bash
docker-compose up --build
```

La API estará disponible en: `http://localhost:8000`

## 📖 Documentación de la API

### Endpoint Principal

**GET** `/uf/{date}`

Consulta el valor de la UF para una fecha específica.

#### Parámetros

- `date` (string): Fecha en formato `YYYY-MM-DD`
  - Fecha mínima: `2013-01-01`
  - Fecha máxima: fecha actual

#### Respuestas

**200 OK**
```json
{
  "date": "2023-01-01",
  "value": "35.122,26"
}
```

**400 Bad Request** - Fecha inválida
```json
{
  "detail": "Invalid date format. Use YYYY-MM-DD"
}
```

**404 Not Found** - UF no encontrada
```json
{
  "detail": "UF value not found for the given date"
}
```

**502 Bad Gateway** - Error del origen de datos
```json
{
  "detail": "Error fetching UF value from source"
}
```

### Documentación Interactiva

Una vez ejecutando la aplicación:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🏗️ Arquitectura

El proyecto sigue principios de **Clean Architecture** con separación clara de responsabilidades:

```
app/
├── main.py              # Punto de entrada de la aplicación
├── api/
│   └── routers/
│       └── router.py    # Definición de endpoints
├── core/
│   └── errors.py        # Excepciones personalizadas
├── uf/
│   ├── scraper.py       # Lógica de scraping del SII
│   ├── service.py       # Lógica de negocio
│   └── validators.py    # Validación de datos
└── tests/
    └── test_router_uf.py # Tests unitarios
```

### Componentes Principales

- **Router**: Maneja las peticiones HTTP y traduce errores de dominio a códigos HTTP
- **Service**: Coordina la validación y obtención de datos
- **Scraper**: Realiza el scraping del sitio del SII
- **Validators**: Valida formato y rangos de fechas
- **Errors**: Excepciones específicas del dominio

## 🧪 Testing

Ejecutar tests:
```bash
pytest app/tests/
```

Ejecutar con cobertura:
```bash
pytest --cov=app app/tests/
```

## 🐳 Docker

### Dockerfile
- Imagen base: `python:3.13-slim`
- Puerto expuesto: `8000`
- Comando: `uvicorn app.main:app --host=0.0.0.0 --port=8000`

### Docker Compose
```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
```

## 🛠️ Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido
- **Requests**: Cliente HTTP para scraping
- **BeautifulSoup4**: Parser HTML para extracción de datos
- **Pydantic**: Validación y serialización de datos
- **Pytest**: Framework de testing
- **Docker**: Containerización

## ⚡ Ejemplo de Uso

### Consultar UF del día de Año Nuevo 2023
```bash
curl http://localhost:8000/uf/2023-01-01
```
Respuesta:
```json
{
  "date": "2023-01-01",
  "value": "35.122,26"
}
```


## 📝 Notas de Implementación

- **Sin Selenium**: Utiliza requests + BeautifulSoup para minimizar consumo de recursos
- **Scraping Dinámico**: Se adapta automáticamente a la estructura HTML del SII
- **Gestión de Errores**: Manejo específico para problemas de red, parsing y datos no encontrados
- **Validación Estricta**: Validación de formato de fecha y rangos permitidos

## 🔗 Referencias

- [Solución alternativa de referencia](https://github.com/LeoLeiva/fapro-with-fastapi-prueba-tecnica)
- [Sitio oficial UF - SII Chile](https://www.sii.cl/valores_y_fechas/uf/)
