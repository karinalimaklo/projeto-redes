def calcular(mensagem):

    partes = mensagem.strip().split("|")

    if len(partes) != 3:
        return "ERROR|Formato invalido"

    operacao = partes[0]

    try:
        a = float(partes[1])
        b = float(partes[2])

    except ValueError:
        return "ERROR|Valores numericos invalidos"

    if operacao == "SOMA":
        resultado = a + b

    elif operacao == "SUB":
        resultado = a - b

    elif operacao == "MULT":
        resultado = a * b

    elif operacao == "DIV":

        if b == 0:
            return "ERROR|Divisao por zero"

        resultado = a / b

    else:
        return "ERROR|Operacao desconhecida"

    return f"{resultado:.10g}"