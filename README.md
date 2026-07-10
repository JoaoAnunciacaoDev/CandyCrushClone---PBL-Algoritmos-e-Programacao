# Candy Crush da Deep Web 🍭☠️

Este projeto é um clone do clássico **Candy Crush** desenvolvido em Python com a biblioteca **Pygame**, enriquecido com várias temáticas divertidas (como *Undertale* e *Street Fighter*), músicas envolventes e animações dinâmicas de transição e GameOver.

O projeto foi inicialmente criado como parte de um projeto de **PBL (Problem-Based Learning)** para a universidade. Esta versão foi organizada, reestruturada e empacotada profissionalmente para facilitar o download de recursos, a execução e a manutenção do código.

---

## 🎨 Temáticas e Recursos
* **Trilha Sonora Dinâmica:**
  * **Menu:** *startTheme.mp3* (ritmo que acelera após 18 segundos!)
  * **Partida:** *Asriel Theme* de Undertale.
  * **GameOver:** *GameOver Song* e efeitos sonoros como o coração quebrando (*broken.mp3* / *somQuebra.mp3*).
  * **Desafio:** Efeito de "Here comes a new challenger" do Street Fighter.
  * **Fim Especial:** Áudio da Ellie (*The Last of Us*) ao desistir do reinício.
* **Efeitos Visuais e Animações:**
  * Coração pulsando durante o jogo.
  * Animação do coração quebrando e se recusando a quebrar (baseada no GameOver de Undertale).
  * Animação de explosão do coração ao escolher não continuar.
* **Sistema de Recordes (Leaderboard):** As 5 melhores pontuações são armazenadas localmente no arquivo `pontuacao.json` na raiz do projeto.
* **Sistema de Dicas (Hints):** Pressione `H` para revelar um movimento válido. Custa **250 pontos**.

---

## 🎮 Controles do Jogo

| Tecla | Ação |
| :--- | :--- |
| **W / A / S / D** ou **Setas** | Mover o retângulo de seleção |
| **ENTER / RETURN** | Selecionar a peça atual (o retângulo mudará de cor) |
| **W/A/S/D ou Setas** (com seleção ativa) | Trocar a peça selecionada com a adjacente |
| **H** | Solicitar uma dica de jogada (Custo: 250 pontos) |
| **ESPAÇO** | Voltar ao Menu Principal |
| **ESC** | Fechar o jogo |

---

## 🏆 Sistema de Pontuação das Gemas

Ao combinar 3 ou mais gemas da mesma cor, a pontuação é calculada de acordo com as seguintes cores:
* 🟨 **Amarelo:** 20 pontos
* 🟩 **Verde:** 30 pontos
* 🟥 **Vermelho:** 35 pontos
* 🟦 **Azul:** 40 pontos
* 🟪 **Violeta:** 50 pontos

---

## 🛠️ Requisitos de Instalação e Execução

O projeto agora usa **Poetry** para gerenciar dependências e **Mise** para simplificar comandos de execução.

### Pré-requisitos
Certifique-se de ter o Python 3.11 ou superior instalado em sua máquina.

### Opção 1: Usando o Mise (Recomendado)
O **Mise** gerencia as dependências e o ambiente virtual de forma automatizada:

1. **Instalar dependências:**
   ```bash
   mise run install
   ```
2. **Executar o jogo:**
   ```bash
   mise run play
   ```

### Opção 2: Usando Poetry Diretamente
Se você preferir usar o **Poetry** de forma manual:

1. **Instalar dependências:**
   ```bash
   poetry install
   ```
2. **Executar o jogo:**
   ```bash
   poetry run play
   ```

### Opção 3: Usando Python Padrão (Sem gerenciadores)
Caso não queira usar Poetry ou Mise:

1. Instale o Pygame:
   ```bash
   pip install pygame
   ```
2. Execute o script principal:
   ```bash
   python src/main.py
   ```

---

## 📂 Estrutura do Projeto Organizada

```
├── assets/                  # Recursos de mídia do jogo
│   ├── audio/               # Trilhas sonoras e efeitos (.mp3)
│   ├── fonts/               # Fontes de texto (.ttf)
│   ├── images/              # Imagens e botões (.png)
│   └── gifs/                # Gifs das animações agrupados por categorias
│       ├── menu/            # Animações de fundo do menu
│       ├── intro/           # Transição "New Challenger"
│       ├── challenger/      # Elementos visuais da transição
│       ├── gameover/        # Animações de coração quebrando (GameOver)
│       ├── refused/         # Animações do coração se recusando a quebrar
│       ├── explode/         # Animação de desistência e explosão
│       └── pulso/           # Coração pulsante durante o jogo
├── src/                     # Código fonte
│   ├── main.py              # Ponto de entrada (Main loop e estados)
│   ├── funcoes.py           # Funções lógicas e telas secundárias
│   ├── animation.py         # Carregamento e escala das animações
│   └── paths.py             # Auxiliar para caminhos dinâmicos de assets
├── .gitignore               # Configurações do Git
├── pyproject.toml           # Arquivo de configuração Poetry
├── mise.toml                # Arquivo de configuração de tarefas Mise
└── README.md                # Esta documentação
```
