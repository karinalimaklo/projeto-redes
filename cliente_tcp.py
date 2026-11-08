import socket
import time

from config import NOME_HOST, NOME_PORTA, TCP_NOME
from protocolo import localizar_servico

def executar_calculadora():
    print("---> CALCULADORA TCP <---")

    operacao = input(
        "Digite a operacao (SOMA, SUB, MULT, DIV): "
    ).strip().upper()

    a = input("Primeiro valor: ").strip()
    b = input("Segundo valor: ").strip()

    mensagem = f"{operacao}|{a}|{b}\n"

    # Primeiro: localizar o servico
    print("\nConsultando servidor de nomes...")

    try:
        endereco = localizar_servico(
            NOME_HOST,
            NOME_PORTA,
            TCP_NOME
        )

    except OSError as erro:
        print(f"Erro ao consultar servidor de nomes: {erro}")
        return

    if endereco is None:
        print("Servico nao encontrado.")
        return

    ip, porta = endereco

    print(f"Servico encontrado em {ip}:{porta}")

    # Segundo: conectar diretamente ao servico
    cliente = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    try:
        cliente.connect((ip, porta))

        inicio = time.perf_counter()

        cliente.sendall(mensagem.encode("utf-8"))

        arquivo = cliente.makefile("r", encoding="utf-8")

        resposta = arquivo.readline()

        fim = time.perf_counter()

        if not resposta:
            print("Servidor encerrou a conexao sem responder.")
            return

        print(f"\nResultado: {resposta.strip()}")

        tempo = (fim - inicio) * 1000

        print(f"Tempo da requisicao: {tempo:.4f} ms")

    except OSError as erro:
        print(f"Erro na comunicacao: {erro}")

    finally:
        cliente.close()

if __name__ == "__main__":
    executar_calculadora()