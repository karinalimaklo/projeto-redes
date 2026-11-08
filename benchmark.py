import socket
import time
import csv
import statistics

from config import (
    NOME_HOST,
    NOME_PORTA,
    TCP_NOME,
    UDP_NOME
)

from protocolo import localizar_servico


# Configuracoes do experimento
QUANTIDADE_TESTES = 100
AQUECIMENTO = 5

OPERACAO = "SOMA"
VALOR_A = 10
VALOR_B = 20

TIMEOUT = 3


def medir_tcp(ip, porta, mensagem):

    cliente = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    try:
        cliente.settimeout(TIMEOUT)
        cliente.connect((ip, porta))

        arquivo = cliente.makefile(
            "r",
            encoding="utf-8"
        )

        inicio = time.perf_counter()

        cliente.sendall(mensagem.encode("utf-8"))

        resposta = arquivo.readline()

        fim = time.perf_counter()

        if not resposta:
            raise RuntimeError("Servidor TCP nao respondeu")

        tempo = (fim - inicio) * 1000

        return tempo

    finally:
        cliente.close()


def medir_udp(ip, porta, mensagem):

    cliente = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    cliente.settimeout(TIMEOUT)

    try:

        inicio = time.perf_counter()

        cliente.sendto(
            mensagem.encode("utf-8"),
            (ip, porta)
        )

        resposta, endereco = cliente.recvfrom(1024)

        fim = time.perf_counter()

        if not resposta:
            raise RuntimeError("Resposta UDP vazia")

        tempo = (fim - inicio) * 1000

        return tempo

    finally:
        cliente.close()


def aquecer(protocolo, ip, porta, mensagem):

    print(f"Aquecendo {protocolo}...")

    for _ in range(AQUECIMENTO):

        if protocolo == "TCP":
            medir_tcp(ip, porta, mensagem)

        else:
            medir_udp(ip, porta, mensagem)


def executar_benchmark():

    mensagem = f"{OPERACAO}|{VALOR_A}|{VALOR_B}\n"

    print("=== BENCHMARK TCP X UDP ===")

    # Descobrir os enderecos dos servicos
    print("\nLocalizando servicos...")

    try:
        endereco_tcp = localizar_servico(
            NOME_HOST,
            NOME_PORTA,
            TCP_NOME
        )

        endereco_udp = localizar_servico(
            NOME_HOST,
            NOME_PORTA,
            UDP_NOME
        )

    except OSError as erro:
        print(f"Erro ao consultar servidor de nomes: {erro}")
        return

    if endereco_tcp is None or endereco_udp is None:
        print("Nao foi possivel localizar os dois servicos.")
        return

    ip_tcp, porta_tcp = endereco_tcp
    ip_udp, porta_udp = endereco_udp

    print(f"TCP: {ip_tcp}:{porta_tcp}")
    print(f"UDP: {ip_udp}:{porta_udp}")

    # Aquecimento
    try:
        aquecer("TCP", ip_tcp, porta_tcp, mensagem)
        aquecer("UDP", ip_udp, porta_udp, mensagem)

    except (OSError, RuntimeError) as erro:
        print(f"Erro durante aquecimento: {erro}")
        return

    tempos_tcp = []
    tempos_udp = []

    falhas_tcp = 0
    falhas_udp = 0

    registros = []

    print("\nIniciando testes...")

    for i in range(QUANTIDADE_TESTES):

        # Alterna a ordem dos protocolos para reduzir
        # o efeito de uma ordem fixa no experimento.
        protocolos = ["TCP", "UDP"]

        if i % 2 == 1:
            protocolos.reverse()

        for protocolo in protocolos:

            try:

                if protocolo == "TCP":

                    tempo = medir_tcp(
                        ip_tcp,
                        porta_tcp,
                        mensagem
                    )

                    tempos_tcp.append(tempo)

                else:

                    tempo = medir_udp(
                        ip_udp,
                        porta_udp,
                        mensagem
                    )

                    tempos_udp.append(tempo)

                registros.append([
                    protocolo,
                    i + 1,
                    f"{tempo:.6f}",
                    "SUCESSO"
                ])

            except (OSError, RuntimeError) as erro:

                if protocolo == "TCP":
                    falhas_tcp += 1
                else:
                    falhas_udp += 1

                registros.append([
                    protocolo,
                    i + 1,
                    "",
                    "FALHA"
                ])

                print(f"{protocolo} - Teste {i + 1}: {erro}")

    # Salvar resultados brutos
    with open(
        "resultados_benchmark.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        escritor = csv.writer(arquivo)

        escritor.writerow([
            "Protocolo",
            "Teste",
            "Tempo_ms",
            "Status"
        ])

        escritor.writerows(registros)

    # Exibir estatisticas
    print("\n=== RESULTADOS ===")

    def exibir_estatisticas(nome, tempos, falhas):

        print(f"\n{nome}")

        if not tempos:
            print("Nenhuma requisicao concluida.")
            return

        print(f"Sucessos: {len(tempos)}")
        print(f"Falhas: {falhas}")
        print(f"Media: {statistics.mean(tempos):.6f} ms")
        print(f"Mediana: {statistics.median(tempos):.6f} ms")
        print(f"Minimo: {min(tempos):.6f} ms")
        print(f"Maximo: {max(tempos):.6f} ms")

        if len(tempos) > 1:
            print(
                f"Desvio padrao: "
                f"{statistics.stdev(tempos):.6f} ms"
            )

    exibir_estatisticas("TCP", tempos_tcp, falhas_tcp)
    exibir_estatisticas("UDP", tempos_udp, falhas_udp)

    print("\nResultados salvos em resultados_benchmark.csv")


if __name__ == "__main__":
    executar_benchmark()