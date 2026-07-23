"""LLM client for ClipMind - supports multiple providers."""

import requests
import json


class LLMClient:
    """Client for interacting with various LLM providers."""

    def __init__(self, config):
        self.provider = config.get("provider", "deepseek")
        self.api_key = config.get("api_key", "")
        self.model = config.get("model", "deepseek-chat")
        self.base_url = config.get("base_url", "https://api.deepseek.com/v1")
        self.language = config.get("language", "es")

    def ask(self, system_prompt, user_text):
        """Send a prompt to the configured LLM provider."""
        if self.provider == "deepseek":
            return self._call_openai_compatible(system_prompt, user_text)
        elif self.provider == "openai":
            return self._call_openai_compatible(system_prompt, user_text)
        elif self.provider == "ollama":
            return self._call_ollama(system_prompt, user_text)
        else:
            raise ValueError(f"Provider '{self.provider}' not supported")

    def _call_openai_compatible(self, system_prompt, user_text):
        """Call any OpenAI-compatible API (DeepSeek, OpenAI, etc.)."""
        url = f"{self.base_url}/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            "temperature": 0.3,
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except requests.exceptions.Timeout:
            raise RuntimeError("La solicitud tardó demasiado. Verifica tu conexión.")
        except requests.exceptions.ConnectionError:
            raise RuntimeError("No se pudo conectar con el servidor. Verifica tu conexión a internet.")
        except requests.exceptions.HTTPError:
            if response.status_code == 401:
                raise RuntimeError("API key inválida. Verifica tu configuración.")
            elif response.status_code == 429:
                raise RuntimeError("Demasiadas solicitudes. Espera un momento.")
            else:
                raise RuntimeError(f"Error HTTP {response.status_code}: {response.text}")
        except (KeyError, json.JSONDecodeError):
            raise RuntimeError("Respuesta inesperada del servidor.")

    def _call_ollama(self, system_prompt, user_text):
        """Call Ollama running locally."""
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            return data["message"]["content"]
        except requests.exceptions.ConnectionError:
            raise RuntimeError("No se pudo conectar con Ollama. ¿Está instalado y ejecutándose?")
        except Exception as e:
            raise RuntimeError(f"Error con Ollama: {e}")

    def test_connection(self):
        """Test if the provider is reachable."""
        try:
            result = self.ask("Responde solo 'OK'", "test")
            return True, result
        except Exception as e:
            return False, str(e)


# System prompts for each action
SYSTEM_PROMPTS = {
    "resumir": (
        "Eres un asistente que resume texto de forma clara y concisa. "
        "Resume el siguiente texto en español, capturando las ideas principales. "
        "Sé directo y no añadas información que no esté en el texto original."
    ),
    "traducir": (
        "Eres un traductor profesional. Traduce el siguiente texto al español. "
        "Mantén el tono y estilo original. Solo devuelve la traducción, sin explicaciones."
    ),
    "explicar": (
        "Eres un tutor experto. Explica el siguiente texto de forma clara y didáctica. "
        "Usa ejemplos si es necesario. Asume que el usuario quiere entender el concepto "
        "a fondo pero sin jerga innecesaria."
    ),
    "responder": (
        "Eres un asistente útil. Genera una respuesta apropiada al siguiente texto. "
        "Si es una pregunta, respóndela. Si es un mensaje, responde como si fueras el usuario. "
        "Sé natural y directo."
    )
}
