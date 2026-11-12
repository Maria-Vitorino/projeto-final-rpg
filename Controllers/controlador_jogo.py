"""Coordena os eventos e a comunicação entre a interface e a lógica do jogo."""

import json
import math
import pygame

from Controllers.caminhos import (
    PASTA_PROJETO,
    caminho_recurso,
    PASTA_BANCO_DADOS,
    PASTA_DADOS_BACKEND
)

from Models import Jogador, NPCDesafio
from Models.desafios import Pergunta, DesafioQuestionario, DesafioTextual
from Models.mundo import EraHistorica
from Services import BancoPerguntas, SessaoJogo
from Views.renderizador import RenderizadorJogo
from Models.persistencia import GerenciadorSalvamento


class ControladorJogo:
    """Gerencia o fluxo da partida e conecta os componentes do jogo."""

    def __init__(self):
        """Inicializa o Pygame, os serviços e o estado inicial da partida."""
        pygame.init()
        pygame.key.start_text_input()
        pygame.display.set_caption("Crônicas do Tempo")

        # Recursos principais da janela e controle de tempo.
        self.tela = pygame.display.set_mode((1280, 720))
        self.relogio = pygame.time.Clock()

        # Componentes responsáveis pela interface, progresso e salvamento.
        self.renderizador = RenderizadorJogo()
        self.sessao = SessaoJogo()
        self.gerenciador_salvamento = GerenciadorSalvamento()

        # Banco local que fornece as perguntas de cada era.
        self.banco_perguntas = BancoPerguntas(
            PASTA_BANCO_DADOS / "perguntas.db",
            PASTA_BANCO_DADOS / "perguntas.json"
        )

        # Carrega as configurações das eras históricas.
        self.eras = self._carregar_eras()

        # Estado geral que controla a execução e a tela atual.
        self.estado = "menu"
        self.executando = True

        # Dados escolhidos ou utilizados pelo jogador.
        self.nome_jogador = "Viajante"
        self.id_personagem = "kassandra"

        # Objetos que representam o jogador, os NPCs e o desafio atual.
        self.jogador = None
        self.npcs = []
        self.npc_proximo = None
        self.npc_ativo = None
        self.desafio_ativo = None

        # Dados temporários da interface de perguntas e mensagens.
        self.texto_digitado = ""
        self.feedback = ""
        self.cor_feedback = (111, 220, 145)

        # Entrada do teclado e posição inicial do mouse.
        self.teclas_pressionadas = set()
        self.posicao_mouse_menu = pygame.mouse.get_pos()

    def _carregar_eras(self):
        """Lê o JSON das eras e transforma cada registro em um objeto EraHistorica."""
        dados = json.loads(
            (PASTA_DADOS_BACKEND / "eras.json").read_text(encoding="utf-8")
        )

        eras = []

        # Converte as chaves do arquivo JSON para os atributos da classe.
        for item in dados:
            era = EraHistorica(
                chave=item["key"],
                nome=item["name"],
                periodo=item["period"],
                introducao=item["introduction"],
                objetivo=item["objective"],
                arquivo_mapa=item["map_file"],
                arquivo_introducao=item["intro_file"],
                posicao_inicial=tuple(item["spawn"]),
                posicoes_npcs=tuple(
                    tuple(posicao) for posicao in item["npc_positions"]
                )
            )

            eras.append(era)

        return eras

    @property
    def era_atual(self):
        """Retorna a era correspondente ao índice atual da sessão."""
        return self.eras[self.sessao.indice_era]

    def _criar_personagens_da_era(self):
        """Cria o jogador e os NPCs nas posições definidas para a era atual."""
        era = self.era_atual

        # Posiciona o jogador no ponto inicial da era.
        self.jogador = Jogador(
            self.nome_jogador,
            self.id_personagem,
            *era.posicao_inicial
        )

        # Cria os NPCs de desafio conforme as coordenadas configuradas no JSON.
        self.npcs = []

        for indice, (x, y) in enumerate(era.posicoes_npcs):
            npc = NPCDesafio(
                f"{era.chave}_{indice + 1}",
                f"Encontro {indice + 1}",
                x,
                y
            )

            self.npcs.append(npc)

        # Limpa referências e mensagens que pertenciam à era anterior.
        self.npc_ativo = None
        self.desafio_ativo = None
        self.npc_proximo = None

        self.texto_digitado = ""
        self.feedback = ""

        # Após criar os personagens, o jogo passa a exibir o mapa.
        self.estado = "mapa"

        self._salvar_progresso()

    def _salvar_progresso(self):
        """Monta os dados atuais da campanha e solicita sua gravação em JSON."""
        dados = {
            "player_name": self.nome_jogador,
            "character_id": self.id_personagem,
            "era_index": self.sessao.indice_era,
            "lives": self.sessao.vidas,
            "score": self.sessao.pontuacao,
            "completed_npcs": list(self.sessao.npcs_concluidos)
        }

        self.gerenciador_salvamento.salvar(dados)

    def _continuar_jogo_salvo(self):
        """Carrega uma campanha existente e restaura seus dados de progresso."""
        dados = self.gerenciador_salvamento.carregar()

        # Sem dados salvos, direciona o usuário à seleção de personagem.
        if not dados:
            self.estado = "personagem"
            return

        # Recupera o nome salvo, limitando-o ao tamanho utilizado pelo jogo.
        self.nome_jogador = str(
            dados.get("player_name", "Viajante")
        )[:20]

        # Confere se o identificador salvo ainda corresponde a um personagem válido.
        id_salvo = dados.get("character_id", "kassandra")
        if id_salvo in Jogador.PERSONAGENS_DISPONIVEIS:
            self.id_personagem = id_salvo
        else:
            self.id_personagem = "kassandra"

        # Mantém o índice da era dentro dos limites existentes.
        era_restaurada = max(
            0,
            min(int(dados.get("era_index", 0)), len(self.eras) - 1)
        )

        # Restaura vidas, pontuação e encontros já concluídos.
        self.sessao.restaurar(
            era_restaurada,
            dados.get("lives", 3),
            dados.get("score", 0),
            dados.get("completed_npcs", [])
        )

        # Recria os personagens e marca os NPCs que já foram concluídos.
        self._criar_personagens_da_era()

        for npc in self.npcs:
            if npc.id_npc in self.sessao.npcs_concluidos:
                npc.marcar_concluido()

    def _iniciar_interacao(self, npc):
        """Abre a interação com um NPC e seleciona uma pergunta da era atual."""
        # Não inicia interação se não houver NPC ou se ele já foi concluído.
        if npc is None or npc.concluido:
            return

        self.npc_ativo = npc

        # Busca uma pergunta pertencente à era em que o jogador está.
        pergunta = self.banco_perguntas.proxima_pergunta(
            self.era_atual.chave
        )

        self.desafio_ativo = self._criar_desafio(pergunta)

        # Limpa os dados da interação anterior e abre a tela de pergunta.
        self.texto_digitado = ""
        self.feedback = ""
        self.estado = "pergunta"

    def _criar_desafio(self, pergunta: Pergunta):
        """Escolhe a classe de desafio conforme o tipo de validação da pergunta."""
        if pergunta.dados.get("tipo_validacao") == "texto":
            return DesafioTextual(pergunta)

        return DesafioQuestionario(pergunta)

    def _enviar_resposta(self):
        """Verifica a resposta e atualiza vidas, pontuação e progresso."""
        # Não processa a resposta se não houver desafio ou NPC ativo.
        if not self.desafio_ativo or not self.npc_ativo:
            return

        pergunta = self.desafio_ativo.pergunta

        if self.desafio_ativo.validar_resposta(self.texto_digitado):

            # Resposta correta: conclui o NPC e adiciona os pontos à sessão.
            self.npc_ativo.marcar_concluido()

            self.sessao.concluir_npc(
                self.npc_ativo.id_npc,
                pergunta.pontos
            )

            self.feedback = "Resposta correta! Encontro concluído."
            self.cor_feedback = (111, 220, 145)

            self.texto_digitado = ""
            self.estado = "resultado"

            self._salvar_progresso()

        else:

            # Resposta incorreta: reduz uma vida e verifica se a partida acabou.
            sem_vidas = self.sessao.perder_vida()

            if sem_vidas:

                self.estado = "fim_de_jogo"
                self.texto_digitado = ""

                # Reinicia o sorteio para uma próxima tentativa/campanha.
                self.banco_perguntas.reiniciar_sorteio()

                # Remove o salvamento quando o jogador perde todas as vidas.
                if self.gerenciador_salvamento.existe():
                    try:
                        self.gerenciador_salvamento.caminho.unlink()
                    except OSError:
                        pass

            else:

                # Evita repetir imediatamente a pergunta que acabou de ser errada.
                id_anterior = pergunta.id_pergunta

                nova_pergunta = self.banco_perguntas.proxima_pergunta(
                    self.era_atual.chave,
                    evitar_id=id_anterior
                )

                self.desafio_ativo = self._criar_desafio(nova_pergunta)

                self.feedback = (
                    f"Resposta não reconhecida. Você perdeu uma vida "
                    f"({self.sessao.vidas} restante(s)). Nova pergunta sorteada!"
                )

                self.cor_feedback = (255, 190, 120)
                self.texto_digitado = ""

                self._salvar_progresso()

    def _reiniciar_jogo(self):
        """Reinicia os dados da sessão e prepara uma nova jornada."""
        self.sessao.reiniciar()
        self.banco_perguntas.reiniciar_sorteio()

        # Mantém o nome atual; utiliza um nome padrão se estiver vazio.
        self.nome_jogador = self.nome_jogador or "Viajante"

        self.npc_ativo = None
        self.desafio_ativo = None

        self.estado = "introducao"

        self._salvar_progresso()

    def _executar_acao(self, acao):
        """Executa a ação solicitada por um botão ou evento da interface."""
        if not acao:
            return

        # Seleciona um personagem se o identificador estiver cadastrado.
        if acao.startswith("choose:"):
            id_escolhido = acao.split(":", 1)[1]
            if id_escolhido in Jogador.PERSONAGENS_DISPONIVEIS:
                self.id_personagem = id_escolhido

        elif acao == "quit":
            # Encerra o laço principal do jogo.
            self.executando = False

        elif acao == "menu":
            self.estado = "menu"

        elif acao == "new_game":
            # Abre a tela para informar o nome e escolher o personagem.
            self.estado = "personagem"

        elif acao == "continue":
            self._continuar_jogo_salvo()

        elif acao == "history":
            self.estado = "historico"

        elif acao == "credits":
            self.estado = "creditos"

        elif acao == "start_game":
            # Valida o nome antes de iniciar a campanha, evitando que um
            # ValueError no construtor de Jogador encerre o jogo.
            nome_validado = self.nome_jogador

            try:
                Jogador(
                    nome_validado,
                    self.id_personagem,
                    *self.eras[0].posicao_inicial
                )
            except ValueError as erro:
                self.feedback = str(erro)
                return

            # Normaliza espaços repetidos e prepara uma sessão nova.
            self.nome_jogador = " ".join(nome_validado.split())
            self.feedback = ""
            self.sessao.reiniciar()
            self.banco_perguntas.reiniciar_sorteio()
            self.estado = "introducao"

        elif acao == "enter_map":
            self._criar_personagens_da_era()

        elif acao == "submit_answer":
            self._enviar_resposta()

        elif acao == "back_map":
            # Fecha a pergunta e retorna ao mapa sem alterar o progresso.
            self.estado = "mapa"
            self.npc_ativo = None
            self.desafio_ativo = None
            self.feedback = ""

        elif acao in ("next_era", "advance_from_map"):

            # Só avança se ainda houver outra era na campanha.
            if self.sessao.indice_era < len(self.eras) - 1:

                self.sessao.proxima_era()
                self.banco_perguntas.reiniciar_sorteio()

                self.estado = "introducao"

                self._salvar_progresso()

        elif acao == "finish_game":
            self.estado = "final"

        elif acao == "restart":
            self._reiniciar_jogo()

    def _tratar_evento(self, evento):
        """Interpreta eventos do Pygame, como teclado, mouse e fechamento."""
        if evento.type == pygame.QUIT:
            self.executando = False

        elif evento.type == pygame.KEYDOWN:

            if self.estado == "mapa":

                # No mapa, Enter interage com o NPC próximo; Escape abre o menu.
                if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):

                    if self.npc_proximo:
                        self._iniciar_interacao(self.npc_proximo)

                elif evento.key == pygame.K_ESCAPE:
                    self.estado = "menu"

                else:
                    self.teclas_pressionadas.add(evento.key)

            elif self.estado == "pergunta":

                # Na pergunta, Enter envia a resposta e Backspace apaga caracteres.
                if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    self._enviar_resposta()

                elif evento.key == pygame.K_BACKSPACE:
                    self.texto_digitado = self.texto_digitado[:-1]

                elif evento.key == pygame.K_ESCAPE:
                    # Sai da pergunta e volta ao mapa.
                    self.estado = "mapa"
                    self.npc_ativo = None
                    self.desafio_ativo = None

            elif self.estado == "personagem":

                # Na seleção, Backspace edita o nome e Escape retorna ao menu.
                if evento.key == pygame.K_BACKSPACE:
                    self.nome_jogador = self.nome_jogador[:-1]
                    self.feedback = ""

                elif evento.key == pygame.K_RETURN:
                    # A validação definitiva ocorre ao clicar em começar.
                    self.feedback = ""

                elif evento.key == pygame.K_ESCAPE:
                    self.estado = "menu"

            elif evento.key == pygame.K_ESCAPE:
                self.estado = "menu"

        elif evento.type == pygame.TEXTINPUT:

            # TEXTINPUT recebe caracteres digitados, incluindo acentos.
            if self.estado == "pergunta":
                if len(self.texto_digitado) + len(evento.text) <= 160:
                    self.texto_digitado += evento.text

            elif self.estado == "personagem":
                # Permite letras, espaços e hífen/apóstrofo em nomes próprios.
                texto_valido = "".join(
                    caractere
                    for caractere in evento.text
                    if caractere.isalpha()
                    or caractere.isspace()
                    or caractere in "-'’"
                )

                # Limita o nome a 20 caracteres.
                if len(self.nome_jogador) + len(texto_valido) <= 20:
                    self.nome_jogador += texto_valido
                    self.feedback = ""

                # Informa quando algum caractere digitado não é permitido.
                if texto_valido != evento.text:
                    self.feedback = "Use apenas letras para o nome do jogador."

        elif evento.type == pygame.KEYUP:
            # Remove a tecla do conjunto quando ela deixa de ser pressionada.
            self.teclas_pressionadas.discard(evento.key)

        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

            # Se o clique foi no campo de nome, não trata como clique em botão.
            if (
                self.estado == "personagem"
                and self.renderizador.retangulo_nome.collidepoint(evento.pos)
            ):
                return

            # Converte a posição do clique em uma ação e a executa.
            acao = self.renderizador.acao_clicada(evento.pos)
            self._executar_acao(acao)

    def _atualizar(self, tempo):
        """Atualiza movimentação e proximidade dos NPCs a cada quadro."""
        # Só atualiza movimento quando o mapa está aberto e há jogador criado.
        if self.estado != "mapa" or not self.jogador:
            return

        dx = 0
        dy = 0

        # Calcula a direção com base nas teclas de movimentação pressionadas.
        if pygame.K_LEFT in self.teclas_pressionadas or pygame.K_a in self.teclas_pressionadas:
            dx -= 1

        if pygame.K_RIGHT in self.teclas_pressionadas or pygame.K_d in self.teclas_pressionadas:
            dx += 1

        if pygame.K_UP in self.teclas_pressionadas or pygame.K_w in self.teclas_pressionadas:
            dy -= 1

        if pygame.K_DOWN in self.teclas_pressionadas or pygame.K_s in self.teclas_pressionadas:
            dy += 1

        # Atualiza a posição do jogador respeitando os limites do mapa.
        self.jogador.definir_movimento(
            dx,
            dy,
            tempo,
            (42, 145, 1238, 675)
        )

        npcs_proximos = []

        # Calcula a distância entre o jogador e cada NPC ainda não concluído.
        for npc in self.npcs:

            if not npc.concluido:
                distancia = math.hypot(
                    self.jogador.x - npc.x,
                    self.jogador.y - npc.y
                )

                if distancia < 92:
                    npcs_proximos.append(npc)

        # Define como próximo o NPC não concluído que estiver mais perto.
        if npcs_proximos:

            self.npc_proximo = min(
                npcs_proximos,
                key=lambda npc: math.hypot(
                    self.jogador.x - npc.x,
                    self.jogador.y - npc.y
                )
            )

        else:
            self.npc_proximo = None

    def _desenhar(self):
        """Seleciona e desenha a tela correspondente ao estado atual do jogo."""
        mouse = pygame.mouse.get_pos()

        # Cada estado direciona a execução para um método específico do renderizador.
        if self.estado == "menu":
            self.renderizador.desenhar_menu(
                self.tela,
                mouse,
                self.gerenciador_salvamento.existe()
            )

        elif self.estado == "personagem":
            self.renderizador.desenhar_selecao_personagem(
                self.tela,
                mouse,
                self.id_personagem,
                self.nome_jogador,
                self.feedback
            )

        elif self.estado == "historico":

            # Texto informativo apresentado na seção de história do jogo.
            texto = (
                "Em Crônicas do Tempo, uma pessoa viajante atravessa quatro períodos históricos. "
                "Em cada era, explora um cenário, encontra habitantes e resolve desafios inspirados "
                "em acontecimentos e conhecimentos daquele contexto. O jogo combina História, "
                "matemática e pensamento científico. Cada era apresenta três encontros; respostas "
                "incorretas consomem vidas e novas perguntas são sorteadas para incentivar a aprendizagem."
            )

            self.renderizador.desenhar_informacoes(
                self.tela,
                mouse,
                "A história da jornada",
                texto
            )

        elif self.estado == "creditos":

            # Identificação da equipe e das tecnologias utilizadas no projeto.
            texto = (
                "Projeto educacional Crônicas do Tempo.\n"
                "Desenvolvimento: Beatriz Coutinho, Maria Fernanda e Vitor Stanciola.\n"
                "Professora: Gabriela Nunes.\n\n"
                "Jogo 2D desenvolvido em Python com Pygame-CE, com arquitetura orientada a objetos, "
                "herança, encapsulamento, abstração, polimorfismo e composição."
            )

            self.renderizador.desenhar_informacoes(
                self.tela,
                mouse,
                "Créditos",
                texto
            )

        elif self.estado == "introducao":
            self.renderizador.desenhar_introducao(
                self.tela,
                mouse,
                self.era_atual
            )

        elif self.estado == "mapa":
            self.renderizador.desenhar_mapa(
                self.tela,
                mouse,
                self.era_atual,
                self.jogador,
                self.npcs,
                self.sessao,
                self.npc_proximo,
                self.feedback
            )

        elif self.estado == "pergunta" and self.desafio_ativo:

            self.renderizador.desenhar_pergunta(
                self.tela,
                mouse,
                self.era_atual,
                self.jogador,
                self.npcs,
                self.sessao,
                self.npc_proximo,
                self.desafio_ativo.pergunta,
                self.texto_digitado,
                self.feedback,
                self.cor_feedback
            )

        elif self.estado == "resultado":

            # Exibe o resultado do desafio e informa se todas as eras foram concluídas.
            self.renderizador.desenhar_resultado(
                self.tela,
                mouse,
                self.era_atual,
                self.desafio_ativo.pergunta,
                self.sessao,
                self.sessao.indice_era == len(self.eras) - 1
            )

        elif self.estado == "fim_de_jogo":
            self.renderizador.desenhar_fim_de_jogo(
                self.tela,
                mouse,
                self.era_atual
            )

        elif self.estado == "final":
            # Mostra a tela de encerramento com a pontuação final.
            self.renderizador.desenhar_encerramento(
                self.tela,
                mouse,
                self.sessao.pontuacao
            )

        # Atualiza a janela para apresentar o desenho do quadro atual.
        pygame.display.flip()

    def executar(self):
        """Executa o laço principal: recebe eventos, atualiza e desenha o jogo."""
        while self.executando:

            # Limita a taxa a 60 FPS e evita saltos grandes no tempo de atualização.
            tempo = min(self.relogio.tick(60) / 1000.0, 0.05)

            # Processa todos os eventos recebidos neste quadro.
            for evento in pygame.event.get():
                self._tratar_evento(evento)

            # Atualiza a lógica e redesenha a tela.
            self._atualizar(tempo)
            self._desenhar()

        # Finaliza os módulos do Pygame ao sair do laço principal.
        pygame.quit()
