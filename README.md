# Azure Function Capturadora de TRM

Esta Azure Function obtiene automáticamente la TRM (Tasa Representativa del Mercado - tipo de cambio del peso colombiano frente al dólar estadounidense) diaria desde la Superintendencia Financiera de Colombia y la envía a un espacio de trabajo de Azure Log Analytics.

## Características

* **Obtención Automatizada de TRM**: Obtiene el valor oficial de la TRM diariamente.
* **Análisis de Datos (Parsing)**: Extrae el valor de la TRM del código HTML de la página de la Superintendencia Financiera.
* **Ejecución Programada**: Se ejecuta según una programación predefinida utilizando un Azure Functions Timer Trigger (normalmente los días de semana).
* **Integración con Azure Log Analytics**: Envía los datos de la TRM recuperados a Azure Log Analytics para monitoreo, alertas o análisis posteriores.

## Detalles Técnicos

* **Fuente de Datos**: [Superintendencia Financiera de Colombia](https://www.superfinanciera.gov.co/jsp/index.jsf) (específicamente la página de consulta de la TRM).
* **Disparador de la Función (Trigger)**: Disparador de temporizador (Timer Trigger). La programación por defecto en `function_app.py` está configurada para ejecutarse a la 1:00 PM UTC (8:00 AM Hora Colombia, asumiendo UTC-5) de lunes a viernes.
    * Expresión CRON: `0 0 13 * * 1-5`

## Prerrequisitos

* [Python](https://www.python.org/downloads/) (Versión 3.9 o superior recomendada)
* [Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local) (para desarrollo y pruebas locales)
* Una Cuenta de Azure con una suscripción activa.
* Un Espacio de Trabajo de Azure Log Analytics y su URL del Extremo de Recopilación de Datos (Data Collection Endpoint).

## Instalación y Configuración

1.  **Clonar el Repositorio**:
    ```bash
    git clone <url-de-tu-repositorio>
    cd <directorio-del-repositorio>
    ```

2.  **Crear un Entorno Virtual**:
    Es altamente recomendado usar un entorno virtual para proyectos de Python.
    ```bash
    python -m venv .venv
    ```
    Activa el entorno virtual:
    * Windows:
        ```bash
        .venv\Scripts\activate
        ```
    * macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```

3.  **Instalar Dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar el Extremo de Log Analytics (URL_POST)**:
    * Crea un nuevo archivo llamado `config.py` en el directorio raíz del proyecto (el mismo directorio que `trmApp.py` y `function_app.py`).
    * Añade la URL de tu Extremo de Recopilación de Datos de Azure Log Analytics a este archivo:
        ```python
        # config.py
        URL_POST = "TU_URL_DEL_EXTREMO_DE_RECOLECCION_DE_DATOS_DE_LOG_ANALYTICS"
        ```
        Reemplaza `"TU_URL_DEL_EXTREMO_DE_RECOLECCION_DE_DATOS_DE_LOG_ANALYTICS"` con tu URL real. Esta URL se utiliza para ingerir datos en tu espacio de trabajo de Log Analytics.

    * **Importante**: Añade `config.py` a tu archivo `.gitignore` para evitar que tu URL sensible se envíe al control de versiones:
        ```gitignore
        # .gitignore

        # Configuración
        config.py

        # Python
        *.pyc
        __pycache__/
        .venv/
        ```

## Desarrollo Local y Pruebas

1.  **Asegúrate de que `local.settings.json` esté configurado si es necesario**:
    Azure Functions podría requerir un archivo `local.settings.json` para ciertas configuraciones, especialmente al tratar con integraciones de servicios de Azure directamente (aunque en esta configuración, `URL_POST` se maneja mediante `config.py`). Si estuvieras utilizando la configuración de la aplicación para `URL_POST`, iría aquí.

    Ejemplo de `local.settings.json` (si tuvieras otras configuraciones):
    ```json
    {
      "IsEncrypted": false,
      "Values": {
        "AzureWebJobsStorage": "UseDevelopmentStorage=true", // O tu cadena de conexión de Azure Storage
        "FUNCTIONS_WORKER_RUNTIME": "python"
        // "URL_POST": "tu_url_aqui" // Alternativa si no usas config.py
      }
    }
    ```
    *Nota: Añade `local.settings.json` a tu `.gitignore` también si contiene información sensible.*

2.  **Ejecutar la Función Localmente**:
    Usa Azure Functions Core Tools para iniciar el host de la función:
    ```bash
    func start
    ```
    La función se activará según su programación si la dejas en ejecución, o a menudo puedes activar funciones de temporizador manualmente para pruebas a través de un extremo local proporcionado por `func start` (revisa la salida de la terminal).

## Despliegue en Azure

Puedes desplegar esta función en Azure utilizando varios métodos:

* **Extensión de Azure Functions para VS Code**: [Desplegar usando VS Code](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python)
* **Azure CLI**: [Desplegar usando Azure CLI](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python)
* **GitHub Actions / Azure DevOps**: Para pipelines de CI/CD.

Al desplegar, asegúrate de que la configuración de tu aplicación en Azure incluya cualquier ajuste necesario. Si estás utilizando el método `config.py` para `URL_POST`, este archivo debe ser parte de tu paquete de despliegue, o deberías configurar `URL_POST` como una Configuración de Aplicación (Application Setting) en la Azure Function App en Azure. Usar la Configuración de Aplicación en Azure es generalmente la forma recomendada para entornos desplegados.

**Uso de la Configuración de Aplicación en Azure para `URL_POST`:**
Si prefieres utilizar la Configuración de Aplicación de Azure Function App (que es más seguro para entornos desplegados):
1.  En `trmApp.py`, modifica cómo se accede a `URL_POST`:
    ```python
    import os
    # ... otras importaciones ...

    # Obtener URL_POST de la variable de entorno (Configuración de Aplicación en Azure)
    # Respaldo a config.py para desarrollo local si lo deseas
    try:
        from config import URL_POST as FALLBACK_URL_POST
    except ImportError:
        FALLBACK_URL_POST = None

    URL_POST = os.environ.get("URL_POST", FALLBACK_URL_POST)

    if not URL_POST:
        # Manejar el caso en que URL_POST no esté configurada, ej. lanzar un error o registrar una advertencia
        print("Error: URL_POST no está configurada. Por favor, configúrala como una variable de entorno o en config.py para uso local.")
        # Potencialmente salir o deshabilitar el envío de datos si URL_POST es crítica
    ```
2.  En el portal de Azure, ve a tu Function App > Configuración > Configuración de la aplicación y añade una nueva configuración de aplicación:
    * **Nombre**: `URL_POST`
    * **Valor**: `TU_URL_DEL_EXTREMO_DE_RECOLECCION_DE_DATOS_DE_LOG_ANALYTICS`

## Estructura de Archivos

├── .vscode/                  # Configuración de VS Code (opcional)
├── .venv/                    # Entorno virtual de Python (ignorado por git)
├── function_app.py           # Disparador de Azure Function y punto de entrada principal
├── trmApp.py                 # Lógica principal para obtener la TRM y enviar datos
├── config.py                 # Configuración para URL_POST (local, ignorado por git)
├── requirements.txt          # Dependencias de Python
├── host.json                 # Configuración del host de Azure Functions
├── local.settings.json       # Configuración de desarrollo local (ignorado por git si es sensible)
├── README.md                 # Este archivo
└── .gitignore                # Especifica archivos no rastreados intencionalmente que Git debe ignorar

## Manejo de Errores y Registro (Logging)

* El script incluye manejo básico de errores para solicitudes de red y análisis de datos.
* Los mensajes de registro se imprimen en la consola (y aparecerán en los registros de Azure Functions) indicando éxito o fracaso.
* La función `send_to_log_analytics` registra el estado del envío de datos a Log Analytics.

## Contribuciones

¡Las contribuciones son bienvenidas! Por favor, siéntete libre de enviar un pull request o abrir un issue.