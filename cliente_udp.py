import socket
import time

from config import NOME_HOST, NOME_PORTA, UDP_NOME
from protocolo import localizar_servico

def executar_calculadora():
    print("---> Calculadora UDP <---")

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
            UDP_NOME
        )

    except OSError as erro:
        print(f"Erro ao consultar servidor de nomes: {erro}")
        return

    if endereco is None:
        print("Servico nao encontrado.")
        return

    ip, porta = endereco

    print(f"Servico encontrado em {ip}:{porta}")

    # Segundo: criar socket UDP
    cliente = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    # Evita que o cliente fique esperando indefinidamente
    cliente.settimeout(3)

    try:
        inicio = time.perf_counter()

        cliente.sendto(
            mensagem.encode("utf-8"),
            (ip, porta)
        )

        resposta, endereco_servidor = cliente.recvfrom(1024)

        fim = time.perf_counter()

        print(f"\nResultado: {resposta.decode('utf-8').strip()}")

        tempo = (fim - inicio) * 1000

        print(f"Tempo da requisicao: {tempo:.4f} ms")

    except socket.timeout:
        print("Tempo esgotado: o servidor UDP nao respondeu.")

    except OSError as erro:
        print(f"Erro na comunicacao: {erro}")

    finally:
        cliente.close()

if __name__ == "__main__":
    executar_calculadora()