# Crônicas do Tempo

## 1. Visão Geral do Projeto

**Crônicas do Tempo** é um jogo educativo 2D desenvolvido em Python com
Pygame-CE e programação orientada a objetos (POO). O jogador assume o
papel de um viajante que explora diferentes períodos históricos,
conversa com habitantes e resolve desafios relacionados à História,
Matemática e pensamento científico.

A jornada é dividida em quatro eras: Grécia Antiga, Idade Média, Idade
Moderna e Idade Contemporânea. Cada era apresenta um cenário próprio,
personagens não jogáveis (NPCs) e perguntas que precisam ser respondidas
para avançar.

O projeto combina exploração, aprendizagem e elementos de RPG,
utilizando conceitos de encapsulamento, herança, abstração, polimorfismo
e composição.

## 2. Estrutura do Projeto

A organização geral do projeto está dividida em módulos:

- `main.py`: ponto de entrada e inicialização do jogo.
- `Models/`: modelos das entidades do jogo (como jogador e NPCs), classes de desafios, representação do mundo, configuração das eras e gerenciamento de persistência/salvamento.
- `Controllers/`: controlador principal e funções centrais do jogo.
- `Services/`: sistemas de sessão/progresso e banco de perguntas.
- `Views/`: renderização das telas, mapas, personagens, botões e demais elementos visuais.
- `Views/assets/`: imagens, mapas, fontes e demais recursos visuais.
- `Data/`: banco SQLite, arquivo JSON de perguntas e esquema SQL.
- `Tests/`: testes do sistema.

Os caminhos de recursos, do banco de dados e do salvamento são centralizados em `Controllers/caminhos.py`.

## 3. Como Executar

O projeto utiliza Python e Pygame-CE.

Instale a dependência:

``` bash
pip install pygame-ce
```

Na pasta principal do projeto, execute:

``` bash
python main.py
```

O arquivo `main.py` inicia o controlador principal do jogo, responsável
por coordenar a lógica, os eventos e a interface.

## 4. Módulos e Classes Principais

A seguir, são apresentados os principais módulos e suas
responsabilidades, no formato de cartões CRC (Classe, Responsabilidades
e Colaborações).

### Personagem

**Responsabilidades:**

-   Representar a estrutura básica de um personagem.
-   Armazenar nome, posição e velocidade.
-   Controlar o deslocamento pelo cenário.
-   Definir o comportamento básico de interação.
-   Servir como classe-base para personagens especializados.

**Colaborações:** Jogador, PersonagemNaoJogavel.

### Jogador

**Responsabilidades:**

-   Representar o personagem controlado pelo usuário.
-   Armazenar o identificador do personagem selecionado.
-   Processar movimentação pelo teclado.
-   Registrar direção e estado de movimento.
-   Informar quando uma vida é perdida ou pontos são adicionados.

**Colaborações:** Personagem, ControladorJogo, RenderizadorJogo.

As vidas e a pontuação da campanha são controladas exclusivamente por `SessaoJogo`.

### PersonagemNaoJogavel

**Responsabilidades:**

-   Representar personagens que não são controlados pelo jogador.
-   Armazenar identificação, nome e posição.
-   Registrar se o encontro associado já foi concluído.
-   Fornecer comportamento básico de interação.

**Colaborações:** NPCDesafio, ControladorJogo, RenderizadorJogo.

### NPCDesafio

**Responsabilidades:**

-   Representar habitantes que apresentam desafios ao jogador.
-   Associar um encontro a uma era histórica.
-   Indicar se o desafio já foi concluído.
-   Participar do sistema de interação do mapa.

**Colaborações:** PersonagemNaoJogavel, ControladorJogo, BancoPerguntas.

### Pergunta

**Responsabilidades:**

-   Armazenar os dados de uma pergunta.
-   Disponibilizar enunciado, explicação, pontuação e opções.
-   Identificar o tipo de validação configurado.
-   Encaminhar a resposta para o validador correspondente.

**Colaborações:** FabricaValidadores, Desafio, DesafioTextual,
DesafioQuestionario.

### Desafio

**Responsabilidades:**

-   Definir a estrutura abstrata dos desafios.
-   Manter a pergunta associada.
-   Estabelecer o método de validação que as classes derivadas devem
    implementar.

**Colaborações:** Pergunta, DesafioTextual, DesafioQuestionario.

### DesafioTextual

**Responsabilidades:**

-   Representar desafios respondidos por texto.
-   Encaminhar a resposta digitada para a pergunta.
-   Retornar o resultado da validação.

**Colaborações:** Desafio, Pergunta, ControladorJogo.

### DesafioQuestionario

**Responsabilidades:**

-   Representar desafios do tipo questionário.
-   Encaminhar a resposta selecionada ou informada para a pergunta.
-   Retornar o resultado da validação.

**Colaborações:** Desafio, Pergunta, ControladorJogo.

### Validadores e FabricaValidadores

**Responsabilidades:**

-   Centralizar as regras de validação das respostas.
-   Selecionar o validador de acordo com o tipo configurado na pergunta.
-   Verificar respostas conforme as regras de cada modalidade.
-   Manter a validação separada da interface gráfica.

**Colaborações:** Pergunta, DesafioTextual, DesafioQuestionario.

### BancoPerguntas

**Responsabilidades:**

-   Carregar perguntas armazenadas no banco SQLite.
-   Utilizar o arquivo JSON inicial para alimentar o banco quando
    necessário.
-   Organizar perguntas por era histórica.
-   Sortear perguntas para os encontros.
-   Evitar a repetição imediata de uma pergunta quando solicitado.
-   Reiniciar o sorteio ao iniciar uma nova jornada ou era.

**Colaborações:** Pergunta, ControladorJogo, Desafio.

### SessaoJogo

**Responsabilidades:**

-   Controlar a era atual da campanha.
-   Ser a fonte oficial das vidas e da pontuação da campanha.
-   Registrar os NPCs já concluídos.
-   Informar a quantidade de encontros concluídos.
-   Verificar se a era foi finalizada.
-   Avançar para a próxima era e restaurar o progresso salvo.

**Colaborações:** Jogador, ControladorJogo, GerenciadorSalvamento,
RenderizadorJogo.

### EraHistorica

**Responsabilidades:**

-   Representar uma era histórica.
-   Armazenar nome, período e introdução.
-   Registrar o objetivo da etapa.
-   Indicar os arquivos de mapa e introdução.
-   Definir a posição inicial do jogador e as posições dos NPCs.

**Colaborações:** ControladorJogo, RenderizadorJogo, SessaoJogo.

### GerenciadorSalvamento

**Responsabilidades:**

-   Salvar os dados de progresso do jogador.
-   Carregar uma partida previamente salva.
-   Verificar a existência de um arquivo de salvamento.
-   Manter os dados necessários para continuar a campanha.

**Colaborações:** ControladorJogo, SessaoJogo.

### ControladorJogo

**Responsabilidades:**

-   Coordenar o fluxo principal do jogo.
-   Controlar os estados das telas e as transições entre eles.
-   Processar eventos de teclado e mouse.
-   Criar o jogador e os NPCs de cada era.
-   Iniciar interações e desafios.
-   Encaminhar respostas para validação.
-   Atualizar vidas, pontuação e progresso.
-   Coordenar carregamento e salvamento da partida.
-   Solicitar ao renderizador a apresentação de cada tela.

**Colaborações:** Jogador, NPCDesafio, Pergunta, Desafio,
BancoPerguntas, SessaoJogo, EraHistorica, GerenciadorSalvamento,
RenderizadorJogo.

### RenderizadorJogo

**Responsabilidades:**

-   Desenhar menus e telas de seleção.
-   Exibir introduções e mapas das eras.
-   Renderizar jogador, NPCs e elementos da interface.
-   Apresentar perguntas e resultados.
-   Exibir vidas, pontuação e progresso.
-   Desenhar as telas de fim de jogo e encerramento.
-   Controlar elementos visuais interativos, como botões.

**Colaborações:** ControladorJogo, Jogador, NPCDesafio, Pergunta,
SessaoJogo, EraHistorica.

## 5. User Stories

-   Como jogador, quero escolher um personagem para iniciar a jornada
    com uma identidade visual própria.
-   Como jogador, quero explorar cenários inspirados em diferentes
    períodos históricos.
-   Como jogador, quero encontrar habitantes e interagir com eles para
    receber desafios.
-   Como jogador, quero responder perguntas de diferentes áreas do
    conhecimento para concluir os encontros.
-   Como jogador, quero receber pontuação pelas respostas corretas para
    acompanhar meu desempenho.
-   Como jogador, quero perder vidas quando responder incorretamente,
    tornando os desafios mais relevantes.
-   Como jogador, quero visualizar explicações relacionadas às perguntas
    para aprender com os desafios.
-   Como jogador, quero salvar meu progresso e continuar a campanha
    posteriormente.
-   Como jogador, quero avançar pelas quatro eras históricas até
    concluir a jornada.
-   Como jogador, quero visualizar minha pontuação final ao terminar a
    campanha.

## 6. Detalhamento do Projeto

### Fluxo de Jogo

1.  O jogador acessa o menu principal.
2.  Pode iniciar uma nova jornada ou continuar uma partida salva.
3.  Na nova jornada, escolhe o personagem e informa seu nome.
4.  Visualiza a introdução da era atual.
5.  Entra no mapa e explora o cenário.
6.  Aproxima-se dos NPCs para iniciar os desafios.
7.  Responde às perguntas apresentadas.
8.  Ao concluir os encontros necessários, avança para a próxima era.
9.  Após passar pelas quatro eras, visualiza a tela de encerramento.

### Eras Históricas

O jogo é dividido em quatro períodos:

-   **Grécia Antiga:** cenário e desafios relacionados à sociedade e aos
    conhecimentos da Antiguidade.
-   **Idade Média:** cenário e desafios relacionados ao período
    medieval.
-   **Idade Moderna:** cenário e desafios relacionados às transformações
    da época moderna.
-   **Idade Contemporânea:** cenário e desafios relacionados ao mundo
    contemporâneo.

Cada era possui mapa, introdução, posições próprias para o jogador e
NPCs, além de um conjunto de perguntas.

### Sistema de Desafios

-   Os NPCs apresentam perguntas ao jogador.
-   As perguntas são organizadas por era histórica.
-   Cada pergunta possui enunciado, explicação e pontuação.
-   A validação é selecionada conforme o tipo definido nos dados da
    pergunta.
-   O sistema permite separar a lógica de validação da apresentação
    visual.
-   Respostas incorretas consomem vidas e podem levar ao sorteio de uma
    nova pergunta.
-   As explicações das perguntas auxiliam o processo de aprendizagem.

### Sistema de Vidas e Pontuação

-   O jogador inicia a campanha com um limite de três vidas.
-   Respostas incorretas reduzem a quantidade de vidas.
-   Ao perder todas as vidas, o jogador chega à tela de fim de jogo.
-   Respostas corretas concluem encontros e adicionam pontos à
    pontuação.
-   A pontuação é mantida durante a campanha e apresentada no
    encerramento.

### Sistema de Progressão

-   Cada era possui três encontros com NPCs.
-   O sistema registra quais encontros foram concluídos.
-   Quando os encontros necessários são finalizados, o jogador pode
    avançar.
-   A progressão atual é armazenada para permitir a continuidade da
    partida.
-   Ao concluir a última era, o jogo apresenta a tela final sem encerrar
    imediatamente a janela.

### Sistema de Salvamento

O sistema de persistência registra informações como:

-   Nome do jogador.
-   Personagem selecionado.
-   Era atual.
-   Quantidade de vidas.
-   Pontuação.
-   Encontros concluídos.

Essas informações são utilizadas para restaurar a partida quando o
jogador escolhe continuar.

### Interface e Recursos Visuais

-   O jogo utiliza Pygame-CE para exibição gráfica e processamento de
    eventos.
-   Os mapas e personagens são apresentados por meio de recursos visuais
    próprios.
-   O renderizador centraliza o desenho das telas e dos elementos da
    interface.
-   O tamanho do personagem pode ser ajustado conforme a escala visual
    de cada era.
-   A entrada de texto utiliza os eventos de texto do Pygame para tratar
    caracteres acentuados.

### Arquitetura Orientada a Objetos

O projeto aplica os principais conceitos de POO:

-   **Encapsulamento:** atributos e estados internos são controlados
    pelas próprias classes, com propriedades e métodos de acesso.
-   **Herança:** classes especializadas reutilizam estruturas de
    classes-base, como `Jogador` e `NPCDesafio` a partir de
    `Personagem`.
-   **Abstração:** classes abstratas, como `Personagem` e `Desafio`,
    definem estruturas e comportamentos esperados.
-   **Polimorfismo:** diferentes tipos de desafio implementam o método
    de validação de acordo com sua modalidade.
-   **Composição:** o controlador coordena objetos de diferentes classes
    para formar o funcionamento completo do jogo.

## 7. Dados e Persistência

O projeto utiliza arquivos JSON para armazenar configurações e dados
iniciais, além de SQLite para organizar as perguntas.

-   `eras.json`: configurações das eras históricas, incluindo nomes,
    períodos, mapas e posições.
-   `perguntas.json`: conjunto inicial de perguntas e seus dados de
    validação.
-   `perguntas.db`: banco SQLite utilizado pelo sistema de perguntas.
-   Arquivo de salvamento: registra o progresso da campanha.

Os nomes dos campos utilizados nos arquivos de dados devem ser mantidos
compatíveis com os formatos esperados pelo código.

## 8. Tecnologias Utilizadas

-   **Python:** linguagem de programação principal.
-   **Pygame-CE:** biblioteca utilizada para gráficos 2D, eventos,
    teclado, mouse e controle da janela.
-   **SQLite:** banco de dados para armazenamento e consulta das
    perguntas.
-   **JSON:** formato utilizado para configuração das eras e dados
    iniciais das perguntas.
-   **Programação Orientada a Objetos:** organização do código em
    classes e módulos.
