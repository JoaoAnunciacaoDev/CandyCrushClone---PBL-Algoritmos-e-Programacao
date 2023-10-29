import pygame, sys, random, animation, json
from pygame.locals import *

with open('pontuação.json', 'r') as arquivo: # Abrindo o arquivo de pontuações e atribuindo a variável pontuacoes
    pontuacoes = json.load(arquivo)

pygame.init() # iniciando o pygame

largura = 800 # definindo a largura da janela
altura = 800 # definindo a altura da janela
recuo = 20 # definindo o recuo para espaçar os quadrados desenhados na tela
tamanhoMatriz = 6 # definindo o tamanho da matriz
tamanhoQuadrado = 40 # definindo o tamanho dos quadrados

tela = pygame.display.set_mode((largura, altura)) # criando a janela de exibição do jogo
pygame.display.set_caption('Candy Crush da Deep Web') # Definindo o título da janela
font = pygame.font.Font('Street Fighter Alpha 3(Small).ttf', 20) # Definindo a fonte utilizada para textos médios
font2 = pygame.font.Font('Street Fighter Alpha 3(Small).ttf', 60) # Definindo a fonte utilizada para textos maiores
font3 = pygame.font.Font('Street Fighter Alpha 3(Small).ttf', 15) # Definindo a fonte utilizada para textos pequenos
clock = pygame.time.Clock() # Criando o objeto clock para controlar a taxa de frames

abc = [chr(i) for i in range(65, 91)] # Criando lista com as 26 letras do alfabeto, usada para o jogador inserir um nome na pontuação
abc.append('_') # Acrescentando a underline na lista de alfabeto

# Definição das cores das gemas e da lista de cores
violeta = (128, 0, 128)
amarelo = (255, 255, 0)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)
preto = (0, 0, 0)
cores = [azul, vermelho, verde, amarelo, violeta]

enter = gameOver = perguntaReset = segunda = terca = reset = False
primeiraLetra = segundaLetra = terceiraLetra = 26
primeiraRodada = começaTocar = prima = True
xSelecao = ySelecao = 225
xcor = ycor = zcor = 255
contadorGame = 0
x = y = 230
tempo = 20

Img = pygame.image.load('Fundo.png')
Fundo = pygame.transform.scale(Img, (800, 800))

matriz = [[cores[random.randint(0,4)] for i in range(tamanhoMatriz)] for j in range(tamanhoMatriz)]

def verificarSequencias(matriz): # Função utilizada para verificar se há sequências de 3 na matriz
    for i in range(tamanhoMatriz):
        for j in range(tamanhoMatriz - 2):
            if matriz[i][j] == matriz[i][j + 1] == matriz[i][j + 2] and matriz[i][j] != preto:
                return True
    for j in range(tamanhoMatriz):
        for i in range(tamanhoMatriz - 2):
            if matriz[i][j] == matriz[i + 1][j] == matriz[i + 2][j] and matriz[i][j] != preto:
                return True
    return False

def evitarRepetidos(matriz): # Função utilizada para evitar combinações já feitas no início do jogo
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

def variaveisPadrao(): # Função utilizada para trazer as variáveis seus valores de fábrica                
    xcor = ycor = zcor = 255
    xSelecao = ySelecao = 225
    enter = gameOver = perguntaReset = segunda = terca = reset = False
    primeiraLetra = segundaLetra = terceiraLetra = 26
    primeiraRodada = começaTocar = prima = True
    contadorGame = 0
    x = y = 230
    tempo = 20
    return xcor, ycor, zcor, xSelecao, ySelecao, enter, gameOver, perguntaReset, prima, segunda, terca, reset, primeiraLetra, segundaLetra, terceiraLetra, primeiraRodada, começaTocar, contadorGame, x, y, tempo

def inicioJogo(tamanhoMatriz, cores): # Função utilizada para seus valores de início de jogo
    matriz = [[cores[random.randint(0,4)] for i in range(tamanhoMatriz)] for j in range(tamanhoMatriz)]
    dicaTela = False
    pontuacao = 0
    qtdJogadas = 5
    while verificarSequencias(matriz) == True:
        matriz = evitarRepetidos(matriz)
    pygame.mixer.music.load('AsrielTheme.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    return matriz, pontuacao, qtdJogadas, dicaTela

def salvar_pontuacao(pontuacao): # Função utilizada para guardar o scoreboard, são guardados apenas os 5 melhores, caso passe de 5 é removido
    if len(pontuacoes) >= 6:
        pontuacoes.popitem()
    with open('pontuação.json', 'w') as arquivo:
        json.dump(pontuacoes, arquivo, indent=4)

def printMatriz(x, y): # Função utilizada para desenhar a matriz de cores na tela
    for linha in range(tamanhoMatriz):
        for coluna in range(tamanhoMatriz):
            cor = matriz[linha][coluna]
            pygame.draw.rect(tela, cor, (x, y, tamanhoQuadrado, tamanhoQuadrado))
            y += recuo + tamanhoQuadrado 
        x += recuo + tamanhoQuadrado  
        y = 230

def posQuadrado(ySelecao, xSelecao, enter): # Função utilizada para relacionar a posição do quadrado desenhado na tela com o elemento da matriz
    pos_quadrado = (ySelecao, xSelecao)
    pos_x = (pos_quadrado[1] // 60) - 3 # com os seguintes cálculos será retornado um número de 0 a 5
    pos_y = (pos_quadrado[0] // 60) - 3
    enter = False
    return pos_x,pos_y, enter

def guardarSequencias(pontuacao):
    pecas_marcadas = set()

    for i in range(6):
        for j in range(4):                
            if matriz[i][j] == matriz[i][j + 1] == matriz[i][j + 2] and matriz[i][j] != preto:
                if (i, j) not in pecas_marcadas:
                    pecas_marcadas.add((i, j))
                    pecas_marcadas.add((i, j + 1))
                    pecas_marcadas.add((i, j + 2))
                else:
                    pecas_marcadas.add((i, j + 2))

    for i in range(4):
        for j in range(6):
            if matriz[i][j] == matriz[i + 1][j] == matriz[i + 2][j] and matriz[i][j] != preto:
                if (i, j) not in pecas_marcadas:
                    pecas_marcadas.add((i, j))
                    pecas_marcadas.add((i + 1, j))
                    pecas_marcadas.add((i + 2, j))
                else:
                    pecas_marcadas.add((i + 2, j))
   
    pontuacao = calculoPontuacao(pontuacao, pecas_marcadas)
    pintandoPreto(pecas_marcadas)             

    return pontuacao


def pintandoPreto(pecas_marcadas):
    for i, j in pecas_marcadas:
        matriz[i][j] = preto
        print(i, j)
        esperaAnima()
    

def subirPreto(): # Função utilizada para por as cores pretas para cima e descer as que não são pretas
    for k in range(6):
        for i in range(6):
            for j in range(1, 6):
                if matriz[i][j] == preto:
                    matriz[i][j] = matriz[i][j - 1] 
                    matriz[i][j - 1] = preto
                    esperaAnima()            
                
def preencherPreto(): # Função utilizada para preencher as cores pretas após subirem
    for i in range(5, -1, -1):
        for j in range(5, -1, -1):
            if matriz[i][j] == preto:
                matriz[i][j] = random.choice(cores)
                esperaAnima()              

def calculoPontuacao(pontuacao, pecas_marcadas):
    cor_pontuacao = {
        amarelo: 20,
        verde: 30,
        vermelho: 35,
        azul: 40,
        violeta: 50,
    }

    for i, j in pecas_marcadas:
        cor_peca = matriz[i][j]  # Obtenha a cor da peça
        if cor_peca in cor_pontuacao:
            pontuacao += cor_pontuacao[cor_peca]

    return pontuacao


def dicas(matriz): # Função que encontra uma possível combinação para mostrar ao jogador
    encontrado = False
    for i in range(tamanhoMatriz):
        for j in range(tamanhoMatriz - 1):
            # Troque os doces adjacentes na mesma linha
            matriz[i][j], matriz[i][j + 1] = matriz[i][j + 1], matriz[i][j]
            if verificarSequencias(matriz):
                encontrado = True
                matriz[i][j], matriz[i][j + 1] = matriz[i][j + 1], matriz[i][j]
                l = True
                return i, j, l
            matriz[i][j], matriz[i][j + 1] = matriz[i][j + 1], matriz[i][j]

    for i in range(tamanhoMatriz - 1):
        for j in range(tamanhoMatriz):
            # Troque os doces adjacentes na mesma coluna
            matriz[i][j], matriz[i + 1][j] = matriz[i + 1][j], matriz[i][j]
            if verificarSequencias(matriz):
                encontrado = True
                matriz[i][j], matriz[i + 1][j] = matriz[i + 1][j], matriz[i][j]
                l = False
                return i, j, l
            matriz[i][j], matriz[i + 1][j] = matriz[i + 1][j], matriz[i][j]

    if not encontrado:
        matriz = [[random.choice(cores) for i in range(tamanhoMatriz)] for j in range(tamanhoMatriz)]

def desenhoDica(i, j, direcao): # Função que desenha a dica na tela para visualização do jogador
    if direcao:
        x = 223 + i * 60 # Ajuste para a posição da matriz
        y = 223 + j * 60  # Ajuste para a posição da matriz
        y1 = 223 + (j + 1) * 60 # Ajuste para a posição da matriz
        pygame.draw.rect(tela, (255, 165, 0), (x, y, 54, 54), 2)
        pygame.draw.rect(tela, (255, 165, 0), (x, y1, 54, 54), 2)
    else:
        x = 223 + i * 60  # Ajuste para a posição da matriz
        y = 223 + j * 60 # Ajuste para a posição da matriz
        x1 = 223 + (i + 1) * 60 # Ajuste para a posição da matriz
        pygame.draw.rect(tela, (255, 165, 0), (x, y, 54, 54), 2)
        pygame.draw.rect(tela, (255, 165, 0), (x1, y, 54, 54), 2)

def esperaAnima(): # Função utilizada para esperar o movimento das peças, para facilitar a visualização nos testes
    pygame.display.flip()
    pygame.time.wait(85)
    printMatriz(x, y) 

def pagPontuacao(): # Função utilizada para criar a página de pontuação
    font = pygame.font.Font("Street Fighter Alpha 3(Small).ttf", 20)
    titulo = font.render('Candy Crush da Deep Web', True, (0, 255, 255))
    subtitulo = font.render('Pontuacoes', True, (0, 255, 255))
    primeiro = font.render('1º', True, (0, 255, 255))
    segundo = font.render('2º', True, (0, 255, 255))
    terceiro = font.render('3º', True, (0, 255, 255))
    quarto = font.render('4º', True, (0, 255, 255))
    quinto = font.render('5º', True, (0, 255, 255))
    rodando = True
    while rodando:
        clock.tick(10) # usar para controlar os frames do jogo
        tela.fill((0, 0, 0))
        tela.blit(titulo, (170, 70))
        tela.blit(subtitulo, (300, 100))
        tela.blit(primeiro, (170, 200))
        tela.blit(segundo, (170, 250))
        tela.blit(terceiro, (170, 300))
        tela.blit(quarto, (170, 350))
        tela.blit(quinto, (170, 400))
        conta = 1
        y = 200
        for chave, valor in pontuacoes.items():
            if conta <= 5:
                texto_chave = font.render(chave, True, (0, 255, 255))
                texto_valor = font.render(valor, True, (0, 255, 255))
                tela.blit(texto_chave, (375, y))
                tela.blit(texto_valor, (600, y))
                y += 50
                conta += 1            

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

def intro(): # Função utilizada para controlar a animação de "Here comes a new challenger"
    contador = 0

    pygame.mixer.music.load('herecomes.mp3')
    pygame.mixer.music.play(0)
    pygame.mixer.music.set_volume(0.5)

    run = True
    while run:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()

        tela.fill(preto)

        if contador < 48:
            tela.blit(animation.lista3[contador], (100, 100))
            contador += 1
        elif contador == 48:
            run = False
        pygame.display.update()

def botaoMenu(): # Função utilizada para controlar o menu principal
    botaoJogarImage = pygame.image.load('jogar.png')
    botaoPontuacaoImage = pygame.image.load('pontuacao.png')
    botaoSairImage = pygame.image.load('sair.png')
    backgroundImage = pygame.image.load('background.png')
    background = pygame.transform.scale(backgroundImage, (800, 600))

    class botoes():
        def __init__(self, x_botao, y_botao, image):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = (x_botao, y_botao)
        def draw(self):
            tela.blit(self.image, (self.rect.x, self.rect.y))

    botaoJogar = botoes(250, 200, botaoJogarImage)
    botaoPontuacao = botoes(250, 400, botaoPontuacaoImage)
    botaoSair = botoes(250, 600, botaoSairImage)

    xSelecaoMenu = 243
    ySelecaoMenu = 193

    font = pygame.font.Font("Street Fighter Alpha 3(Small).ttf", 20)
    titulo = font.render('Candy Crush da Deep Web', True, (0, 255, 255))

    tempoInicial = pygame.time.get_ticks()

    contadora = contador = 0
    bpm = 15

    pygame.mixer.music.load('startTheme.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    run = True
    while run: # loop principal do menu
            contadora += 1
            clock.tick(bpm) # usar para controlar os frames do jogo

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
                            run = False
                            pygame.mixer.music.stop()
                            intro()
                            return
                        elif selecao.colliderect(botaoPontuacao):
                            selecao = pygame.draw.rect(tela, (255, 255, 255), (xSelecaoMenu, ySelecaoMenu, 310, 150))
                            run = False
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

            pygame.display.update() # função para atualizar a cada interação do loop principal    
