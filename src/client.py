import os
import requests
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def enviar_prompt_llm(prompt: str) -> str:
    """
    Envia uma solicitacao textual para a API REST do LLM (padrao OpenAPI / Bearer Token)
    e retorna a ata de reuniao formatada nas secoes Decisoes, Acoes e Pendencias.
    """
    # 1. Le as credenciais do cofre .env
    base_url = os.getenv("LLM_API_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai")
    api_key = os.getenv("LLM_API_KEY")
    model = os.getenv("LLM_MODEL", "gemini-1.5-flash")

    # Validação de credenciais de ambiente
    if not api_key or api_key == "sua_chave_do_google_ai_studio_aqui":
        return "Erro de Autenticação (401): A chave LLM_API_KEY nao foi configurada corretamente no arquivo .env."

    # 2. Autenticacao via Cabecalho HTTP (Conformidade C03 / LGPD - Sem chave na URL)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # 3. System Prompt para o Formatador de Atas
    system_prompt = (
        "Transforme o texto recebido em topicos curtos de Atas de Reuniao em Portugues do Brasil. "
        "Retorne estritamente as tres secoes: ## Decisoes, ## Acoes e ## Pendencias."
    )

    # 4. Estrutura o Payload JSON no padrao OpenAPI
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500  # Evita resposta truncada (Obstaculo 2 do curso)
    }

    # 5. Envia a chamada HTTP POST
    endpoint = f"{base_url.rstrip('/')}/chat/completions"

    try:
        response = requests.post(endpoint, json=payload, headers=headers, timeout=30)

        if response.status_code == 200:
            dados = response.json()
            return dados["choices"][0]["message"]["content"]
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