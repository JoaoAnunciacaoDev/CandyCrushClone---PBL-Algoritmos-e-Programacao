import pygame
import sys
import random
import json
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import animation
from paths import get_asset_path, BASE_DIR
from pygame.locals import (
    QUIT,
    KEYDOWN,
    K_ESCAPE,
    K_SPACE,
    K_KP_ENTER,
    K_RETURN,
    K_w,
    K_UP,
    K_s,
    K_DOWN,
)

SCORE_FILE = os.path.join(BASE_DIR, "pontuacao.json")

try:
    with open(SCORE_FILE, "r", encoding="utf-8") as arquivo:
        pontuacoes = json.load(arquivo)
except FileNotFoundError:
    pontuacoes = {"JAO": "10000", "Sak": "40", "ChL": "30", "Ken": "20", "Ryu": "10"}

pygame.init()

largura = 800
altura = 800
recuo = 20
tamanhoMatriz = 6
tamanhoQuadrado = 40

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Candy Crush da Deep Web")


FONT_PATH = get_asset_path("fonts", "Street Fighter Alpha 3(Small).ttf")
font = pygame.font.Font(FONT_PATH, 20)
font2 = pygame.font.Font(FONT_PATH, 60)
font3 = pygame.font.Font(FONT_PATH, 15)
clock = pygame.time.Clock()

abc = [chr(i) for i in range(65, 91)]
abc.append("_")


violeta = (128, 0, 128)
amarelo = (255, 255, 0)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)
preto = (0, 0, 0)
cores = [azul, vermelho, verde, amarelo, violeta]


Img = pygame.image.load(get_asset_path("images", "background.png"))
Fundo = pygame.transform.scale(Img, (800, 800))

matriz = [[cores[random.randint(0, 4)] for i in range(tamanhoMatriz)] for j in range(tamanhoMatriz)]


def verificarSequencias(matriz):
    for i in range(tamanhoMatriz):
        for j in range(tamanhoMatriz - 2):
            if matriz[i][j] == matriz[i][j + 1] == matriz[i][j + 2] and matriz[i][j] != preto:
                return True
    for j in range(tamanhoMatriz):
        for i in range(tamanhoMatriz - 2):
            if matriz[i][j] == matriz[i + 1][j] == matriz[i + 2][j] and matriz[i][j] != preto:
                return True
    return False


def evitarRepetidos(matriz):
    for i in range(tamanhoMatriz):
        for j in range(tamanhoMatriz - 2):
            if matriz[i][j] == matriz[i][j + 1] == matriz[i][j + 2]:
                nova_cor = random.choice(cores)
                while nova_cor == matriz[i][j + 1]:
                    nova_cor = random.choice(cores)
                matriz[i][j] = nova_cor

            if matriz[j][i] == matriz[j + 1][i] == matriz[j + 2][i]:
                nova_cor = random.choice(cores)
                while nova_cor == matriz[j + 1][i]:
                    nova_cor = random.choice(cores)
                matriz[j][i] = nova_cor
    return matriz


matriz = evitarRepetidos(matriz)


def variaveisPadrao():
    xcor = ycor = zcor = 255
    xSelecao = ySelecao = 225
    enter = gameOver = perguntaReset = segunda = terca = reset = False
    primeiraLetra = segundaLetra = terceiraLetra = 26
    primeiraRodada = começaTocar = prima = True
    contadorGame = 0
    x = y = 230
    tempo = 20
    return (
        xcor,
        ycor,
        zcor,
        xSelecao,
        ySelecao,
        enter,
        gameOver,
        perguntaReset,
        prima,
        segunda,
        terca,
        reset,
        primeiraLetra,
        segundaLetra,
        terceiraLetra,
        primeiraRodada,
        começaTocar,
        contadorGame,
        x,
        y,
        tempo,
    )


(
    xcor,
    ycor,
    zcor,
    xSelecao,
    ySelecao,
    enter,
    gameOver,
    perguntaReset,
    prima,
    segunda,
    terca,
    reset,
    primeiraLetra,
    segundaLetra,
    terceiraLetra,
    primeiraRodada,
    começaTocar,
    contadorGame,
    x,
    y,
    tempo,
) = variaveisPadrao()


def inicioJogo(tamanhoMatriz, cores):
    matriz = [[cores[random.randint(0, 4)] for i in range(tamanhoMatriz)] for j in range(tamanhoMatriz)]
    dicaTela = False
    pontuacao = 0
    qtdJogadas = 5
    while verificarSequencias(matriz):
        matriz = evitarRepetidos(matriz)
    pygame.mixer.music.load(get_asset_path("audio", "AsrielTheme.mp3"))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    return matriz, pontuacao, qtdJogadas, dicaTela


def salvar_pontuacao(pontuacao):
    if len(pontuacoes) >= 6:
        pontuacoes.popitem()
    with open(SCORE_FILE, "w", encoding="utf-8") as arquivo:
        json.dump(pontuacoes, arquivo, indent=4)


def printMatriz(x, y):
    for linha in range(tamanhoMatriz):
        for coluna in range(tamanhoMatriz):
            cor = matriz[linha][coluna]
            pygame.draw.rect(tela, cor, (x, y, tamanhoQuadrado, tamanhoQuadrado))
            y += recuo + tamanhoQuadrado
        x += recuo + tamanhoQuadrado
        y = 230


def posQuadrado(ySelecao, xSelecao, enter):
    pos_quadrado = (ySelecao, xSelecao)
    pos_x = (pos_quadrado[1] // 60) - 3
    pos_y = (pos_quadrado[0] // 60) - 3
    enter = False
    return pos_x, pos_y, enter


def guardarSequencias(pontuacao):
    pecas_marcadas = set()

    for i in range(6):
        for j in range(4):
            if matriz[i][j] == matriz[i][j + 1] == matriz[i][j + 2] and matriz[i][j] != preto:
                pecas_marcadas.add((i, j))
                pecas_marcadas.add((i, j + 1))
                pecas_marcadas.add((i, j + 2))

    for i in range(4):
        for j in range(6):
            if matriz[i][j] == matriz[i + 1][j] == matriz[i + 2][j] and matriz[i][j] != preto:
                pecas_marcadas.add((i, j))
                pecas_marcadas.add((i + 1, j))
                pecas_marcadas.add((i + 2, j))

    pontuacao = calculoPontuacao(pontuacao, pecas_marcadas)
    pintandoPreto(pecas_marcadas)

    return pontuacao


def pintandoPreto(pecas_marcadas):
    velocidade = 100
    for i, j in pecas_marcadas:
        matriz[i][j] = preto
        esperaAnima(velocidade)


def subirPreto():
    velocidade = 150
    for k in range(6):
        for i in range(6):
            for j in range(1, 6):
                if matriz[i][j] == preto:
                    matriz[i][j] = matriz[i][j - 1]
                    matriz[i][j - 1] = preto
                    esperaAnima(velocidade)


def preencherPreto():
    velocidade = 75
    for i in range(5, -1, -1):
        for j in range(5, -1, -1):
            if matriz[i][j] == preto:
                matriz[i][j] = random.choice(cores)
                esperaAnima(velocidade)


def calculoPontuacao(pontuacao, pecas_marcadas):
    cor_pontuacao = {
        amarelo: 20,
        verde: 30,
        vermelho: 35,
        azul: 40,
        violeta: 50,
    }

    for i, j in pecas_marcadas:
        cor_peca = matriz[i][j]
        if cor_peca in cor_pontuacao:
            pontuacao += cor_pontuacao[cor_peca]

    return pontuacao


def dicas(matriz):
    for i in range(tamanhoMatriz):
        for j in range(tamanhoMatriz - 1):
            matriz[i][j], matriz[i][j + 1] = matriz[i][j + 1], matriz[i][j]
            if verificarSequencias(matriz):
                matriz[i][j], matriz[i][j + 1] = matriz[i][j + 1], matriz[i][j]
                dica_direcao = True
                return i, j, dica_direcao
            matriz[i][j], matriz[i][j + 1] = matriz[i][j + 1], matriz[i][j]

    for i in range(tamanhoMatriz - 1):
        for j in range(tamanhoMatriz):
            matriz[i][j], matriz[i + 1][j] = matriz[i + 1][j], matriz[i][j]
            if verificarSequencias(matriz):
                matriz[i][j], matriz[i + 1][j] = matriz[i + 1][j], matriz[i][j]
                dica_direcao = False
                return i, j, dica_direcao
            matriz[i][j], matriz[i + 1][j] = matriz[i + 1][j], matriz[i][j]

    matriz = [[random.choice(cores) for i in range(tamanhoMatriz)] for j in range(tamanhoMatriz)]


def desenhoDica(i, j, direcao):
    if direcao:
        x = 223 + i * 60
        y = 223 + j * 60
        y1 = 223 + (j + 1) * 60
        pygame.draw.rect(tela, (255, 165, 0), (x, y, 54, 54), 2)
        pygame.draw.rect(tela, (255, 165, 0), (x, y1, 54, 54), 2)
    else:
        x = 223 + i * 60
        y = 223 + j * 60
        x1 = 223 + (i + 1) * 60
        pygame.draw.rect(tela, (255, 165, 0), (x, y, 54, 54), 2)
        pygame.draw.rect(tela, (255, 165, 0), (x1, y, 54, 54), 2)


def esperaAnima(velocidade):
    pygame.display.flip()
    pygame.time.wait(velocidade)
    printMatriz(x, y)


def pagPontuacao():
    titulo = font.render("Candy Crush da Deep Web", True, (0, 255, 255))
    subtitulo = font.render("Pontuacoes", True, (0, 255, 255))
    primeiro = font.render("1º", True, (0, 255, 255))
    segundo = font.render("2º", True, (0, 255, 255))
    terceiro = font.render("3º", True, (0, 255, 255))
    quarto = font.render("4º", True, (0, 255, 255))
    quinto = font.render("5º", True, (0, 255, 255))

    rodando = True
    while rodando:
        clock.tick(10)
        tela.fill((0, 0, 0))
        tela.blit(titulo, (170, 70))
        tela.blit(subtitulo, (300, 100))
        tela.blit(primeiro, (170, 200))
        tela.blit(segundo, (170, 250))
        tela.blit(terceiro, (170, 300))
        tela.blit(quarto, (170, 350))
        tela.blit(quinto, (170, 400))

        y_pos = 200

        for chave, valor in pontuacoes.items():
            texto_chave = font.render(chave, True, (0, 255, 255))
            texto_valor = font.render(valor, True, (0, 255, 255))
            tela.blit(texto_chave, (375, y_pos))
            tela.blit(texto_valor, (600, y_pos))
            y_pos += 50

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_SPACE:
                    rodando = False
                    botaoMenu()

        pygame.display.update()


def intro():
    contador = 0

    pygame.mixer.music.load(get_asset_path("audio", "herecomes.mp3"))
    pygame.mixer.music.play(1)
    pygame.mixer.music.set_volume(0.5)

    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tela.fill(preto)
        clock.tick(10)

        if contador < 48:
            tela.blit(animation.lista3[contador], (100, 100))
            contador += 1
        elif contador == 48:
            rodando = False
        pygame.display.update()


def botaoMenu():
    botaoJogarImagem = pygame.image.load(get_asset_path("images", "jogar.png"))
    botaoPontuacaoImagem = pygame.image.load(get_asset_path("images", "pontuacao.png"))
    botaoSairImagem = pygame.image.load(get_asset_path("images", "sair.png"))
    backgroundImagem = pygame.image.load(get_asset_path("images", "background.png"))
    background = pygame.transform.scale(backgroundImagem, (800, 600))

    class botoes:
        def __init__(self, x_botao, y_botao, image):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = (x_botao, y_botao)

        def draw(self):
            tela.blit(self.image, (self.rect.x, self.rect.y))

    botaoJogar = botoes(250, 200, botaoJogarImagem)
    botaoPontuacao = botoes(250, 400, botaoPontuacaoImagem)
    botaoSair = botoes(250, 600, botaoSairImagem)

    xSelecaoMenu = 243
    ySelecaoMenu = 193

    titulo = font.render("Candy Crush da Deep Web", True, (0, 255, 255))

    tempoInicial = pygame.time.get_ticks()

    contadora = contador = 0
    bpm = 15

    pygame.mixer.music.load(get_asset_path("audio", "startTheme.mp3"))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    rodando = True
    while rodando:
        contadora += 1
        clock.tick(bpm)

        tela.fill((0, 0, 0))

        tela.blit(background, (0, -120))
        tela.blit(titulo, (170, 70))
        tela.blit(animation.lista[contadora], (30, 560))

        selecao = pygame.draw.rect(tela, (255, 255, 255), (xSelecaoMenu, ySelecaoMenu, 310, 150), 2)
        botaoJogar.draw()
        botaoPontuacao.draw()
        botaoSair.draw()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_KP_ENTER or event.key == K_RETURN:
                    if selecao.colliderect(botaoJogar):
                        selecao = pygame.draw.rect(tela, (255, 255, 255), (xSelecaoMenu, ySelecaoMenu, 310, 150))
                        rodando = False
                        pygame.mixer.music.stop()
                        intro()
                        return
                    elif selecao.colliderect(botaoPontuacao):
                        selecao = pygame.draw.rect(tela, (255, 255, 255), (xSelecaoMenu, ySelecaoMenu, 310, 150))
                        rodando = False
                        pygame.mixer.music.stop()
                        pagPontuacao()
                        return
                    elif selecao.colliderect(botaoSair):
                        pygame.quit()
                        sys.exit()
                if event.key == K_w or event.key == K_UP:
                    if ySelecaoMenu != 193:
                        ySelecaoMenu -= 200
                if event.key == K_s or event.key == K_DOWN:
                    if ySelecaoMenu != 593:
                        ySelecaoMenu += 200

        if contadora == 42:
            contadora = 0
        if contador == 7:
            contador = 0

        comparacaoTempo = pygame.time.get_ticks() - tempoInicial
        if comparacaoTempo >= 18000:
            bpm = 30
            contador += 1
            pygame.mixer.music.set_volume(0.8)
            tela.blit(animation.lista2[contador], (560, 500))

        pygame.display.update()
