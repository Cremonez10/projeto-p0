import os

import requests
from dotenv import load_dotenv

load_dotenv()


def enviar_prompt_llm(prompt: str) -> str:
    """
    Envia anotações ao LLM e trata erros HTTP e de conexão.
    """
    base_url = os.getenv(
        "LLM_API_BASE_URL",
        "https://generativelanguage.googleapis.com/v1beta/openai"
    )
    api_key = os.getenv("LLM_API_KEY")
    model = os.getenv("LLM_MODEL", "gemini-1.5-flash")

    if not api_key or api_key == "sua_chave_do_google_ai_studio_aqui":
        return "Erro de Configuração: A chave LLM_API_KEY não foi configurada."

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
                "content": (
                    "Transforme o texto recebido em tópicos curtos "
                    "de atas de reunião. Retorne as seções: "
                    "## Decisões, ## Ações e ## Pendências."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        # Limita a geração; não garante que a resposta fique completa.
        "max_tokens": 500
    }

    try:
        # Define um timeout de 30 segundos para a requisição.
        response = requests.post(
            endpoint,
            json=payload,
            headers=headers,
            timeout=30
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]

        elif response.status_code == 400:
            return (
                "Erro de Requisição (400): "
                "Verifique o modelo e os parâmetros enviados."
            )

        elif response.status_code == 401:
            return (
                "Erro de Autenticação (401): "
                "Verifique sua chave de API."
            )

        elif response.status_code == 403:
            return (
                "Erro de Permissão (403): "
                "Acesso negado ao recurso solicitado."
            )

        elif response.status_code == 429:
            return (
                "Erro de Limite (429): "
                "Limite de requisições ou cota da API atingido."
            )

        else:
            return (
                f"Erro HTTP {response.status_code}: "
                "Falha ao processar a requisição."
            )

    except requests.exceptions.Timeout:
        return (
            "Erro de Conexão: "
            "A API do LLM demorou muito para responder (Timeout)."
        )

    except requests.exceptions.RequestException:
        return (
            "Erro de Conexão: "
            "Não foi possível concluir a comunicação com o servidor."
        )