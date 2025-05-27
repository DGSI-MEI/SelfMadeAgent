import requests
import time
import socket
import ssl
from datetime import datetime

DEEPSEEK_API_KEY = "sk-45273889dcbe407480bb5f35931d01f4"  # Reemplaza con tu API key real
API_URL = "https://api.deepseek.com/v1/chat/completions"

class DebuggableDeepSeekAgent:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }

    def get_response(self, question: str) -> str:
        """Versión con diagnóstico extendido de errores"""
        print(f"\n[Debug] Iniciando solicitud a las {datetime.now().isoformat()}")
        
        # Diagnóstico de red preliminar
        self._network_diagnosis()

        try:
            # Intento principal con verificación SSL
            return self._make_api_call(
                system="Responde de forma concisa",
                user=question,
                mode="normal"
            )
        except Exception as e:
            # Registro detallado del error
            error_info = self._get_connection_error_details(e)
            print("\n⚠️ [Error Detallado] ⚠️")
            print(f"Tipo: {type(e).__name__}")
            print(f"Mensaje: {str(e)}")
            print(f"Timestamp: {datetime.now().isoformat()}")
            print("\n[Diagnóstico]:")
            print(error_info)
            
            # Intento alternativo sin verificación SSL
            try:
                print("\nIntentando conexión insegura (sin verificación SSL)...")
                return self._make_api_call(
                    system="Responde brevemente",
                    user=question,
                    mode="insecure"
                )
            except Exception as fallback_e:
                return self._generate_local_fallback(question, error_info)

    def _make_api_call(self, system: str, user: str, mode: str) -> str:
        """Llamada API con logging detallado"""
        print(f"\n[Modo: {mode}] Preparando solicitud...")
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            "max_tokens": 500
        }

        try:
            start_time = time.time()
            response = self.session.post(
                API_URL,
                json=payload,
                verify=(mode == "normal"),  # Solo verifica SSL en modo normal
                timeout=10
            )
            response_time = time.time() - start_time

            print(f"[Debug] HTTP Status: {response.status_code}")
            print(f"[Debug] Tiempo respuesta: {response_time:.2f}s")
            
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']

        except requests.exceptions.SSLError as e:
            print("[Debug] Error SSL:", str(e))
            raise
        except requests.exceptions.ConnectionError as e:
            print("[Debug] ConnectionError detalles:")
            self._log_socket_error(e)
            raise
        except Exception as e:
            print(f"[Debug] Error inesperado: {type(e).__name__}")
            raise

    def _network_diagnosis(self):
        """Ejecuta pruebas de conectividad"""
        print("\n[Diagnóstico de Red]")
        
        # Prueba DNS
        try:
            ip = socket.gethostbyname("api.deepseek.com")
            print(f"✅ DNS Resuelto: {ip}")
        except socket.gaierror:
            print("🚨 Fallo DNS - No se puede resolver la dirección")

        # Prueba TCP
        try:
            with socket.create_connection(("api.deepseek.com", 443), timeout=5):
                print("✅ Conexión TCP/443 exitosa")
        except socket.timeout:
            print("🚨 Timeout en conexión TCP")
        except ConnectionRefusedError:
            print("🚨 Conexión rechazada (puerto bloqueado?)")

        # Prueba SSL
        try:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(
                socket.socket(), 
                server_hostname="api.deepseek.com"
            ) as s:
                s.connect(("api.deepseek.com", 443))
                print(f"✅ SSL válido. Certificado: {s.version()}")
        except ssl.SSLError as e:
            print(f"🚨 Error SSL: {e}")

    def _log_socket_error(self, error):
        """Log específico para ConnectionError"""
        if isinstance(error, requests.exceptions.ConnectionError):
            print("Posibles causas:")
            print("- Firewall bloqueando la conexión")
            print("- Problemas con el proxy")
            print("- API no disponible")
            print("- Limitación de red local")

    def _get_connection_error_details(self, error) -> str:
        """Genera informe detallado del error"""
        error_map = {
            'ConnectionError': "Fallo en la conexión física con el servidor",
            'SSLError': "Problema con el certificado SSL/TLS",
            'Timeout': "El servidor no respondió a tiempo",
            'ProxyError': "Fallo en la conexión a través del proxy"
        }
        
        error_type = type(error).__name__
        return error_map.get(error_type, f"Error desconocido: {error_type}")

    def _generate_local_fallback(self, question: str, error_info: str) -> str:
        """Respuesta local con detalles técnicos"""
        return f"""
        ⚠️ Error de conexión con DeepSeek API
        ----------------------------
        Pregunta: {question[:100]}
        Error: {error_info}
        Hora: {datetime.now().isoformat()}
        
        Soluciones sugeridas:
        1. Verifica tu conexión a Internet
        2. Intenta desactivar el firewall temporalmente
        3. Prueba usando una red diferente
        """

def main():
    agent = DebuggableDeepSeekAgent()
    
    while True:
        question = input("\nTu pregunta (o 'salir'): ").strip()
        if question.lower() == 'salir':
            break

        print("\n" + "="*50)
        response = agent.get_response(question)
        print("\n[RESPUESTA FINAL]")
        print(response)
        print("="*50 + "\n")

if __name__ == "__main__":
    main()