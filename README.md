# Proyecto: Sistema de Recomendación de Películas con FastAPI

## Presentación del Proyecto

Este proyecto consiste en el desarrollo de un sistema de recomendación de películas implementado como una API utilizando el framework FastAPI de Python. El objetivo principal es ofrecer a los usuarios la posibilidad de descubrir películas similares a aquellas que les han interesado previamente, facilitando la exploración del catálogo cinematográfico.

Se ha explorado un enfoques para la recomendación:

**Recomendación Simple Basada en Géneros:** Un método inicial que identifica la similitud entre películas basándose en la cantidad de géneros que comparten.

La API construida permite interactuar con este sistema de recomendación a través de endpoints HTTP, devolviendo listas de películas recomendadas en formato JSON.

## Trabajo Realizado

El trabajo realizado en este proyecto se puede resumir en las siguientes etapas:

**1. Exploración y Análisis de Datos (EDA):**

* Se realizó un análisis inicial del dataset de películas para comprender su estructura, tipos de datos y posibles valores faltantes.
* Se exploró la distribución de variables numéricas clave como presupuesto, ingresos, popularidad y promedio de votos a través de histogramas y boxplots.
* Se analizó la popularidad de los géneros más frecuentes en el dataset.
* Se investigó la distribución de las fechas de lanzamiento de las películas a lo largo del tiempo (por año, mes y día de la semana).
* Se generaron visualizaciones interesantes como nubes de palabras de los títulos de las películas y mapas de calor de la co-ocurrencia de géneros para extraer información relevante.
* Se realizó el procesamiento de columnas como 'genres' para facilitar el análisis y la implementación del sistema de recomendación.

**2. Desarrollo del Sistema de Recomendación:**

* **Recomendación Simple Basada en Géneros:** Se implementó una función que toma el título de una película y recomienda otras películas basándose en la cantidad de géneros que tienen en común.

**3. Construcción de la API con FastAPI:**

* Se creó una API utilizando el framework FastAPI para exponer la funcionalidad del sistema de recomendación a través de endpoints HTTP.
* Se definieron rutas (endpoints) para recibir el título de una película y devolver una lista de recomendaciones en formato JSON.
* Se implementó la carga del dataset al inicio de la aplicación para que esté disponible para las solicitudes.

**4. Integración del Sistema de Recomendación en la API:**

* Se integraron las funciones de recomendación dentro de las rutas de la API para que puedan ser llamadas al recibir solicitudes.

**5. Documentación y Presentación:**

* Se ha elaborado este archivo `README.md` para presentar el proyecto, el trabajo realizado, las funcionalidades de la API, las tecnologías utilizadas y las instrucciones para la ejecución.

## Tecnologías Utilizadas

* **Python:** Lenguaje de programación principal.
* **FastAPI:** Framework web moderno y de alto rendimiento para construir APIs.
* **Pandas:** Librería para la manipulación y análisis de datos.
* **`ast`:** Módulo para la manipulación de estructuras de datos literales (parsing de columnas).
* **Matplotlib y Seaborn:** Librerías para la visualización de datos durante la etapa de EDA.
* **Uvicorn:** Servidor ASGI para ejecutar la aplicación FastAPI.

## Conclusiones

Se ha logrado desarrollar un sistema de recomendación de películas funcional y desplegable como una API utilizando FastAPI. El análisis exploratorio de datos fue fundamental para comprender el dataset y guiar el desarrollo del sistema de recomendación.

La API construida permite a los usuarios obtener recomendaciones de películas de manera sencilla a través de solicitudes HTTP. Este proyecto sienta las bases para futuras mejoras y la exploración de técnicas de recomendación más avanzadas.