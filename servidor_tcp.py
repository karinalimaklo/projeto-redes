import socket
import threading

from config import (
    NOME_HOST,
    NOME_PORTA,
    TCP_HOST,
    TCP_PORTA,
    TCP_NOME
)

from protocolo import registrar_servico

from calculadora import calcular

def atender_cliente(conexao, endereco):
    print(f"Cliente conectado: {endereco}")

    try:
        arquivo = conexao.makefile("r", encoding="utf-8")

        mensagem = arquivo.readline()

        if mensagem:
            resposta = calcular(mensagem)

            conexao.sendall(
                (resposta + "\n").encode("utf-8")
            )

            print(f"Requisicao: {mensagem.strip()}")
            print(f"Resposta: {resposta}")

    except OSError as erro:
        print(f"Erro na conexao: {erro}")

    finally:
        conexao.close()

def iniciar_servidor():
    servidor = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    servidor.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    servidor.bind((TCP_HOST, TCP_PORTA))

    servidor.listen()

    print("Servidor TCP iniciado")

    # Registro no servidor de nomes
    resposta = registrar_servico(
        NOME_HOST,
        NOME_PORTA,
        TCP_NOME,
        TCP_HOST,
        TCP_PORTA
    )

    if resposta != "OK":
        servidor.close()
        raise RuntimeError(
            f"Falha ao registrar servico: {resposta}"
        )

    print(f"Servico registrado: {TCP_NOME}")
    print(f"Escutando em {TCP_HOST}: {TCP_PORTA}")

    while True:
        conexao, endereco = servidor.accept()

        thread = threading.Thread(
            target = atender_cliente,
            args = (conexao, endereco)
        )

        thread.start()

if __name__ == "__main__":
    iniciar_servidor()