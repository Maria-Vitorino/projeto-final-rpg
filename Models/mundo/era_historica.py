"""Representa uma era histórica e seus recursos."""

from dataclasses import dataclass


@dataclass(frozen=True)
class EraHistorica:

    chave: str
    nome: str
    periodo: str
    introducao: str
    objetivo: str
    arquivo_mapa: str
    arquivo_introducao: str
    posicao_inicial: tuple[int, int]
    posicoes_npcs: tuple[tuple[int, int], ...]