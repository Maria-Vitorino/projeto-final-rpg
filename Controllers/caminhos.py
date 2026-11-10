"""Centraliza os caminhos absolutos do projeto."""
from pathlib import Path

# caminhos.py fica em Controllers; parents[1] aponta para a raiz.
PASTA_PROJETO = Path(__file__).resolve().parents[1]
ASSETS_DIR = PASTA_PROJETO / "Views" / "assets"
PASTA_BANCO_DADOS = PASTA_PROJETO / "Data"
PASTA_DADOS_BACKEND = PASTA_PROJETO / "Models" / "dados"
ARQUIVO_SALVAMENTO = PASTA_PROJETO / "savegame.json"

def caminho_recurso(*parts: str) -> Path:
    return ASSETS_DIR.joinpath(*parts)
