from config import NOME_HOST, NOME_PORTA
from protocolo import localizar_servico


def testar_servico_inexistente():

    nome = "servico_que_nao_existe"

    print("=== TESTE DE SERVICO INEXISTENTE ===")

    try:

        endereco = localizar_servico(
            NOME_HOST,
            NOME_PORTA,
            nome
        )

        if endereco is None:
            print("SUCESSO: servico nao encontrado.")
            print("O cliente tratou corretamente a resposta.")

        else:
            print(f"ERRO: servico encontrado em {endereco}")

    except OSError as erro:
        print(f"Falha na comunicacao: {erro}")


if __name__ == "__main__":
    testar_servico_inexistente()