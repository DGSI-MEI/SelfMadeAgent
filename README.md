# SelfMadeAgent
Agente Pensante – Simulación de Razonamiento

Este proyecto tiene como objetivo crear un **agente pensante**, es decir, una simulación de razonamiento autónomo usando modelos de lenguaje.

La idea central es construir un bucle en el que partimos de un **prompt inicial**, y a partir de las respuestas generadas, el sistema toma decisiones y genera **self-prompts** (prompts hacia sí mismo) para continuar el proceso. Esto imita un ciclo de pensamiento continuo.

## ¿Cómo funciona?

1. Prompt inicial define el objetivo o problema.
2. El modelo responde.
3. El sistema interpreta esa respuesta y genera un nuevo prompt (self-prompt).
4. Se repite el ciclo.

Este proceso permite simular razonamientos complejos a través de pasos encadenados.

---

## Agentes implementados

El proyecto incluye varios agentes temáticos, cada uno con acciones especializadas y siguiendo el patrón ReAct (Reason + Act):

- **Agente de Razón General (ReAct básico):**
  - Ejemplo de razonamiento y acciones simples (como cálculos o consulta de datos ficticios).

- **Recipe Helper (Ayudante de Recetas):**
  - Acciones: sugerir sustitutos de ingredientes, calcular calorías aproximadas de una receta.

- **Weather Helper (Ayudante del Clima):**
  - Acciones: obtener el clima actual y el pronóstico para una ciudad (datos simulados).

- **Finance Helper (Ayudante de Finanzas Personales):**
  - Acciones: convertir monedas (con tasas simuladas), calcular interés simple.

- **Health & Fitness Helper (Salud y Fitness):**
  - Acciones: calcular el IMC (BMI), estimar calorías quemadas en actividades físicas.

Cada agente utiliza el modelo de lenguaje de DeepSeek y un bucle de razonamiento para decidir qué acción ejecutar y cómo avanzar en la conversación.

---

## Estructura de los notebooks

Cada notebook sigue la misma estructura:

1. Definición del agente y sus acciones disponibles.
2. Prompt inicial que explica el ciclo de razonamiento y las acciones.
3. Implementación de las funciones de acción (por ejemplo, `ingredient_substitute`, `current_weather`, `currency_convert`, `bmi_calculate`, etc.).
4. Bucle de interacción que simula el razonamiento paso a paso.
5. Ejemplos de uso para cada agente.

---

## Requisitos

- Python 3.8+
- httpx
- Clave de API de DeepSeek (`DEEPSEEK_API_KEY`)

---

## Ejecución

1. Instala las dependencias:
   ```powershell
   pip install httpx
   ```
2. Define tu clave de API de DeepSeek en el entorno:
   ```powershell
   $env:DEEPSEEK_API_KEY="tu_clave_aqui"
   ```
3. Abre y ejecuta el notebook que desees en Jupyter o VS Code.

---

## Créditos

Inspirado en el patrón ReAct y en [til.simonwillison.net/llms/python-react-pattern](https://til.simonwillison.net/llms/python-react-pattern).
