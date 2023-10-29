import Funcoes
from Funcoes import *

#botaoMenu() # Chamada da função do Menu Principal

xcor, ycor, zcor, xSelecao, ySelecao, enter, gameOver, perguntaReset, prima, segunda, terca, reset, primeiraLetra, segundaLetra, terceiraLetra, primeiraRodada, começaTocar, contadorGame, x, y, tempo = variaveisPadrao()  

while True: # loop principal do jogo
    clock.tick(tempo) # usar para controlar os frames do jogo
    tela.fill(preto) # preencher tela na cor preta  

    if primeiraRodada: # Condicional para verificar a início do jogo, reiniciando apenas as variáveis necessárias
        Funcoes.matriz, Funcoes.pontuacao, Funcoes.qtdJogadas, Funcoes.dicaTela = inicioJogo(tamanhoMatriz, cores) 
        primeiraRodada = False

    if Funcoes.qtdJogadas == 0: # Condicional para verificar se a quantidade de jogadas chegou a zero, resultando no fim de jogo
        if verificarSequencias(Funcoes.matriz): # Apenas será permitido o fim de jogo após acabar as combinações
            gameOver = False
        else:
            pygame.time.wait(100)
            gameOver = True

    if contadorGame == 49: # Condicional para verificar o momento para a música de gameover começar
        if começaTocar:
            pygame.mixer.music.load('GameOverSong.mp3')
            pygame.mixer.music.play(1)
            pygame.mixer.music.set_volume(0.5)
            começaTocar = False

    if gameOver: # Condicional para verificar se o fim de jogo chegou
        tempo = 10

        if contadorGame == 0: # Condicional para parar a música logo no primeiro frame da animação de gameover
            pygame.mixer.music.stop()

        if contadorGame < 49: # Enquanto estiver em um elemento da lista antes do 49 continua passando para o próximo
            tela.blit(animation.listaGameOver[contadorGame], (200, 50))
            contadorGame += 1

            if contadorGame == 20: # No frame 20 toca a som de quebrar do coração
                pygame.mixer.music.load('broken.mp3')
                pygame.mixer.music.play(1)
                pygame.mixer.music.set_volume(0.8)

        elif contadorGame == 49 and not perguntaReset: # Quando chegar no elemento 49 da listaGameOver e ainda não chegou na pergunta de reinício
            textoGameOver = font2.render(f'GameOver', True, (255, 255, 255))
            textoInfoPontuacao = font.render(f'Sua pontuacao foi de {Funcoes.pontuacao}', True, (255, 255, 255))
            textoMensagem = font.render(f'(Isso te enche de determinacao.)', True, (255, 255, 255))

            letra1 = font.render(abc[primeiraLetra], True, (255, 255, 255))
            letra2 = font.render(abc[segundaLetra], True, (255, 255, 255))
            letra3 = font.render(abc[terceiraLetra], True, (255, 255, 255))

            tela.blit(animation.listaGameOver[48], (200, 50))
            tela.blit(textoGameOver, (175, 100))
            tela.blit(textoInfoPontuacao, (165, 500))
            tela.blit(textoMensagem, (80, 550))
            tela.blit(letra1, (350, 600))
            tela.blit(letra2, (400, 600))
            tela.blit(letra3, (450, 600))

        if perguntaReset: # Caso esteja no momento de perguntar sobre o reset
            salvar_pontuacao(Funcoes.pontuacao)
            
            textoInfoPontuacao = font.render(f'Deseja reiniciar o jogo?', True, (255, 255, 255))
            letra2 = font.render(abc[segundaLetra], True, (255, 255, 255))

            tela.blit(animation.listaGameOver[48], (200, 50))
            tela.blit(textoInfoPontuacao, (165, 500))
            tela.blit(letra2, (400, 600))

        if reset: # Caso esteja no momento de reiniciar
            if abc[segundaLetra] == "S": # Caso o jogador queira jogar novamente
                if contadorGame < 73:
                    tela.blit(animation.listaRefused[contadorGame], (200, 50))
                    contadorGame += 1
                    if contadorGame == 29:
                        pygame.mixer.music.load('somQuebra.mp3')
                        pygame.mixer.music.play(1)
                        pygame.mixer.music.set_volume(0.5)
                    if contadorGame == 73:
                        xcor, ycor, zcor, xSelecao, ySelecao, enter, gameOver, perguntaReset, prima, segunda, terca, reset, primeiraLetra, segundaLetra, terceiraLetra, primeiraRodada, começaTocar, contadorGame, x, y, tempo = variaveisPadrao()
            
            if abc[segundaLetra] == "N": # Caso o jogador não queira jogar novamente
                if contadorGame < 29:
                    tela.blit(animation.listaExplode[contadorGame], (178, 165)) # Roda a animação de quebra do coração antes de voltar ao menu
                    if contadorGame == 19:
                        pygame.mixer.music.load('somQuebra.mp3')
                        pygame.mixer.music.play(1)
                        pygame.mixer.music.set_volume(0.5)
                    contadorGame += 1
                else:
                    xcor, ycor, zcor, xSelecao, ySelecao, enter, gameOver, perguntaReset, prima, segunda, terca, reset, primeiraLetra, segundaLetra, terceiraLetra, primeiraRodada, começaTocar, contadorGame, x, y, tempo = variaveisPadrao()
                    botaoMenu()
    
    else: # Caso ainda não esteja no gameOver o jogo funciona normalmente
        pygame.draw.rect(tela, (18, 18, 18), (220, 220, 360, 360), border_radius = 10) # Desenha o tabuleiro onde as peças ficam
        selecao = pygame.draw.rect(tela, (xcor, ycor, zcor), (ySelecao, xSelecao, 50, 50), 2)

        if Funcoes.dicaTela:
            Funcoes.desenhoDica(a, b, dicaDirecao)

        if contadorGame < 12: # Controle da animaçã do coração pulsando
            tela.blit(animation.listaPulso[contadorGame], (325, 10))
            contadorGame += 1
        else:
            contadorGame = 0

        textoPontuacao = font.render(f'Pontuacao: {Funcoes.pontuacao}', True, (255, 255, 255)) # Armazenando o texto de jogadas, pontuaçõa e instruções
        textoJogadas = font.render(f'Jogadas: {Funcoes.qtdJogadas}', True, (255, 255, 255))
        textoInstrucao = font3.render(f'W/A/S/D ou SETAS para mover', True, (255, 255, 255))
        textoInstrucao2 = font3.render(f'ENTER para selecionar', True, (255, 255, 255))
        textoInstrucao3 = font3.render(f'H para pedir dica (Custo: 250p)', True, (255, 255, 255))
        textoInstrucao4 = font3.render(f'ESPACO para voltar ao menu', True, (255, 255, 255))
        textoInstrucao5 = font3.render(f'ESC para fechar o jogo', True, (255, 255, 255))

        tela.blit(textoPontuacao, (10, 10)) # Mostrando os textosna tela
        tela.blit(textoJogadas, (560, 10))
        tela.blit(textoInstrucao, (200, 600))
        tela.blit(textoInstrucao2, (250, 640))
        tela.blit(textoInstrucao3, (170, 680))
        tela.blit(textoInstrucao4, (215, 720))
        tela.blit(textoInstrucao5, (235, 760))
        
        printMatriz(x, y) # Chamando a função para desenhar a matriz na tela
        
        Funcoes.pontuacao = guardarSequencias(Funcoes.pontuacao) # Chamando a função para calcular a pontuação e eliminar as seguências

        subirPreto() # Chamando a função para subir as peças pretas
        preencherPreto() # Chamando a função para preencher as peças pretas com cores aleatórias
        
    for event in pygame.event.get(): # loop for para identificar quando um evento acontecer, por exemplo quando for pressionado uma tecla
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN: # Sair do programa quando pressionar a tecla ESC
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_w or event.key == K_UP: # Tecla W e Seta Up usadas para mover a seleção
                if Funcoes.qtdJogadas > 0: # Apenas permite o movimento do retângulo de seleção caso tenha jogadas disponíveis
                    if xSelecao > 225: # Condicional para evitar que o retângulo de seleção saia da matriz
                        xSelecao -= 60
                        xcor = ycor = zcor = 255 # Sempre que o retângulo de seleção é movido ele recebe a cor branca
                        if enter: # Se o jogador tiver apertado enter e em seguida apertou W ou Seta Cima ocorre a troca de peças
                            pos_x, pos_y, enter = posQuadrado(ySelecao, xSelecao, enter) # Armazenamos a posição da peça selecionada
                            Funcoes.matriz[pos_y][pos_x], Funcoes.matriz[pos_y][pos_x + 1] = Funcoes.matriz[pos_y][pos_x + 1], Funcoes.matriz[pos_y][pos_x] # Troca de peças
                            sequencia = verificarSequencias(Funcoes.matriz) # Verifica se houve uma sequência após alteração
                            if not sequencia: # Caso não há combinação após alteração ocorre a troca novamente
                                Funcoes.matriz[pos_y][pos_x], Funcoes.matriz[pos_y][pos_x + 1] = Funcoes.matriz[pos_y][pos_x + 1], Funcoes.matriz[pos_y][pos_x]

                            else:
                               Funcoes.qtdJogadas -= 1 # Caso haja, diminui a quantidade de jogadas
                            if Funcoes.dicaTela:
                                Funcoes.dicaTela = False
                                Funcoes.pontuacao -= 250
                                
                if gameOver: # Se estivermos na tela de gameOver, o jogador passa a controlar as letras para escrever seu nome
                    if prima: # Verifica se o jogador está na primeira letra
                        if primeiraLetra > 0:
                            primeiraLetra -= 1
                        else:
                            primeiraLetra = 26
                    if segunda: # Verifica se o jogador está na segunda letra
                        if segundaLetra > 0:
                            segundaLetra -= 1
                        else:
                            segundaLetra = 26
                    if terca: # Verifica se o jogador está na terceira letra
                        if terceiraLetra > 0:
                            terceiraLetra -= 1
                        else:
                            terceiraLetra = 26
                    if perguntaReset: # Caso esteja na tela da pergunta de reinício
                        segundaLetra = 18
                        
            if event.key == K_s or event.key == K_DOWN: # Tecla D e Seta Down usadas para mover a seleção
                if Funcoes.qtdJogadas > 0:
                    if xSelecao < 525: # Condicional para evitar que o retângulo de seleção saia da matriz
                        xSelecao += 60
                        xcor = ycor = zcor = 255
                        if enter:
                            pos_x, pos_y, enter = posQuadrado(ySelecao, xSelecao, enter)
                            Funcoes.matriz[pos_y][pos_x], Funcoes.matriz[pos_y][pos_x - 1] = Funcoes.matriz[pos_y][pos_x - 1], Funcoes.matriz[pos_y][pos_x]
                            sequencia = verificarSequencias(Funcoes.matriz)
                            if not sequencia:
                                Funcoes.matriz[pos_y][pos_x], Funcoes.matriz[pos_y][pos_x - 1] = Funcoes.matriz[pos_y][pos_x - 1], Funcoes.matriz[pos_y][pos_x]
                            else:
                                Funcoes.qtdJogadas -= 1
                            if Funcoes.dicaTela:
                                Funcoes.dicaTela = False
                                Funcoes.pontuacao -= 250

                if gameOver:
                    if prima:
                        if primeiraLetra < 26:
                            primeiraLetra += 1
                        else:
                            primeiraLetra = 0
                    if segunda:
                        if segundaLetra < 26:
                            segundaLetra += 1
                        else:
                            segundaLetra = 0
                    if terca:
                        if terceiraLetra < 26:
                            terceiraLetra += 1
                        else:
                            terceiraLetra = 0
                    if perguntaReset:
                        segundaLetra = 13
                            
            if event.key == K_a or event.key == K_LEFT: # Tecla A e Seta Left usadas para mover a seleção
                if Funcoes.qtdJogadas > 0:
                    if ySelecao > 225: # Condicional para evitar que o retângulo de seleção saia da matriz
                        ySelecao -= 60
                        xcor = ycor = zcor = 255
                        if enter:
                            pos_x, pos_y, enter = posQuadrado(ySelecao, xSelecao, enter)
                            Funcoes.matriz[pos_y][pos_x], Funcoes.matriz[pos_y + 1][pos_x] = Funcoes.matriz[pos_y + 1][pos_x], Funcoes.matriz[pos_y][pos_x]
                            sequencia = verificarSequencias(Funcoes.matriz)
                            if not sequencia:
                                Funcoes.matriz[pos_y][pos_x], Funcoes.matriz[pos_y + 1][pos_x] = Funcoes.matriz[pos_y + 1][pos_x], Funcoes.matriz[pos_y][pos_x]
                            else:
                                Funcoes.qtdJogadas -= 1
                            if Funcoes.dicaTela:
                                Funcoes.dicaTela = False
                                Funcoes.pontuacao -= 250

            if event.key == K_d or event.key == K_RIGHT: # Tecla D e Seta Right usadas para mover a seleção
                if Funcoes.qtdJogadas > 0:
                    if ySelecao < 525: # Condicional para evitar que o retângulo de seleção saia da matriz
                        ySelecao += 60
                        xcor = ycor = zcor = 255
                        if enter:
                            pos_x, pos_y, enter = posQuadrado(ySelecao, xSelecao, enter)
                            Funcoes.matriz[pos_y][pos_x], Funcoes.matriz[pos_y - 1][pos_x] = Funcoes.matriz[pos_y - 1][pos_x], Funcoes.matriz[pos_y][pos_x]
                            sequencia = verificarSequencias(Funcoes.matriz)
                            if not sequencia:
                                Funcoes.matriz[pos_y][pos_x], Funcoes.matriz[pos_y - 1][pos_x] = Funcoes.matriz[pos_y - 1][pos_x], Funcoes.matriz[pos_y][pos_x]
                            else:
                                Funcoes.qtdJogadas -= 1
                            if Funcoes.dicaTela:
                                Funcoes.dicaTela = False
                                Funcoes.pontuacao -= 250

            if event.key == K_h:
                if Funcoes.pontuacao >= 250:
                    Funcoes.dicaTela = True
                a, b, dicaDirecao = Funcoes.dicas(Funcoes.matriz)

            if event.key == K_KP_ENTER or event.key == K_RETURN: # Verifica se o jogador apertou Enter ou Return
                enter = True 
                ycor = zcor = 0 # Mudamos a cor do retângulo para indicar que foi selecionado
        
                if gameOver: # Caso o jogador tenha apertado Enter no gameover
                    if perguntaReset: # Se estiver na pergunta de reinício
                        if abc[segundaLetra] == "S" or abc[segundaLetra] == "N":
                            reset = True
                            contadorGame = 0
                            perguntaReset = False
                    else:
                        if prima: # Caso o jogador aperte enter, passamos para a próxima letra
                            prima = False
                            segunda = True
                        elif segunda:
                            segunda = False
                            terca = True
                        else:
                            terca = False
                            nomeJogador = abc[primeiraLetra] + abc[segundaLetra] + abc[terceiraLetra] # Juntamos as letras escolhidas pelo jogador
                            primeiraLetra = segundaLetra = terceiraLetra = 26 # Voltamos as letras para seu valor original
                            Funcoes.pontuacoes[nomeJogador] = Funcoes.pontuacao  # Armazenamos no dicionário de pontuações
                            Funcoes.pontuacoes = dict(sorted(Funcoes.pontuacoes.items(), key=lambda item: int(item[1]), reverse=True)) # Organizamos o dicionário em ordem decrescente, para isso os valores são transformados em inteiros
                            for chave, valor in Funcoes.pontuacoes.items(): # os valores são transformados em string para evitar problemas no momento de mostrar na tela na página de pontuação
                                Funcoes.pontuacoes[chave] = str(valor)
                            perguntaReset = True # Após o jogador inserir seu nome, inicia a pergunta de reinício

            if event.key == K_SPACE: # Usamos a tecla espaço para voltar ao menu
                primeiraRodada = True
                botaoMenu()
                
    pygame.display.flip() # função para atualizar a cada interação do loop principal