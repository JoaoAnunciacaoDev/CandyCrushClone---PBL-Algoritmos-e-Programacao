import pygame, sys, random, animation, json
from pygame.locals import *

try:
    with open('pontuação.json', 'r') as arquivo: # Abrindo o arquivo de pontuações e atribuindo a variável pontuacoes
        pontuacoes = json.load(arquivo)
except FileNotFoundError:
        pontuacoes = {"JAO": "10000", "Sak": "40", "ChL": "30", "Ken": "20", "Ryu": "10"}

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

xcor, ycor, zcor, xSelecao, ySelecao, enter, gameOver, perguntaReset, prima, segunda, terca, reset, primeiraLetra, segundaLetra, terceiraLetra, primeiraRodada, começaTocar, contadorGame, x, y, tempo = variaveisPadrao()

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
    if len(pontuacoes) >= 6: # É armazenado apenas 5 pontuações, caso passe disso, o último será removido até sobrar somente 5
        pontuacoes.popitem()
    with open('pontuação.json', 'w') as arquivo: # É escrito a pontuação no arquivo
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

def guardarSequencias(pontuacao): # Função utilizada para guardar as coordenadas das sequências encontradas na matriz
    pecas_marcadas = set() # utilizado para armazenar elementos únicos, dessa forma é armazenado as coordenadas sem repetir

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

def pintandoPreto(pecas_marcadas): # Função utilizada para pintar as sequências guardadas de preto
    velocidade = 100
    for i, j in pecas_marcadas:
        matriz[i][j] = preto
        esperaAnima(velocidade)
    
def subirPreto(): # Função utilizada para por as cores pretas para cima e descer as que não são pretas
    velocidade = 150
    for k in range(6):
        for i in range(6):
            for j in range(1, 6):
                if matriz[i][j] == preto:
                    matriz[i][j] = matriz[i][j - 1] 
                    matriz[i][j - 1] = preto
                    esperaAnima(velocidade)            
                
def preencherPreto(): # Função utilizada para preencher as cores pretas após subirem
    velocidade = 75
    for i in range(5, -1, -1):
        for j in range(5, -1, -1):
            if matriz[i][j] == preto:
                matriz[i][j] = random.choice(cores)
                esperaAnima(velocidade)              

def calculoPontuacao(pontuacao, pecas_marcadas): # Função utilizada para calcular os pontos gerados pelas combinações de cores
    cor_pontuacao = {
        amarelo: 20,
        verde: 30,
        vermelho: 35,
        azul: 40,
        violeta: 50,
    }

    for i, j in pecas_marcadas:
        cor_peca = matriz[i][j]  # Obtem a cor da peça
        if cor_peca in cor_pontuacao: # soma a pontuação de acordo com as cores que foram combinadas
            pontuacao += cor_pontuacao[cor_peca]

    return pontuacao

def dicas(matriz): # Função que encontra uma possível combinação para mostrar ao jogador
    for i in range(tamanhoMatriz):
        for j in range(tamanhoMatriz - 1):
            # Troca os doces adjacentes na mesma linha
            matriz[i][j], matriz[i][j + 1] = matriz[i][j + 1], matriz[i][j]
            if verificarSequencias(matriz): # Caso após a troca haja combinação
                matriz[i][j], matriz[i][j + 1] = matriz[i][j + 1], matriz[i][j] # retorna as peças a sua posição inicial
                l = True
                return i, j, l
            matriz[i][j], matriz[i][j + 1] = matriz[i][j + 1], matriz[i][j]

    for i in range(tamanhoMatriz - 1):
        for j in range(tamanhoMatriz):
            # Troca os doces adjacentes na mesma coluna
            matriz[i][j], matriz[i + 1][j] = matriz[i + 1][j], matriz[i][j]
            if verificarSequencias(matriz):
                matriz[i][j], matriz[i + 1][j] = matriz[i + 1][j], matriz[i][j]
                l = False
                return i, j, l
            matriz[i][j], matriz[i + 1][j] = matriz[i + 1][j], matriz[i][j]
 
    matriz = [[random.choice(cores) for i in range(tamanhoMatriz)] for j in range(tamanhoMatriz)] # se nenhuma dica foi encontrada, é indicado que não há jogadas possíveis, e então é gerada uma nova matriz

def desenhoDica(i, j, direcao): # Função que desenha a dica na tela para visualização do jogador
    if direcao:
        x = 223 + i * 60 # Ajusta para a posição da matriz
        y = 223 + j * 60  
        y1 = 223 + (j + 1) * 60 
        pygame.draw.rect(tela, (255, 165, 0), (x, y, 54, 54), 2)
        pygame.draw.rect(tela, (255, 165, 0), (x, y1, 54, 54), 2)
    else:
        x = 223 + i * 60  # Ajusta para a posição da matriz
        y = 223 + j * 60 
        x1 = 223 + (i + 1) * 60 
        pygame.draw.rect(tela, (255, 165, 0), (x, y, 54, 54), 2)
        pygame.draw.rect(tela, (255, 165, 0), (x1, y, 54, 54), 2)

def esperaAnima(velocidade): # Função utilizada para esperar o movimento das peças, para facilitar a visualização nos testes
    pygame.display.flip()
    pygame.time.wait(velocidade)
    printMatriz(x, y) 

def pagPontuacao(): # Função utilizada para criar a página de pontuação
    font = pygame.font.Font("Street Fighter Alpha 3(Small).ttf", 20) # Renderização dos textos
    titulo = font.render('Candy Crush da Deep Web', True, (0, 255, 255))
    subtitulo = font.render('Pontuacoes', True, (0, 255, 255))
    primeiro = font.render('1º', True, (0, 255, 255))
    segundo = font.render('2º', True, (0, 255, 255))
    terceiro = font.render('3º', True, (0, 255, 255))
    quarto = font.render('4º', True, (0, 255, 255))
    quinto = font.render('5º', True, (0, 255, 255))

    rodando = True # variável usada para controlar o loop
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

        y = 200 # posição inicial do texto da pontuação

        for chave, valor in pontuacoes.items(): # laço de repetição utilizado para mostrar os nomes e as pontuações respectivamente
            texto_chave = font.render(chave, True, (0, 255, 255))
            texto_valor = font.render(valor, True, (0, 255, 255))
            tela.blit(texto_chave, (375, y))
            tela.blit(texto_valor, (600, y))
            y += 50           

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN: 
                if event.key == K_ESCAPE: # Caso aperte ESC o jogo fecha
                    pygame.quit()
                    sys.exit()
                if event.key == K_SPACE: # Caso aperte espaço é retornado ao menu principal
                    rodando = False
                    botaoMenu()

        pygame.display.update()

def intro(): # Função utilizada para controlar a animação de "Here comes a new challenger"
    contador = 0

    pygame.mixer.music.load('herecomes.mp3') # Começa a tocar áudio
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
            tela.blit(animation.lista3[contador], (100, 100)) # Controle da animação
            contador += 1
        elif contador == 48:
            rodando = False
        pygame.display.update()

def botaoMenu(): # Função utilizada para controlar o menu principal
    botaoJogarImagem = pygame.image.load('jogar.png') # Carregando as imagens
    botaoPontuacaoImagem = pygame.image.load('pontuacao.png')
    botaoSairImagem = pygame.image.load('sair.png')
    backgroundImagem = pygame.image.load('background.png')
    background = pygame.transform.scale(backgroundImagem, (800, 600))

    class botoes(): # declarando a classe para os botões
        def __init__(self, x_botao, y_botao, image):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = (x_botao, y_botao)
        def draw(self):
            tela.blit(self.image, (self.rect.x, self.rect.y))

    botaoJogar = botoes(250, 200, botaoJogarImagem) # instâncias dos botões
    botaoPontuacao = botoes(250, 400, botaoPontuacaoImagem)
    botaoSair = botoes(250, 600, botaoSairImagem)

    xSelecaoMenu = 243 # coordenadas do retângulo de seleção do menu
    ySelecaoMenu = 193

    font = pygame.font.Font("Street Fighter Alpha 3(Small).ttf", 20) # delcaração da fonte
    titulo = font.render('Candy Crush da Deep Web', True, (0, 255, 255)) # renderização do titulo

    tempoInicial = pygame.time.get_ticks() # Usado para ter informação do tempo, para a animação do menu

    contadora = contador = 0
    bpm = 15

    pygame.mixer.music.load('startTheme.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    rodando = True
    while rodando: # loop principal do menu
            contadora += 1
            clock.tick(bpm) # usar para controlar os frames do jogo

            tela.fill((0, 0, 0))

            tela.blit(background, (0, -120)) # mostra o fundo
            tela.blit(titulo, (170, 70)) # mostra o titulo
            tela.blit(animation.lista[contadora], (30, 560)) # mostra os frames da animação

            selecao = pygame.draw.rect(tela, (255, 255, 255), (xSelecaoMenu, ySelecaoMenu, 310, 150), 2) # desenha na tela o retângulo de seleção
            botaoJogar.draw() # desenho dos botões na tela
            botaoPontuacao.draw()  
            botaoSair.draw()
               
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN: 
                    if event.key == K_ESCAPE: # caso o jogador pressione ESC o jogo fecha
                        pygame.quit()
                        sys.exit()
                    if event.key == K_KP_ENTER or event.key == K_RETURN: # Caso aperte enter ou return, significa que o jogador selecionou algum botão
                        if selecao.colliderect(botaoJogar): # verifica se o botão selecionado foi o Jogar
                            selecao = pygame.draw.rect(tela, (255, 255, 255), (xSelecaoMenu, ySelecaoMenu, 310, 150)) # troca a forma de preenchimento do retângulo
                            rodando = False # encerra o loop
                            pygame.mixer.music.stop() # para a música
                            intro() # chama a introdução
                            return # return para encerrar a função atual
                        elif selecao.colliderect(botaoPontuacao): # verifica se o botão selecionado foi o Pontuacao
                            selecao = pygame.draw.rect(tela, (255, 255, 255), (xSelecaoMenu, ySelecaoMenu, 310, 150)) # troca a forma de preenchimento do retângulo
                            rodando = False # encerra o loop
                            pygame.mixer.music.stop() # para a música
                            pagPontuacao() # chama a página de pontuação
                            return # return para encerrar a função atual
                        elif selecao.colliderect(botaoSair): # verifica se o botão selecionado foi o Sair
                            pygame.quit() # encerra o programa
                            sys.exit()
                    if event.key == K_w or event.key == K_UP: # verificação da direção para onde o retângulo seleção vai
                        if ySelecaoMenu != 193: # é permitido ir pra cima apenas até o botão Jogar
                            ySelecaoMenu -= 200
                    if event.key == K_s or event.key == K_DOWN:
                        if ySelecaoMenu != 593: # é permitido ir pra baixo apenas até o botão Sairr
                            ySelecaoMenu += 200                    
                            
            if contadora == 42: # controle da animação
                contadora = 0
            if contador == 7:
                contador = 0
            
            comparacaoTempo = pygame.time.get_ticks() - tempoInicial # controle da animação
            if comparacaoTempo >= 18000:
                bpm = 30
                contador += 1
                pygame.mixer.music.set_volume(0.8)
                tela.blit(animation.lista2[contador], (560, 500))

            pygame.display.update() # função para atualizar a cada interação do loop principal    
