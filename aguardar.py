"""
Aguarda um componente ficar pronto (usado pelo Makefile).

Uso:
    python3 aguardar.py nomes             -> espera o servidor de nomes aceitar conexoes
    python3 aguardar.py <nome_do_servico> -> espera o servico aparecer registrado

Garante a ordem de execucao: o servidor de nomes precisa estar no ar
antes de os servidores TCP/UDP tentarem se registrar nele.
"""

import socket
import sys
import time

from config import NOME_HOST, NOME_PORTA
from protocolo import localizar_servico

LIMITE_SEGUNDOS = 10
INTERVALO = 0.2


def pronto(alvo):
    try:
        if alvo == "nomes":
            socket.create_connection((NOME_HOST, NOME_PORTA), timeout=1).close()
            return True

        return localizar_servico(NOME_HOST, NOME_PORTA, alvo) is not None

    except OSError:
        return False


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 aguardar.py <nomes|nome_do_servico>")
        sys.exit(2)

    alvo = sys.argv[1]
    limite = time.monotonic() + LIMITE_SEGUNDOS

    while time.monotonic() < limite:
        if pronto(alvo):
            sys.exit(0)
        time.sleep(INTERVALO)

    print(f"Tempo esgotado aguardando '{alvo}'.")
    sys.exit(1)


if __name__ == "__main__":
    main()
