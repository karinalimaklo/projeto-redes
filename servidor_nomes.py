import socket
import threading

from config import NOME_HOST, NOME_PORTA

# Tabela de serviços registrados
servicos = {}

# Protege a tabela contra acessos simultâneos
lock = threading.Lock()

def processar_mensagem(mensagem):
    partes = mensagem.strip().split("|")

    if partes[0] == "REGISTER":
        if len(partes) != 4:
            return "ERROR|Mensagem de registro invalida\n"

        nome = partes[1]
        ip = partes[2]

        try:
            porta = int(partes[3])

            if not nome or not ip or not 1 <= porta <= 65535:
                return "ERROR|Dados invalidos\n"

        except ValueError:
            return "ERROR|Porta invalida\n"

        with lock:
            servicos[nome] = (ip, porta)

        print(f"Servico registrado: {nome} -> {ip}:{porta}")

        return "OK\n"

    elif partes[0] == "LOOKUP":
        if len(partes) != 2 or not partes[1]:
            return "ERROR|Consulta invalida\n"

        nome = partes[1]

        with lock:
            endereco = servicos.get(nome)

        if endereco is None:
            return "ERROR|Servico nao encontrado\n"

        ip, porta = endereco

        return f"FOUND|{ip}|{porta}\n"
    
    else:
        return "ERROR|Comando desconhecido\n"

def atender_cliente(conexao, endereco):
    print(f"Nova conexao de {endereco}")

    try:
        arquivo = conexao.makefile("r", encoding="utf-8")

        mensagem = arquivo.readline()

        if mensagem:
            resposta = processar_mensagem(mensagem)
            conexao.sendall(resposta.encode("utf-8"))

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

    servidor.bind((NOME_HOST, NOME_PORTA))

    servidor.listen()

    print("Servidor de nomes iniciado")
    print(f"Executando em {NOME_HOST}:{NOME_PORTA}")

    while True:
        conexao, endereco = servidor.accept()

        thread = threading.Thread(
            target = atender_cliente,
            args = (conexao, endereco)
        )

        thread.start()

if __name__ == "__main__":
    iniciar_servidor()