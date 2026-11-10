import os
import requests
from dotenv import load_dotenv

load_dotenv()

def enviar_prompt_llm(prompt: str) -> str:
    """
    Envia solicitacao REST (OpenAPI) e trata erros HTTP (400/401/403/429) e Timeout amigavelmente.
    """
    base_url = os.getenv("LLM_API_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai")
    api_key = os.getenv("LLM_API_KEY")
    model = os.getenv("LLM_MODEL", "gemini-1.5-flash")

    if not api_key or api_key == "sua_chave_do_google_ai_studio_aqui":
        return "Erro de Autenticação (401): A chave LLM_API_KEY nao foi configurada."

    endpoint = f"{base_url.rstrip('/')}/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system", 
                "content": "Transforme o texto recebido em topicos curtos de Atas de Reuniao. Retorne as secoes: ## Decisoes, ## Acoes e ## Pendencias."
            },
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500  # Evita resposta truncada
    }

    try:
        # Requisição com timeout de segurança de 30 segundos
        response = requests.post(endpoint, json=payload, headers=headers, timeout=30)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        
        # Tratamento amigável para falhas de autenticação/credenciais
        elif response.status_code in (400, 401, 403):
            return "Erro de Autenticação (401): Sua chave de API do LLM institucional é inválida ou expirou."
        
        # Tratamento para limite de requisições excedido
        elif response.status_code == 429:
            return "Erro de Limite (429): Você atingiu o limite de requisições da API."
        
        else:
            return f"Erro HTTP {response.status_code}: Falha ao processar a requisição."

    except requests.exceptions.Timeout:
        return "Erro de Conexão: A API do LLM demorou muito para responder (Timeout)."
    except requests.exceptions.RequestException as e:
        return f"Erro Crítico de Conexão: Não foi possível acessar o servidor."