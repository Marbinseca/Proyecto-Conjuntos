import tornado.ioloop
import tornado.web
import tornado.escape
import google.generativeai as genai
import os
import sys
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3 # Para diagramas de 2 o 3 conjuntos
import io
import base64
import re

# Carga la API Key desde el archivo .env

print("--- DIAGNÓSTICO DE ENTORNO ---")
print(f"Python Executable: {sys.executable}")
print(f"Versión de google-generativeai: {genai.__version__}")
print("-----------------------------")

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Configuración del modelo de Gemini
generation_config = {
  "temperature": 0.2,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}
model = genai.GenerativeModel('gemini-1.5-flash-latest', generation_config=generation_config)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/index.html")

class SolveHandler(tornado.web.RequestHandler):
    async def post(self):
        try:
            problem_text = self.get_body_argument("problem", default="")
            if not problem_text:
                self.set_status(400)
                self.write({"error": "Por favor, ingresa un problema."})
                return

            # 1. Llamar a la IA para obtener la solución en texto
            solution_text = self._call_gemini(problem_text)

            # 2. Extraer los datos numéricos del texto de la solución
            data = self._parse_solution_data(solution_text)
            if not data:
                # Si no se pudieron extraer datos, enviar la explicación de la IA sin diagrama.
                self.write({
                    "solution": solution_text,
                    "diagram": None,
                    "warning": "No se pudieron extraer datos numéricos para generar el diagrama."
                })
                return

            # 3. Generar el Diagrama de Venn a partir de los datos
            venn_diagram_base64 = self.create_venn_diagram(data)

            # 4. Enviar la respuesta completa como JSON
            self.write({
                "solution": solution_text,
                "diagram": venn_diagram_base64
            })

        except Exception as e:
            self.set_status(500)
            self.write({"error": f"Error al procesar la solicitud: {e}"})

    def _call_gemini(self, problem_text: str) -> str:
        """Construye el prompt y se comunica con la API de Gemini."""
        prompt = f"""
        Resuelve el siguiente problema de lógica de conjuntos paso a paso.
        Problema: "{problem_text}"

        Al final, proporciona un resumen numérico claro con cada valor en una nueva línea y usando las siguientes claves exactas:
        CONJUNTO_A: [valor_solo_A]
        CONJUNTO_B: [valor_solo_B]
        CONJUNTO_C: [valor_solo_C]
        INTERSECCION_AB: [valor_interseccion]
        INTERSECCION_AC: [valor_interseccion]
        INTERSECCION_BC: [valor_interseccion]
        INTERSECCION_ABC: [valor_interseccion]
        UNIVERSO: [valor_total]
        FUERA: [valor_fuera_de_los_conjuntos]
        """
        response = model.generate_content(prompt)
        return response.text

    def _parse_solution_data(self, solution_text: str) -> dict:
        """Extrae los datos numéricos del texto de la solución usando expresiones regulares."""
        data = {}
        # Regex para encontrar líneas como "CLAVE_EJEMPLO: 123"
        matches = re.findall(r"^\s*([A-Z_]+):\s*(\d+)\s*$", solution_text, re.MULTILINE)
        for key, value in matches:
            data[key.strip()] = int(value.strip())
        return data

    def create_venn_diagram(self, data: dict) -> str:
        """Genera un diagrama de Venn para 2 o 3 conjuntos y lo devuelve como una imagen en base64."""
        plt.figure(figsize=(8, 6))

        # Detecta si es un problema de 3 conjuntos
        set_c_keys = {"CONJUNTO_C", "INTERSECCION_AC", "INTERSECCION_BC", "INTERSECCION_ABC"}
        is_three_sets = any(key in data for key in set_c_keys)

        if is_three_sets:
            subsets = (
                data.get("CONJUNTO_A", 0), data.get("CONJUNTO_B", 0), data.get("INTERSECCION_AB", 0),
                data.get("CONJUNTO_C", 0), data.get("INTERSECCION_AC", 0), data.get("INTERSECCION_BC", 0),
                data.get("INTERSECCION_ABC", 0)
            )
            venn3(subsets=subsets, set_labels=('Conjunto A', 'Conjunto B', 'Conjunto C'))
        else:
            subsets = (
                data.get("CONJUNTO_A", 0), data.get("CONJUNTO_B", 0), data.get("INTERSECCION_AB", 0)
            )
            venn2(subsets=subsets, set_labels=('Conjunto A', 'Conjunto B'))

        # Guardar la imagen en memoria
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        
        # Codificar en Base64 para enviarla al frontend
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close()
        
        return f"data:image/png;base64,{image_base64}" # Devuelve la imagen codificada


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/solve", SolveHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
    ], debug=True, autoreload=False) # Cambiado para evitar conflictos de puerto

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Servidor corriendo en http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()