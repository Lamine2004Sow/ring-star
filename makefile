VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
SYSTEM_PYTHON = python3

.PHONY: help install clean run

f ?= ulysses16.tsp
p ?= 5


help:
	@echo "--- Makefile SAÉ Optimisation (Mode Venv) ---"
	@echo "Commandes disponibles :"
	@echo "  make install                 : Crée le venv et installe les dépendances"
	@echo "  make run f=fichier p=stations: Lance la résolution"
	@echo "  make clean                   : Nettoie les fichiers temporaires"

install:
	@echo "--- Création de l'environnement virtuel (Mode manuel) ---"
	rm -rf $(VENV)
	$(SYSTEM_PYTHON) -m venv $(VENV) --without-pip
	@echo "--- Installation de pip à l'intérieur du venv ---"
	curl -sS https://bootstrap.pypa.io/get-pip.py | $(PYTHON)
	@echo "--- Installation des dépendances ---"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "--- Installation terminée ! ---"

clean:
	rm -rf __pycache__ src/__pycache__ $(VENV)
	rm -f *.pyc src/*.pyc

run:
	$(PYTHON) main.py $(f) $(p)
