# Projeto P0 — Assistente de Atas com LLM

Aplicação de terminal em Python que usa um modelo de linguagem para organizar
anotações de reuniões em decisões, ações e pendências.

## Instalação no Windows

Pré-requisito mínimo do projeto: Python 3.10 ou superior.

Na raiz do projeto, em uma cópia recém-clonada, execute no PowerShell:

```powershell
# Cria um ambiente virtual para isolar as dependências do projeto.
python -m venv .venv

# Ativa o ambiente virtual no PowerShell.
.\.venv\Scripts\Activate.ps1

# Instala as dependências listadas no projeto.
python -m pip install -r requirements.txt

# Cria o arquivo de configuração local a partir do modelo.
Copy-Item .env.example .env
```

## Configuração e execução

Preencha `LLM_API_BASE_URL`, `LLM_API_KEY` e `LLM_MODEL` no arquivo `.env`.
Mantenha a chave real apenas na configuração local.

```powershell
# Inicia a aplicação a partir da raiz do projeto.
python -m src.app
```

Digite suas anotações no terminal. Para encerrar, digite `sair`.