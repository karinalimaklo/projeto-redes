# Makefile - Projeto Cliente-Servidor (TCP/UDP) - CIN154
#
# Ordem de execucao:
#   1. servidor de nomes  (porta 5000)
#   2. servidor TCP       (porta 5001) -> registra "calculadora_tcp"
#   3. servidor UDP       (porta 5002) -> registra "calculadora_udp"
#   4. clientes / teste de servico inexistente / benchmark
#
# Uso rapido:
#   make servidores    sobe os 3 servidores em segundo plano, na ordem certa
#   make cliente-tcp   executa o cliente TCP (interativo)
#   make cliente-udp   executa o cliente UDP (interativo)
#   make parar         derruba os servidores

PYTHON ?= python3
PY      = $(PYTHON) -u
LOGS    = logs
PIDS    = .pids

TCP_NOME = calculadora_tcp
UDP_NOME = calculadora_udp

.PHONY: help servidores nomes tcp udp cliente-tcp cliente-udp inexistente \
        benchmark demo status logs parar limpar

help:
	@echo "Alvos disponiveis:"
	@echo "  make servidores   - sobe servidor de nomes, TCP e UDP (em segundo plano, nessa ordem)"
	@echo "  make cliente-tcp  - executa o cliente TCP (interativo)"
	@echo "  make cliente-udp  - executa o cliente UDP (interativo)"
	@echo "  make inexistente  - testa a resolucao de um servico nao registrado"
	@echo "  make benchmark    - compara tempos TCP x UDP e gera resultados_benchmark.csv"
	@echo "  make demo         - servidores + teste de servico inexistente + benchmark"
	@echo "  make status       - mostra quais servidores estao rodando"
	@echo "  make logs         - mostra a saida dos servidores"
	@echo "  make parar        - encerra os servidores"
	@echo "  make limpar       - encerra os servidores e apaga logs/cache"
	@echo ""
	@echo "Para ver cada servidor em um terminal separado (primeiro plano):"
	@echo "  make nomes   ->   make tcp   ->   make udp"

# --------------------------------------------------------------------
# Servidores em segundo plano
# --------------------------------------------------------------------

# $(1) = identificador, $(2) = script, $(3) = alvo para o aguardar.py
define iniciar
	@mkdir -p $(LOGS) $(PIDS)
	@if [ -f $(PIDS)/$(1).pid ] && kill -0 $$(cat $(PIDS)/$(1).pid) 2>/dev/null; then \
		echo "[$(1)] ja esta em execucao (PID $$(cat $(PIDS)/$(1).pid))"; \
	else \
		nohup $(PY) $(2) > $(LOGS)/$(1).log 2>&1 & echo $$! > $(PIDS)/$(1).pid; \
		if $(PYTHON) aguardar.py $(3); then \
			echo "[$(1)] pronto (PID $$(cat $(PIDS)/$(1).pid)) - log em $(LOGS)/$(1).log"; \
		else \
			echo "[$(1)] falhou ao iniciar. Saida:"; cat $(LOGS)/$(1).log; \
			kill $$(cat $(PIDS)/$(1).pid) 2>/dev/null; rm -f $(PIDS)/$(1).pid; \
			exit 1; \
		fi; \
	fi
endef

servidores:
	$(call iniciar,nomes,servidor_nomes.py,nomes)
	$(call iniciar,tcp,servidor_tcp.py,$(TCP_NOME))
	$(call iniciar,udp,servidor_udp.py,$(UDP_NOME))
	@echo "Servidores no ar. Use 'make cliente-tcp' ou 'make cliente-udp'."

# --------------------------------------------------------------------
# Servidores em primeiro plano (um por terminal, util para demonstracao)
# --------------------------------------------------------------------

nomes:
	$(PY) servidor_nomes.py

tcp:
	@$(PYTHON) aguardar.py nomes || (echo "Suba antes o servidor de nomes (make nomes)"; exit 1)
	$(PY) servidor_tcp.py

udp:
	@$(PYTHON) aguardar.py nomes || (echo "Suba antes o servidor de nomes (make nomes)"; exit 1)
	$(PY) servidor_udp.py

# --------------------------------------------------------------------
# Clientes
# --------------------------------------------------------------------

cliente-tcp:
	@$(PYTHON) cliente_tcp.py

cliente-udp:
	@$(PYTHON) cliente_udp.py

inexistente:
	@$(PYTHON) teste_servico_inexistente.py

benchmark:
	@$(PYTHON) benchmark.py

demo: servidores
	@echo ""
	@$(MAKE) --no-print-directory inexistente
	@echo ""
	@$(MAKE) --no-print-directory benchmark

# --------------------------------------------------------------------
# Utilitarios
# --------------------------------------------------------------------

status:
	@for s in nomes tcp udp; do \
		if [ -f $(PIDS)/$$s.pid ] && kill -0 $$(cat $(PIDS)/$$s.pid) 2>/dev/null; then \
			echo "[$$s] rodando (PID $$(cat $(PIDS)/$$s.pid))"; \
		else \
			echo "[$$s] parado"; \
		fi; \
	done

logs:
	@for s in nomes tcp udp; do \
		echo "===== $$s ====="; \
		cat $(LOGS)/$$s.log 2>/dev/null || echo "(sem log)"; \
	done

parar:
	@for s in udp tcp nomes; do \
		if [ -f $(PIDS)/$$s.pid ]; then \
			kill $$(cat $(PIDS)/$$s.pid) 2>/dev/null && echo "[$$s] encerrado"; \
			rm -f $(PIDS)/$$s.pid; \
		fi; \
	done

limpar: parar
	rm -rf $(LOGS) $(PIDS) __pycache__
