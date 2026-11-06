import os
import requests
from dotenv import load_dotenv

# Carrega as variaveis do cofre secreto .env
load_dotenv()

def enviar_prompt_llm(prompt: str) -> str:
    """
    Envia uma solicitacao textual para a API REST do Gemini e retorna a resposta formatada.
    """
    api_key = os.getenv("LLM_API_KEY")
    model = os.getenv("LLM_MODEL", "gemini-1.5-flash")

    if not api_key or api_key == "sua_chave_do_google_ai_studio_aqui":
        return "Erro de Autenticação (401): A chave LLM_API_KEY nao foi configurada corretamente no arquivo .env."

    # Endpoint nativo da API REST do Google AI Studio (Gemini)
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

    system_prompt = (
        "Transforme o texto recebido em topicos curtos de Atas de Reuniao em Portugues do Brasil. "
        "Retorne estritamente as tres secoes: ## Decisoes, ## Acoes e ## Pendencias."
    )

    # Payload estruturado para o contrato de API do Gemini
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"{system_prompt}\n\nTexto a analisar:\n{prompt}"}
                ]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": 500  # Evita resposta truncada (Obstaculo 2 do curso)
        }
    }

    try:
        response = requests.post(endpoint, json=payload, headers=headers, timeout=30)

        if response.status_code == 200:
            dados = response.json()
            # Extrai o texto gerado da estrutura de resposta do Gemini
            candidates = dados.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "Nenhum texto retornado.")
            return "Resposta recebida com formato inesperado."
        elif response.status_code == 401:
            return "Erro de Autenticação (401): A chave de API fornecida e invalida ou expirou."
        elif response.status_code == 429:
            return "Erro de Limite de Requisições (429): Voce atingiu o limite de taxa da API."
        else:
            return f"Erro HTTP {response.status_code}: {response.text}"

    except requests.exceptions.Timeout:
        return "Erro de Conexão: A API do LLM demorou muito para responder (Timeout de 30s excedido)."
    except requests.exceptions.ConnectionError:
        return "Erro de Conexão: Nao foi possivel conectar ao servidor da API."
    except requests.exceptions.RequestException as e:
        return f"Erro na chamada da API: {str(e)}"