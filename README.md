# Comparação de desempenho entre TCP e UDP

Projeto desenvolvido para a disciplina de Redes de Computadores, com o objetivo de implementar e comparar a comunicação entre cliente e servidor utilizando os protocolos TCP e UDP.

## Sobre o projeto

O sistema implementa uma aplicação de calculadora distribuída, na qual os clientes podem executar operações matemáticas por meio de dois protocolos de comunicação: TCP e UDP.

A arquitetura utiliza um **servidor de nomes**, responsável por registrar e localizar os serviços disponíveis. Dessa forma, antes de estabelecer a comunicação com a calculadora, o cliente consulta o servidor de nomes para descobrir o endereço IP e a porta do serviço desejado.

### Arquitetura

O projeto é composto por três servidores:

- **Servidor de nomes:** mantém uma tabela em memória associando o nome de cada serviço ao seu endereço IP e porta.
- **Servidor TCP:** recebe requisições dos clientes por meio de conexões TCP e executa operações matemáticas.
- **Servidor UDP:** recebe datagramas UDP e executa as mesmas operações matemáticas do servidor TCP.

Os dois servidores de calculadora compartilham a mesma lógica de processamento, permitindo comparar os protocolos utilizando a mesma aplicação.

### Operações disponíveis

- SOMA
- SUBTRAÇÃO
- MULTIPLICAÇÃO
- DIVISÃO

O sistema também realiza validações para operações inválidas, valores não numéricos e divisão por zero.

## Tecnologias utilizadas

- Python 3
- Sockets (`socket`)
- Threads (`threading`)
- TCP
- UDP
- CSV

Não são utilizadas bibliotecas externas para a comunicação em rede.

## Estrutura do projeto

```text
projeto-redes/
│
├── benchmark.py
├── calculadora.py
├── cliente_tcp.py
├── cliente_udp.py
├── config.py
├── protocolo.py
│
├── servidor_nomes.py
├── servidor_tcp.py
├── servidor_udp.py
│
├── teste_servico_inexistente.py
├── resultados_benchmark.csv
│
├── aguardar.py
├── Makefile
└── README.md
```

## Configurações de rede

O projeto utiliza os seguintes endereços e portas:

| Serviço | Endereço | Porta |
|---|---|---|
| Servidor de nomes | 127.0.0.1 | 5000 |
| Calculadora TCP | 127.0.0.1 | 5001 |
| Calculadora UDP | 127.0.0.1 | 5002 |

As configurações podem ser alteradas no arquivo `config.py`.

## Como executar

### 1. Pré-requisitos

- Python 3 instalado.
- Terminal ou prompt de comando.
- Os arquivos do projeto disponíveis localmente.

Não é necessário instalar dependências externas.

### 2. Execução com Makefile (recomendado)

O `Makefile` sobe os servidores na ordem correta (servidor de nomes → TCP → UDP), esperando cada um ficar pronto antes de iniciar o próximo (via `aguardar.py`). Os servidores rodam em segundo plano e sua saída fica em `logs/`.

```bash
make servidores     # sobe servidor de nomes, TCP e UDP
make cliente-tcp    # cliente TCP (interativo)
make cliente-udp    # cliente UDP (interativo)
make inexistente    # teste de serviço inexistente
make benchmark      # comparação TCP x UDP
make status         # mostra quais servidores estão rodando
make logs           # mostra a saída dos servidores
make parar          # encerra os servidores
```

Também é possível rodar tudo de uma vez (servidores + teste de serviço inexistente + benchmark) com `make demo`.

Para acompanhar cada servidor em um terminal separado (útil para os prints), use `make nomes`, `make tcp` e `make udp`, nessa ordem, cada um em um terminal.

> **Windows:** o Makefile usa comandos de shell do Linux/macOS (`nohup`, `kill`) e não funciona no PowerShell ou no Prompt de Comando. No Windows, use o WSL ou o Git Bash com `make` instalado, ou siga a execução manual abaixo.

### 3. Execução manual (sem Makefile)

Abra três terminais, na pasta do projeto. Em sistemas Linux, use `python3` no lugar de `python`.

**Terminal 1 — Servidor de nomes**

```bash
python servidor_nomes.py
```

**Terminal 2 — Servidor TCP**

```bash
python servidor_tcp.py
```

**Terminal 3 — Servidor UDP**

```bash
python servidor_udp.py
```

Os servidores de calculadora realizarão automaticamente o registro de seus serviços no servidor de nomes.

#### Executar os clientes

Com os três servidores em execução, abra outro terminal.

**Cliente TCP**

```bash
python cliente_tcp.py
```

**Cliente UDP**

```bash
python cliente_udp.py
```

Os clientes consultam o servidor de nomes antes de enviar suas requisições aos servidores de calculadora.

### 4. Testar serviço inexistente

Para verificar o tratamento de serviços que não estão registrados, execute:

```bash
python teste_servico_inexistente.py
```

O cliente deverá identificar que o serviço não foi encontrado sem interromper sua execução por uma falha inesperada.

### 5. Executar o benchmark

Com todos os servidores em execução, execute:

```bash
python benchmark.py
```

O benchmark realiza requisições utilizando TCP e UDP, calcula estatísticas dos tempos de resposta e salva os resultados no arquivo `resultados_benchmark.csv`.

São calculadas as seguintes métricas:

- Tempo médio;
- Mediana;
- Tempo mínimo;
- Tempo máximo;
- Desvio padrão;
- Quantidade de sucessos e falhas.

## Resultados do benchmark

Foram realizadas 100 requisições para cada protocolo, utilizando a mesma operação matemática e os mesmos valores de entrada.

| Métrica | TCP | UDP |
|---|---:|---:|
| Requisições bem-sucedidas | 100 | 100 |
| Falhas | 0 | 0 |
| Tempo médio | 0,404557 ms | 0,471742 ms |
| Mediana | 0,376800 ms | 0,431650 ms |
| Mínimo | 0,182000 ms | 0,296300 ms |
| Máximo | 1,194600 ms | 0,840800 ms |
| Desvio padrão | 0,150954 ms | 0,127635 ms |

Nos testes realizados localmente, o TCP apresentou menor tempo médio de resposta, enquanto o UDP apresentou menor desvio padrão.

É importante destacar que o tempo de estabelecimento da conexão TCP não foi incluído nas medições. Os resultados representam o intervalo entre o envio da requisição e o recebimento da resposta.

## Autores

- Isabela Maria de Moura Nascimento
- Karina Lima de Oliveira
- Kauanny Karolinna D'Avalon Araújo e Barros
