# Azure Function Capturadora de TRM

Esta Azure Function obtiene automáticamente la TRM (Tasa Representativa del Mercado - tipo de cambio del peso colombiano frente al dólar estadounidense) diaria desde la Superintendencia Financiera de Colombia y la envía a un webhook, como Power Automate o Logic Apps.

## Características

* **Obtención Automatizada de TRM**: Obtiene el valor oficial de la TRM diariamente.
* **Análisis de Datos (Parsing)**: Extrae el valor de la TRM del código HTML de la página de la Superintendencia Financiera.
* **Ejecución Programada**: Se ejecuta según una programación predefinida utilizando un Azure Functions Timer Trigger.

## Detalles Técnicos

* **Fuente de Datos**: [Superintendencia Financiera de Colombia](https://www.superfinanciera.gov.co/jsp/index.jsf).
* **Disparador de la Función (Trigger)**: Disparador de temporizador (Timer Trigger). La programación por defecto en `function_app.py` está configurada para ejecutarse todos los días a las 8:00 AM UTC (3:00 AM Hora Colombia, UTC-5).
    * Expresión CRON: `0 0 8 * * *`.

## Prerrequisitos

* [Python](https://www.python.org/downloads/) (Versión 3.9 o superior).
* [Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local).
* Una cuenta de Azure con una suscripción activa.
* La URL de un webhook (Power Automate, Logic Apps, etc.) para recibir los datos.

## Instalación y Configuración

1.  **Clonar el Repositorio**:
    ```bash
    git clone <url-de-tu-repositorio>
    cd <directorio-del-repositorio>
    ```

2.  **Crear un Entorno Virtual**:
    Se recomienda encarecidamente usar un entorno virtual.
    ```bash
    python -m venv .venv
    ```
    Activa el entorno:
    * Windows: `.venv\Scripts\activate`
    * macOS/Linux: `source .venv/bin/activate`

3.  **Instalar Dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

## Desarrollo Local y Pruebas

1.  **Configurar Variables Locales**:
    Para el desarrollo local, Azure Functions utiliza el archivo `local.settings.json` para gestionar las variables de entorno. Crea este archivo en la raíz del proyecto si no existe.

    **Contenido de `local.settings.json`**:
    ```json
    {
      "IsEncrypted": false,
      "Values": {
        "AzureWebJobsStorage": "UseDevelopmentStorage=true",
        "FUNCTIONS_WORKER_RUNTIME": "python",
        "URL_POST": "TU_URL_DEL_WEBHOOK_AQUI"
      }
    }
    ```
    **Importante**: El archivo `.gitignore` ya está configurado para ignorar `local.settings.json` y así evitar que la URL del webhook se suba al control de versiones.

2.  **Ejecutar la Función Localmente**:
    Usa las Azure Functions Core Tools para iniciar el host de la función.
    ```bash
    func start
    ```
    La herramienta mostrará una URL que puedes usar para activar manualmente la función con fines de prueba sin tener que esperar a la hora programada.

## Despliegue en Azure

Puedes desplegar esta función en Azure usando la [extensión de Azure Functions para VS Code](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python) o con el [Azure CLI](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python).

**Configurar el Webhook en Azure**:
Después de desplegar, debes configurar la URL del webhook de forma segura en la configuración de la aplicación.

1.  En el portal de Azure, ve a tu Function App.
2.  Ve a **Configuración > Configuración de la aplicación**.
3.  En la sección de **Configuración de la aplicación**, añade un nuevo ajuste:
    * **Nombre**: `URL_POST`
    * **Valor**: `TU_URL_DEL_WEBHOOK_AQUI`
4.  Guarda los cambios. La función ahora leerá esta variable de entorno en lugar de usar el valor de `local.settings.json`.

## Estructura de Archivos

```
├── .vscode/
├── .venv/
├── function_app.py      # Lógica principal de la función y disparador
├── requirements.txt     # Dependencias de Python
├── host.json            # Configuración del host de Azure Functions
├── local.settings.json  # Configuración local (ignorado por git)
├── README.md            # Este archivo
└── .gitignore
```

## Manejo de Errores y Registro (Logging)

* El script incluye registro de información para el seguimiento de la ejecución y la captura de errores.
* Se registran errores si la solicitud a la página de la TRM falla o si el envío de datos al webhook no es exitoso.
* Los registros se pueden monitorear en la consola local durante las pruebas o en Application Insights cuando la función está desplegada en Azure.

## Contribuciones

¡Las contribuciones son bienvenidas! Siéntete libre de abrir un *issue* o enviar un *pull request*.