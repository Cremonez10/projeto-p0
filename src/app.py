import sys
from src.client import enviar_prompt_llm

def executar_cli():
    print("=" * 60)
    print(" 📝 FORMATADOR DE ATAS DE REUNIÃO (SOFTEX P0)")
    print("=" * 60)
    print("Digite ou cole as anotações da sua reunião abaixo.")
    print("Para encerrar o programa, digite 'sair' e aperte Enter.\n")

    while True:
        # 1. Captura a entrada do usuário no terminal
        entrada_usuario = input("\n[Entrada] Digite as anotações: ").strip()

        # 2. Valida se o usuário quer sair do programa
        if entrada_usuario.lower() == 'sair':
            print("\nEncerrando o programa... Até logo!")
            sys.exit(0)

        # 3. Validação de segurança: Impede o envio de entradas vazias
        if not entrada_usuario:
            print("⚠️ [Aviso]: A entrada não pode estar vazia. Tente novamente.")
            continue

        print("\n⏳ Enviando solicitação para o Gemini... Aguarde...")
        
        # 4. Chama o nosso client.py e recebe o resultado
        resultado = enviar_prompt_llm(entrada_usuario)

        # 5. Apresenta o resultado formatado na tela
        print("\n" + "=" * 60)
        print(" 📌 RESULTADO FORMATADO DA ATA:")
        print("=" * 60)
        print(resultado)
        print("=" * 60)

if __name__ == "__main__":
    executar_cli()