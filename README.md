# Urban Routes – Proyecto de Automatización QA

## Descripción del Proyecto
Este proyecto contiene pruebas automatizadas de interfaz (UI) para la aplicación web **Urban Routes**, una plataforma utilizada para solicitar viajes en taxi.

Las pruebas simulan el comportamiento real de un usuario y validan el flujo principal de solicitud de un viaje, incluyendo:

- Configurar direcciones de origen y destino
- Seleccionar la tarifa Comfort
- Agregar y confirmar un número de teléfono
- Agregar una tarjeta de crédito
- Escribir un mensaje para el conductor
- Solicitar opciones adicionales del viaje
- Pedir un taxi y verificar la información del conductor

El objetivo del proyecto es asegurar que los flujos críticos del usuario funcionen correctamente mediante pruebas automatizadas.

---

## Tecnologías Utilizadas
- **Python**
- **Selenium WebDriver**
- **pytest**
- **Page Object Model (POM)**
- Esperas explícitas (`WebDriverWait`)
- Automatización de formularios y ventanas modales

---
## Cómo Ejecutar las Pruebas
### 1. Iniciar el servidor Urban Routes
Antes de ejecutar las pruebas, debes iniciar el servidor proporcionado por TripleTen.

Al iniciar el servidor, se generará una **URL única** de Urban Routes.

### 2. Configurar la URL en `data.py`
Abre el archivo `data.py` y reemplaza la URL base con la URL generada al iniciar el servidor:
```python
urban_routes_url = "PEGA_AQUI_LA_URL_DEL_SERVIDOR"
```
### 3. Instalar dependencias
pip install selenium pytest

### 4. Asegúrate de tener:

- Google Chrome instalado
- ChromeDriver compatible disponible en el PATH del sistema

### 5. Ejecutar todas las pruebas
```bash
  pytest main.py -v
```

### 6. Ejecutar una prueba específica
Ejemplo:
``` bash 
    pytest Draft_main.py::TestUrbanRoutes::test_set_route -v 
```
---

## Cobertura de Pruebas

Las pruebas automatizadas validan los siguientes escenarios:
1. Configurar direcciones del recorrido
2. Seleccionar tarifa Comfort
3. Introducir número de teléfono y código de confirmación
4. Agregar método de pago con tarjeta 
5. Escribir mensaje para el conductor 
6. Activar opción de manta y pañuelos 
7. Agregar dos helados 
8. Solicitar un taxi 
9. Validar el modal con la información del conductor (opcional)

---

## Notas

* Los datos de prueba se almacenan en `data.py` para facilitar el mantenimiento.

* La función `retrieve_phone_code()` captura automáticamente el código de confirmación del teléfono desde los registros del navegador.

* Las pruebas siguen buenas prácticas de automatización QA para mejorar la legibilidad y escalabilidad.