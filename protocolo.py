import socket

# Padronizando a comunicação
def criar_registro(nome, ip, porta):
    return f"REGISTER|{nome}|{ip}|{porta}\n"

def criar_consulta(nome):
    return f"LOOKUP|{nome}\n"

def enviar_requisicao_tcp(host, porta, mensagem):
    cliente = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    try:
        cliente.connect((host, porta))

        cliente.sendall(mensagem.encode("utf-8"))

        arquivo = cliente.makefile("r", encoding="utf-8")

        resposta = arquivo.readline()

        return resposta.strip()

    finally:
        cliente.close()

def registrar_servico(host, porta, nome, ip, porta_servico):
    mensagem = criar_registro(nome, ip, porta_servico)

    return enviar_requisicao_tcp(host, porta, mensagem)

def localizar_servico(host, porta, nome):
    mensagem = criar_consulta(nome)

    resposta = enviar_requisicao_tcp(host, porta, mensagem)

    partes = resposta.split("|")

    if len(partes) == 3 and partes[0] == "FOUND":
        return partes[1], int(partes[2])

    return None