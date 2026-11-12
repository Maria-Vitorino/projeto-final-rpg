"""Banco SQLite de perguntas com sorteio aleatorio sem repeticao imediata."""

import json
import random
import sqlite3
from pathlib import Path
from Models.desafios.pergunta import Pergunta


class BancoPerguntas:

    def __init__(self, caminho_banco: Path, arquivo_inicial: Path | None = None, semente=None):
        self._caminho_banco = Path(caminho_banco)
        self._arquivo_inicial = Path(arquivo_inicial) if arquivo_inicial else None
        self._aleatorio = random.Random(semente)

        self._perguntas = {}
        self._baralhos = {}
        self._ultima_por_era = {}

        self._inicializar_banco()
        self._carregar_do_banco()

    def _conectar(self):
        self._caminho_banco.parent.mkdir(parents=True, exist_ok=True)

        conexao = sqlite3.connect(self._caminho_banco)
        conexao.execute("PRAGMA foreign_keys = ON")

        return conexao

    def _inicializar_banco(self):

        with self._conectar() as conexao:

            conexao.execute(
                """CREATE TABLE IF NOT EXISTS perguntas (
                    id TEXT PRIMARY KEY,
                    era TEXT NOT NULL,
                    dados_json TEXT NOT NULL
                )"""
            )

            conexao.execute(
                "CREATE INDEX IF NOT EXISTS idx_perguntas_era ON perguntas(era)"
            )

            total = conexao.execute(
                "SELECT COUNT(*) FROM perguntas"
            ).fetchone()[0]

            if total == 0 and self._arquivo_inicial and self._arquivo_inicial.exists():

                dados = json.loads(
                    self._arquivo_inicial.read_text(encoding="utf-8")
                )

                linhas = []

                for era, perguntas in dados.items():

                    for pergunta in perguntas:
                        linhas.append((
                            pergunta["id"],
                            era,
                            json.dumps(pergunta, ensure_ascii=False)
                        ))

                conexao.executemany(
                    "INSERT OR IGNORE INTO perguntas(id, era, dados_json) VALUES (?, ?, ?)",
                    linhas,
                )

    def _carregar_do_banco(self):

        with self._conectar() as conexao:

            linhas = conexao.execute(
                "SELECT era, dados_json FROM perguntas ORDER BY era, id"
            ).fetchall()

        perguntas_agrupadas = {}

        for era, conteudo in linhas:

            perguntas_agrupadas.setdefault(era, []).append(
                Pergunta(json.loads(conteudo))
            )

        eras_necessarias = (
            "grecia",
            "medieval",
            "moderna",
            "contemporanea"
        )

        if not perguntas_agrupadas or any(
            not perguntas_agrupadas.get(era) for era in eras_necessarias
        ):
            raise ValueError(
                "O banco SQLite não contém perguntas para todas as quatro eras."
            )

        self._perguntas = perguntas_agrupadas
        self.reiniciar_sorteio()

    def reiniciar_sorteio(self):
        """Embaralha novamente as perguntas ao iniciar ou reiniciar uma jornada."""

        self._baralhos = {}
        self._ultima_por_era = {}

        for era, perguntas in self._perguntas.items():

            ids_perguntas = [pergunta.id_pergunta for pergunta in perguntas]

            self._aleatorio.shuffle(ids_perguntas)
            self._baralhos[era] = ids_perguntas

    def proxima_pergunta(self, chave_era: str, evitar_id: str | None = None) -> Pergunta:

        perguntas = self._perguntas.get(chave_era, [])

        if not perguntas:
            raise KeyError(
                f"Não existem perguntas cadastradas para a era {chave_era!r}."
            )

        perguntas_por_id = {}

        for pergunta in perguntas:
            perguntas_por_id[pergunta.id_pergunta] = pergunta

        baralho = self._baralhos.setdefault(chave_era, [])

        if not baralho:
            baralho.extend(perguntas_por_id)
            self._aleatorio.shuffle(baralho)

        id_excluido = evitar_id or self._ultima_por_era.get(chave_era)

        if len(baralho) > 1 and baralho[-1] == id_excluido:
            baralho[0], baralho[-1] = baralho[-1], baralho[0]

        id_pergunta = baralho.pop()

        self._ultima_por_era[chave_era] = id_pergunta

        return perguntas_por_id[id_pergunta]

    def contar_perguntas(self, chave_era: str) -> int:
        return len(self._perguntas.get(chave_era, []))
