# 🧠 Resolutor de Problemas de Conjuntos con IA

Una aplicación web que utiliza la API de Google Gemini para resolver problemas de teoría de conjuntos en lenguaje natural, proporcionando una explicación detallada y generando un diagrama de Venn como visualización.

 
*(Nota: Reemplaza esta URL con una captura de pantalla real de tu aplicación)*

## ✨ Características

- **Resolución por IA:** Envía un problema de conjuntos y obtén una solución paso a paso generada por el modelo `gemini-1.5-flash-latest`.
- **Visualización Gráfica:** Genera automáticamente diagramas de Venn para 2 o 3 conjuntos basados en los datos extraídos de la solución.
- **Interfaz Profesional:** Diseño limpio y moderno construido con Tornado y Tailwind CSS, enfocado en una experiencia de usuario clara y agradable.
- **Backend Asíncrono:** Utiliza el framework asíncrono Tornado para un manejo eficiente de las peticiones a la API de IA.

## 🛠️ Tecnologías Utilizadas

- **Backend:** Python, Tornado
- **Frontend:** HTML, Tailwind CSS, JavaScript
- **Inteligencia Artificial:** Google Gemini API
- **Visualización de Datos:** Matplotlib, Matplotlib-Venn

## 🚀 Instalación y Puesta en Marcha

Sigue estos pasos para ejecutar el proyecto en tu máquina local.

### Prerrequisitos

- Python 3.8 o superior
- Una clave de API de Google para Gemini. Puedes obtenerla en Google AI Studio.

### Pasos

1.  **Clonar el repositorio (o descargar los archivos):**
    ```bash
    git clone https://github.com/Marbinseca/Proyecto-Conjuntos.git
    cd Proyecto-Conjuntos
    ```

2.  **Crear y activar un entorno virtual:**
    Es una buena práctica para aislar las dependencias del proyecto.
    ```bash
    # En Windows
    python -m venv env
    .\env\Scripts\activate

    # En macOS/Linux
    python3 -m venv env
    source env/bin/activate
    ```

3.  **Instalar las dependencias:**
    Este comando leerá el archivo `requirements.txt` e instalará todas las librerías necesarias.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar la clave de API:**
    Crea un archivo llamado `.env` en la raíz del proyecto y añade tu clave de API de Google Gemini:
    ```
    GEMINI_API_KEY="TU_API_KEY_AQUI"
    ```

5.  **Ejecutar la aplicación:**
    ```bash
    python app.py
    ```

6.  Abre tu navegador y ve a `http://localhost:8888` para empezar a usar la aplicación.
