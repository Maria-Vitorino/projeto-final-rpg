"""Camada visual do jogo: responsável por desenhar as telas e os elementos."""

import math
import pygame

from  Controllers.caminhos import caminho_recurso


LARGURA, ALTURA = 1280, 720

CREME = (246, 239, 222)
DOURADO = (245, 211, 130)
CINZA = (190, 197, 204)
VERDE = (111, 220, 145)
VERMELHO = (236, 119, 130)
PAINEL = (11, 23, 37)

ESCALAS_PERSONAGEM = {
    "grecia": 1.0,
    "medieval": 1.4,
    "moderna": 0.80,
    "contemporanea": 0.40
}


PERSONAGENS = [
    {
        "id": "kassandra",
        "nome": "Kassandra",
        "classe": "Arqueira",
        "atributos": "Agilidade  •  Precisão",
        "cor": (91, 160, 105)
    },
    {
        "id": "nikos",
        "nome": "Nikos",
        "classe": "Guerreiro",
        "atributos": "Força  •  Defesa",
        "cor": (190, 151, 72)
    },
    {
        "id": "lyra",
        "nome": "Lyra",
        "classe": "Maga",
        "atributos": "Sabedoria  •  Conhecimento",
        "cor": (105, 130, 210)
    },
    {
        "id": "alexandros",
        "nome": "Alexandros",
        "classe": "Explorador",
        "atributos": "Estratégia  •  Astúcia",
        "cor": (135, 145, 160)
    },
]


class RenderizadorJogo:

    def __init__(self):
        pygame.font.init()

        self.fonte = pygame.font.SysFont("arial", 22)
        self.fonte_pequena = pygame.font.SysFont("arial", 17)
        self.fonte_media = pygame.font.SysFont("arial", 29, bold=True)
        self.fonte_grande = pygame.font.SysFont("arial", 46, bold=True)
        self.fonte_titulo = pygame.font.SysFont("georgia", 48, bold=True)

        self.botoes = []
        self.retangulos_personagens = []
        self.retangulo_nome = pygame.Rect(0, 0, 0, 0)

        self.planos_de_fundo = {}
        self.imagens_personagens = {}

        self._carregar_recursos()

    def _carregar_recursos(self):

        arquivos_fundo = [
            "menu.jpg",
            "intro_grecia.jpg",
            "intro_medieval.jpg",
            "intro_moderna.jpg",
            "intro_contemporanea.jpg"
        ]

        for arquivo in arquivos_fundo:

            caminho = caminho_recurso("backgrounds", arquivo)

            try:
                self.planos_de_fundo[arquivo] = pygame.image.load(
                    str(caminho)
                ).convert()

            except (pygame.error, OSError):
                self.planos_de_fundo[arquivo] = None

        arquivos_mapa = [
            "grecia.png",
            "medieval.png",
            "moderna.png",
            "contemporanea.png"
        ]

        for arquivo in arquivos_mapa:

            caminho = caminho_recurso("maps", arquivo)

            try:
                self.planos_de_fundo[arquivo] = pygame.image.load(
                    str(caminho)
                ).convert()

            except (pygame.error, OSError):
                self.planos_de_fundo[arquivo] = None

        for personagem in PERSONAGENS:

            caminho = caminho_recurso(
                "characters",
                personagem["id"] + ".png"
            )

            try:
                self.imagens_personagens[personagem["id"]] = (
                    pygame.image.load(str(caminho)).convert_alpha()
                )

            except (pygame.error, OSError):
                self.imagens_personagens[personagem["id"]] = None

    def _desenhar_texto(
        self,
        tela,
        texto,
        x,
        y,
        fonte=None,
        cor=CREME,
        centralizar=False
    ):

        imagem_texto = (fonte or self.fonte).render(
            str(texto),
            True,
            cor
        )

        retangulo = imagem_texto.get_rect()

        if centralizar:
            retangulo.center = (x, y)
        else:
            retangulo.topleft = (x, y)

        tela.blit(imagem_texto, retangulo)

        return retangulo

    def _quebrar_texto(self, texto, fonte, largura_maxima):

        linhas = []

        for paragrafo in str(texto).split("\n"):

            if not paragrafo:
                linhas.append("")
                continue

            linha_atual = ""

            for palavra in paragrafo.split():

                if not linha_atual:
                    tentativa = palavra
                else:
                    tentativa = linha_atual + " " + palavra

                if fonte.size(tentativa)[0] <= largura_maxima:
                    linha_atual = tentativa

                else:

                    if linha_atual:
                        linhas.append(linha_atual)

                    linha_atual = palavra

            if linha_atual:
                linhas.append(linha_atual)

        return linhas

    def _desenhar_fundo(self, tela, arquivo=None, escurecer=0):

        tela.fill((22, 35, 49))

        imagem = self.planos_de_fundo.get(arquivo) if arquivo else None

        if imagem:

            imagem_redimensionada = pygame.transform.smoothscale(
                imagem,
                (LARGURA, ALTURA)
            )

            tela.blit(imagem_redimensionada, (0, 0))

        else:

            for x in range(0, LARGURA, 64):
                pygame.draw.line(
                    tela,
                    (35, 49, 62),
                    (x, 0),
                    (x, ALTURA),
                    1
                )

            for y in range(0, ALTURA, 64):
                pygame.draw.line(
                    tela,
                    (35, 49, 62),
                    (0, y),
                    (LARGURA, y),
                    1
                )

        if escurecer:

            sombra = pygame.Surface(
                (LARGURA, ALTURA),
                pygame.SRCALPHA
            )

            sombra.fill((3, 9, 17, escurecer))
            tela.blit(sombra, (0, 0))

    def _desenhar_painel(
        self,
        tela,
        retangulo,
        borda=DOURADO,
        transparencia=238,
        arredondamento=16
    ):

        camada = pygame.Surface(
            retangulo.size,
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            camada,
            (*PAINEL, transparencia),
            camada.get_rect(),
            border_radius=arredondamento
        )

        tela.blit(camada, retangulo.topleft)

        pygame.draw.rect(
            tela,
            borda,
            retangulo,
            2,
            border_radius=arredondamento
        )

    def _desenhar_botao(
        self,
        tela,
        retangulo,
        texto,
        acao,
        mouse,
        habilitado=True
    ):

        mouse_sobre_botao = retangulo.collidepoint(mouse) and habilitado

        if mouse_sobre_botao:
            preenchimento = (58, 79, 99)
        else:
            preenchimento = (29, 46, 63)

        if not habilitado:
            preenchimento = (48, 52, 58)

        pygame.draw.rect(
            tela,
            preenchimento,
            retangulo,
            border_radius=10
        )

        cor_borda = DOURADO if mouse_sobre_botao else (99, 119, 134)

        pygame.draw.rect(
            tela,
            cor_borda,
            retangulo,
            2,
            border_radius=10
        )

        cor_texto = CREME if habilitado else CINZA

        self._desenhar_texto(
            tela,
            texto,
            *retangulo.center,
            self.fonte,
            cor_texto,
            True
        )

        self.botoes.append((retangulo, acao))

    def acao_clicada(self, posicao):

        for retangulo, acao in reversed(self.botoes):

            if retangulo.collidepoint(posicao):
                return acao

        return None

    def desenhar_menu(self, tela, mouse, possui_salvamento=False):

        self.botoes = []

        self._desenhar_fundo(tela, "menu.jpg", 90)

        self._desenhar_painel(
            tela,
            pygame.Rect(100, 85, 1080, 550),
            transparencia=225
        )

        self._desenhar_texto(
            tela,
            "CRÔNICAS DO TEMPO",
            640,
            165,
            self.fonte_titulo,
            DOURADO,
            True
        )

        self._desenhar_texto(
            tela,
            "Uma jornada de descobertas por quatro períodos históricos",
            640,
            225,
            self.fonte,
            CREME,
            True
        )

        self._desenhar_texto(
            tela,
            "Grécia Antiga   →   Idade Média   →   Idade Moderna   →   Era Contemporânea",
            640,
            280,
            self.fonte_pequena,
            DOURADO,
            True
        )

        botoes_menu = [
            ("Nova jornada", "new_game"),
            ("Continuar", "continue"),
            ("História", "history"),
            ("Créditos", "credits"),
            ("Sair", "quit")
        ]

        larguras = [205, 180, 160, 160, 130]

        largura_total = sum(larguras) + 4 * 14
        x = (LARGURA - largura_total) // 2

        for (texto, acao), largura in zip(botoes_menu, larguras):

            retangulo = pygame.Rect(x, 405, largura, 58)

            habilitado = acao != "continue" or possui_salvamento

            self._desenhar_botao(
                tela,
                retangulo,
                texto,
                acao,
                mouse,
                habilitado
            )

            x += largura + 14

        self._desenhar_texto(
            tela,
            "Movimente-se com WASD ou as setas. Aproxime-se dos marcadores e pressione ENTER.",
            640,
            535,
            self.fonte_pequena,
            CINZA,
            True
        )

        self._desenhar_texto(
            tela,
            "Projeto educacional em Python + Pygame-CE",
            640,
            580,
            self.fonte_pequena,
            CINZA,
            True
        )

    def desenhar_selecao_personagem(
        self,
        tela,
        mouse,
        selecionado,
        nome_jogador,
        mensagem_erro=""
    ):

        self.botoes = []
        self.retangulos_personagens = []

        self._desenhar_fundo(tela, "menu.jpg", 105)

        self._desenhar_texto(
            tela,
            "Escolha seu viajante",
            640,
            48,
            self.fonte_grande,
            DOURADO,
            True
        )

        self._desenhar_texto(
            tela,
            "Os quatro personagens acompanham você durante toda a jornada.",
            640,
            91,
            self.fonte_pequena,
            CREME,
            True
        )

        for indice, personagem in enumerate(PERSONAGENS):

            x = 30 + indice * 307

            cartao = pygame.Rect(x, 130, 285, 430)

            esta_selecionado = personagem["id"] == selecionado

            pygame.draw.rect(
                tela,
                (14, 27, 40),
                cartao,
                border_radius=15
            )

            cor_borda = DOURADO if esta_selecionado else personagem["cor"]
            espessura = 4 if esta_selecionado else 2

            pygame.draw.rect(
                tela,
                cor_borda,
                cartao,
                espessura,
                border_radius=15
            )

            imagem = self.imagens_personagens.get(personagem["id"])

            if imagem:

                proporcao = min(
                    165 / imagem.get_width(),
                    260 / imagem.get_height()
                )

                tamanho = (
                    max(1, int(imagem.get_width() * proporcao)),
                    max(1, int(imagem.get_height() * proporcao))
                )

                imagem_redimensionada = pygame.transform.scale(
                    imagem,
                    tamanho
                )

                tela.blit(
                    imagem_redimensionada,
                    imagem_redimensionada.get_rect(
                        midtop=(cartao.centerx, 145)
                    )
                )

            cor_nome = DOURADO if esta_selecionado else CREME

            self._desenhar_texto(
                tela,
                personagem["nome"],
                cartao.centerx,
                425,
                self.fonte_media,
                cor_nome,
                True
            )

            self._desenhar_texto(
                tela,
                personagem["classe"],
                cartao.centerx,
                465,
                self.fonte,
                personagem["cor"],
                True
            )

            self._desenhar_texto(
                tela,
                personagem["atributos"],
                cartao.centerx,
                496,
                self.fonte_pequena,
                CREME,
                True
            )

            retangulo = pygame.Rect(x + 42, 520, 201, 32)

            texto_botao = (
                "Selecionado ✓"
                if esta_selecionado
                else "Escolher"
            )

            self._desenhar_botao(
                tela,
                retangulo,
                texto_botao,
                f"choose:{personagem['id']}",
                mouse
            )

            self.retangulos_personagens.append(
                (retangulo, personagem["id"])
            )

        self._desenhar_texto(
            tela,
            "Nome do jogador:",
            410,
            602,
            self.fonte_pequena,
            CREME
        )

        self.retangulo_nome = pygame.Rect(555, 583, 300, 42)

        pygame.draw.rect(
            tela,
            (14, 27, 40),
            self.retangulo_nome,
            border_radius=7
        )

        pygame.draw.rect(
            tela,
            DOURADO,
            self.retangulo_nome,
            2,
            border_radius=7
        )

        self._desenhar_texto(
            tela,
            nome_jogador + " ▏",
            self.retangulo_nome.x + 10,
            self.retangulo_nome.y + 10,
            self.fonte_pequena,
            CREME
        )

        if mensagem_erro:
            self._desenhar_texto(
                tela,
                mensagem_erro,
                640,
                665,
                self.fonte_pequena,
                (255, 120, 120),
                True
            )

        iniciar = pygame.Rect(900, 580, 300, 52)

        self._desenhar_botao(
            tela,
            iniciar,
            "Começar aventura →",
            "start_game",
            mouse
        )

        voltar = pygame.Rect(25, 25, 125, 40)

        self._desenhar_botao(
            tela,
            voltar,
            "← Menu",
            "menu",
            mouse
        )

    def desenhar_introducao(self, tela, mouse, era):

        self.botoes = []

        self._desenhar_fundo(
            tela,
            era.arquivo_introducao,
            110
        )

        self._desenhar_painel(
            tela,
            pygame.Rect(100, 65, 1080, 590),
            transparencia=232
        )

        self._desenhar_texto(
            tela,
            era.nome,
            640,
            125,
            self.fonte_grande,
            DOURADO,
            True
        )

        self._desenhar_texto(
            tela,
            era.periodo,
            640,
            175,
            self.fonte_media,
            CREME,
            True
        )

        y = 225

        for linha in self._quebrar_texto(
            era.introducao,
            self.fonte,
            940
        ):

            if not linha:
                y += 17
                continue

            self._desenhar_texto(
                tela,
                linha,
                165,
                y,
                self.fonte,
                CREME
            )

            y += 30

        y += 20

        self._desenhar_texto(
            tela,
            "Sua missão",
            165,
            y,
            self.fonte_media,
            DOURADO
        )

        y += 43

        for linha in self._quebrar_texto(
            era.objetivo,
            self.fonte,
            940
        ):

            self._desenhar_texto(
                tela,
                linha,
                165,
                y,
                self.fonte,
                CREME
            )

            y += 29

        retangulo = pygame.Rect(470, 570, 340, 55)

        self._desenhar_botao(
            tela,
            retangulo,
            "Entrar no mapa →",
            "enter_map",
            mouse
        )

    def desenhar_marcador_npc(self, tela, npc, proximo=False):

        x = int(npc.x)
        y = int(npc.y)

        caixa = pygame.Rect(x - 16, y - 66, 32, 32)

        cor = VERDE if npc.concluido else DOURADO

        sombra = caixa.move(2, 3)

        pygame.draw.rect(
            tela,
            (8, 15, 22),
            sombra,
            border_radius=6
        )

        pygame.draw.rect(
            tela,
            (18, 31, 43),
            caixa,
            border_radius=6
        )

        pygame.draw.rect(
            tela,
            cor,
            caixa,
            3,
            border_radius=6
        )

        marcador = "?"

        self._desenhar_texto(
            tela,
            marcador,
            caixa.centerx,
            caixa.centery - 1,
            self.fonte_media,
            cor,
            True
        )

        if proximo and not npc.concluido:

            etiqueta = self.fonte_pequena.render(
                "ENTER • conversar",
                True,
                CREME
            )

            fundo = etiqueta.get_rect(
                center=(x, y - 86)
            ).inflate(14, 8)

            pygame.draw.rect(
                tela,
                (12, 23, 35),
                fundo,
                border_radius=5
            )

            tela.blit(
                etiqueta,
                etiqueta.get_rect(center=fundo.center)
            )

        elif npc.concluido:

            etiqueta = self.fonte_pequena.render(
                "Concluído",
                True,
                VERDE
            )

            tela.blit(
                etiqueta,
                etiqueta.get_rect(center=(x, y - 86))
            )

    def desenhar_mapa(
        self,
        tela,
        mouse,
        era,
        jogador,
        npcs,
        sessao,
        npc_proximo,
        feedback=""
    ):

        self.botoes = []

        self._desenhar_fundo(
            tela,
            era.arquivo_mapa,
            0
        )

        painel_informacoes = pygame.Surface(
            (LARGURA, 100),
            pygame.SRCALPHA
        )

        painel_informacoes.fill((7, 17, 29, 218))

        tela.blit(painel_informacoes, (0, 0))

        self._desenhar_texto(
            tela,
            era.nome,
            24,
            13,
            self.fonte_media,
            DOURADO
        )

        self._desenhar_texto(
            tela,
            era.periodo,
            26,
            55,
            self.fonte_pequena,
            CREME
        )

        self._desenhar_texto(
            tela,
            f"Vidas: {'♥ ' * sessao.vidas}   "
            f"Encontros: {sessao.quantidade_concluida}/3   "
            f"Pontos: {sessao.pontuacao}",
            770,
            22,
            self.fonte,
            CREME
        )

        self._desenhar_texto(
            tela,
            "WASD / setas: mover   •   ENTER: interagir   •   ESC: menu",
            770,
            58,
            self.fonte_pequena,
            CINZA
        )

        for npc in npcs:

            self.desenhar_marcador_npc(
                tela,
                npc,
                proximo=(npc_proximo is npc)
            )

        self.desenhar_jogador(tela, jogador, era.chave)

        if feedback:

            self._desenhar_painel(
                tela,
                pygame.Rect(245, 635, 790, 48),
                borda=VERDE,
                transparencia=235,
                arredondamento=10
            )

            self._desenhar_texto(
                tela,
                feedback,
                640,
                659,
                self.fonte_pequena,
                VERDE,
                True
            )

        if sessao.era_concluida:

            if era.chave == "contemporanea":
                texto_botao = "Concluir jornada"
                acao = "finish_game"
            else:
                texto_botao = "Avançar de era →"
                acao = "advance_from_map"

            retangulo = pygame.Rect(500, 665, 280, 38)

            self._desenhar_botao(
                tela,
                retangulo,
                texto_botao,
                acao,
                mouse
            )

        retangulo = pygame.Rect(1095, 665, 160, 38)

        self._desenhar_botao(
            tela,
            retangulo,
            "Menu",
            "menu",
            mouse
        )

    def desenhar_jogador(self, tela, jogador, chave_era):

        imagem = self.imagens_personagens.get(jogador.id_personagem)

        if not imagem:
            return

        # Pequeno movimento vertical durante a caminhada.
        movimento = (
            int(math.sin(pygame.time.get_ticks() / 75) * 2)
            if jogador.andando
            else 0
        )

        imagem = pygame.transform.flip(
            imagem,
            not jogador.olhando_direita,
            False
        )

        escala = ESCALAS_PERSONAGEM.get(chave_era, 1.0)

        largura_maxima = 76 * escala
        altura_maxima = 112 * escala

        proporcao = min(
            largura_maxima / imagem.get_width(),
            altura_maxima / imagem.get_height()
        )

        tamanho = (
            max(1, int(imagem.get_width() * proporcao)),
            max(1, int(imagem.get_height() * proporcao))
        )

        imagem = pygame.transform.scale(imagem, tamanho)

        tela.blit(
            imagem,
            imagem.get_rect(
                midbottom=(
                    int(jogador.x),
                    int(jogador.y + 24 + movimento)
                )
            )
        )

    def desenhar_pergunta(
        self,
        tela,
        mouse,
        era,
        jogador,
        npcs,
        sessao,
        npc_proximo,
        pergunta,
        texto_digitado,
        feedback,
        cor_feedback
    ):

        self.desenhar_mapa(
            tela,
            mouse,
            era,
            jogador,
            npcs,
            sessao,
            npc_proximo
        )

        sombra = pygame.Surface(
            (LARGURA, ALTURA),
            pygame.SRCALPHA
        )

        sombra.fill((0, 0, 0, 155))
        tela.blit(sombra, (0, 0))

        self._desenhar_painel(
            tela,
            pygame.Rect(155, 125, 970, 495),
            transparencia=248
        )

        self._desenhar_texto(
            tela,
            pergunta.nome,
            640,
            171,
            self.fonte_media,
            DOURADO,
            True
        )

        y = 225

        for linha in self._quebrar_texto(
            pergunta.enunciado,
            self.fonte,
            850
        ):

            self._desenhar_texto(
                tela,
                linha,
                215,
                y,
                self.fonte,
                CREME
            )

            y += 34

        if pergunta.opcoes:

            y += 12

            for indice, opcao in enumerate(pergunta.opcoes):

                self._desenhar_texto(
                    tela,
                    f"{indice + 1}. {opcao}",
                    245,
                    y,
                    self.fonte,
                    DOURADO
                )

                y += 32

        y = max(y + 15, 390)

        self._desenhar_texto(
            tela,
            "Sua resposta:",
            215,
            y,
            self.fonte,
            DOURADO
        )

        retangulo_entrada = pygame.Rect(
            215,
            y + 38,
            850,
            54
        )

        pygame.draw.rect(
            tela,
            (16, 29, 42),
            retangulo_entrada,
            border_radius=8
        )

        pygame.draw.rect(
            tela,
            (125, 151, 169),
            retangulo_entrada,
            2,
            border_radius=8
        )

        if texto_digitado:
            texto_exibido = texto_digitado[-75:]
        else:
            texto_exibido = "Digite sua resposta aqui..."

        self._desenhar_texto(
            tela,
            texto_exibido + ("▏" if texto_digitado else ""),
            retangulo_entrada.x + 14,
            retangulo_entrada.y + 14,
            self.fonte,
            CREME if texto_digitado else CINZA
        )

        if feedback:

            self._desenhar_texto(
                tela,
                feedback,
                640,
                530,
                self.fonte_pequena,
                cor_feedback,
                True
            )

        self._desenhar_botao(
            tela,
            pygame.Rect(825, 550, 220, 48),
            "Enviar resposta",
            "submit_answer",
            mouse
        )

        self._desenhar_botao(
            tela,
            pygame.Rect(235, 550, 200, 48),
            "Voltar ao mapa",
            "back_map",
            mouse
        )

    def desenhar_resultado(
        self,
        tela,
        mouse,
        era,
        pergunta,
        sessao,
        todas_eras_concluidas=False
    ):

        self.botoes = []

        self._desenhar_fundo(
            tela,
            era.arquivo_introducao,
            150
        )

        self._desenhar_painel(
            tela,
            pygame.Rect(190, 125, 900, 470),
            borda=VERDE,
            transparencia=245
        )

        self._desenhar_texto(
            tela,
            "Desafio concluído!",
            640,
            190,
            self.fonte_grande,
            VERDE,
            True
        )

        self._desenhar_texto(
            tela,
            "A interrogação deste encontro agora está verde no mapa.",
            640,
            250,
            self.fonte,
            CREME,
            True
        )

        y = 315

        for linha in self._quebrar_texto(
            pergunta.explicacao,
            self.fonte,
            760
        ):

            self._desenhar_texto(
                tela,
                linha,
                260,
                y,
                self.fonte,
                CREME
            )

            y += 35

        self._desenhar_texto(
            tela,
            f"Encontros concluídos: {sessao.quantidade_concluida}/3"
            f"    •    Pontuação: {sessao.pontuacao}",
            640,
            420,
            self.fonte,
            DOURADO,
            True
        )

        if sessao.era_concluida:

            if todas_eras_concluidas:
                texto_botao = "Concluir jornada"
                acao = "finish_game"
            else:
                texto_botao = "Avançar para próxima era →"
                acao = "next_era"

        else:
            texto_botao = "Continuar explorando"
            acao = "back_map"

        self._desenhar_botao(
            tela,
            pygame.Rect(430, 490, 420, 58),
            texto_botao,
            acao,
            mouse
        )

    def desenhar_fim_de_jogo(self, tela, mouse, era):

        self.botoes = []

        self._desenhar_fundo(
            tela,
            era.arquivo_introducao,
            160
        )

        self._desenhar_painel(
            tela,
            pygame.Rect(220, 170, 840, 390),
            borda=VERMELHO,
            transparencia=245
        )

        self._desenhar_texto(
            tela,
            "A jornada será reiniciada",
            640,
            245,
            self.fonte_grande,
            VERMELHO,
            True
        )

        self._desenhar_texto(
            tela,
            "Suas três vidas foram utilizadas.",
            640,
            320,
            self.fonte,
            CREME,
            True
        )

        self._desenhar_texto(
            tela,
            "Você voltará à Grécia Antiga com novos desafios sorteados.",
            640,
            365,
            self.fonte,
            CREME,
            True
        )

        self._desenhar_botao(
            tela,
            pygame.Rect(435, 435, 410, 58),
            "Recomeçar na Grécia",
            "restart",
            mouse
        )

    def desenhar_encerramento(self, tela, mouse, pontuacao):

        self.botoes = []

        self._desenhar_fundo(
            tela,
            "intro_contemporanea.jpg",
            140
        )

        self._desenhar_painel(
            tela,
            pygame.Rect(170, 120, 940, 470),
            borda=DOURADO,
            transparencia=245
        )

        self._desenhar_texto(
            tela,
            "Jornada concluída!",
            640,
            205,
            self.fonte_grande,
            DOURADO,
            True
        )

        self._desenhar_texto(
            tela,
            "Você atravessou as quatro eras e superou os desafios.",
            640,
            290,
            self.fonte,
            CREME,
            True
        )

        self._desenhar_texto(
            tela,
            f"Pontuação final: {pontuacao}",
            640,
            355,
            self.fonte_media,
            VERDE,
            True
        )

        self._desenhar_botao(
            tela,
            pygame.Rect(455, 455, 370, 58),
            "Voltar ao menu",
            "menu",
            mouse
        )

    def desenhar_informacoes(
        self,
        tela,
        mouse,
        titulo,
        texto,
        acao="menu"
    ):

        self.botoes = []

        self._desenhar_fundo(
            tela,
            "menu.jpg",
            130
        )

        self._desenhar_painel(
            tela,
            pygame.Rect(140, 100, 1000, 520),
            transparencia=242
        )

        self._desenhar_texto(
            tela,
            titulo,
            640,
            165,
            self.fonte_grande,
            DOURADO,
            True
        )

        y = 235

        for linha in self._quebrar_texto(
            texto,
            self.fonte,
            850
        ):

            if not linha:
                y += 16
                continue

            self._desenhar_texto(
                tela,
                linha,
                215,
                y,
                self.fonte,
                CREME
            )

            y += 35

        self._desenhar_botao(
            tela,
            pygame.Rect(500, 545, 280, 52),
            "Voltar",
            "menu",
            mouse
        )
