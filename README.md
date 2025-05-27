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
