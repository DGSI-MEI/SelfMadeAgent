import requests
import datetime
import os
from typing import Tuple, List

# Configuración de API Key
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

class DeepSeekImprovementAgent:
    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.max_iterations = 3  # Máximo de mejoras iterativas

    def process_question(self, question: str) -> str:
        """Proceso completo de mejora iterativa"""
        # Generar respuesta inicial
        current_response, improvements = self.generate_initial_response(question)
        print(f"\n[Iteración 1] Respuesta inicial generada con {len(improvements)} puntos de mejora")
        
        # Mejora iterativa
        for iteration in range(self.max_iterations):
            improved_response = self.generate_improved_response(current_response, improvements)
            new_improvements = self.analyze_response(improved_response)
            
            # Verificar si quedan mejoras por aplicar
            if not new_improvements or iteration == self.max_iterations - 1:
                print(f"\n[Mejoras completadas] Iteración final: {iteration + 1}")
                return improved_response
                
            # Actualizar para siguiente iteración
            current_response = improved_response
            improvements = new_improvements
            print(f"\n[Iteración {iteration + 2}] Aplicando nuevas mejoras...")
            
        return current_response

    def generate_initial_response(self, question: str) -> Tuple[str, List[str]]:
        """Genera respuesta inicial con puntos de mejora"""
        response = self._call_api(
            system="Eres un asistente experto que genera respuestas técnicas detalladas",
            user=question
        )
        improvements = self._call_api(
            system="Analiza esta respuesta y genera 3 puntos de mejora específicos",
            user=f"Respuesta a mejorar:\n{response}"
        )
        return response, self._parse_improvements(improvements)

    def generate_improved_response(self, response: str, improvements: List[str]) -> str:
        """Genera versión mejorada de la respuesta"""
        prompt = f"""Mejora esta respuesta implementando TODOS estos puntos:
        {chr(10).join(improvements)}
        
        Respuesta actual:
        {response}"""
        
        return self._call_api(
            system="Eres un editor experto que implementa mejoras específicas",
            user=prompt
        )

    def analyze_response(self, response: str) -> List[str]:
        """Identifica nuevas mejoras potenciales"""
        analysis = self._call_api(
            system="Identifica 2-3 mejoras específicas para esta respuesta",
            user=response
        )
        return self._parse_improvements(analysis)

    def _call_api(self, system: str, user: str) -> str:
        """Llama a la API de DeepSeek"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            "temperature": 0.5,
            "max_tokens": 2000
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error en la API: {e}")
            return ""

    @staticmethod
    def _parse_improvements(text: str) -> List[str]:
        """Extrae puntos de mejora de la respuesta de la API"""
        return [line.split('. ', 1)[1] for line in text.split('\n') if '. ' in line][:3]

def main():
    agent = DeepSeekImprovementAgent()
    
    question = input("Ingresa tu pregunta: ")
    
    # Proceso completo de mejoras
    final_response = agent.process_question(question)
    
    print("\n--- RESPUESTA FINAL ---")
    print(final_response)
    print("\nProceso completado satisfactoriamente!")

if __name__ == "__main__":
    main()