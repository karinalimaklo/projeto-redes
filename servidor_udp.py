import socket
import threading

from config import (
    NOME_HOST,
    NOME_PORTA,
    UDP_HOST,
    UDP_PORTA,
    UDP_NOME
)

from protocolo import registrar_servico
from calculadora import calcular

def atender_requisicao(servidor, mensagem, endereco):
    try:
        texto = mensagem.decode("utf-8")

        resposta = calcular(texto)

        servidor.sendto(
            resposta.encode("utf-8"),
            endereco
        )

        print(f"Cliente: {endereco}")
        print(f"Requisicao: {texto.strip()}")
        print(f"Resposta: {resposta}")

    except (UnicodeDecodeError, OSError) as erro:
        print(f"Erro ao processar requisicao: {erro}")

def iniciar_servidor():
    servidor = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    servidor.bind((UDP_HOST, UDP_PORTA))

    print("Servidor UDP iniciado")

    # Registro no servidor de nomes
    resposta = registrar_servico(
        NOME_HOST,
        NOME_PORTA,
        UDP_NOME,
        UDP_HOST,
        UDP_PORTA
    )

    if resposta != "OK":
        servidor.close()
        raise RuntimeError(
            f"Falha ao registrar servico: {resposta}"
        )

    print(f"Servico registrado: {UDP_NOME}")
    print(f"Escutando em {UDP_HOST}:{UDP_PORTA}")

    while True:

        mensagem, endereco = servidor.recvfrom(1024)

        thread = threading.Thread(
            target=atender_requisicao,
            args=(servidor, mensagem, endereco)
        )

        thread.start()

if __name__ == "__main__":
    iniciar_servidor()