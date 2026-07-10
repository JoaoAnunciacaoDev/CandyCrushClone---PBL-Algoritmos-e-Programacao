import sys
import os


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame
from pygame.locals import (
    QUIT,
    KEYDOWN,
    K_ESCAPE,
    K_w,
    K_UP,
    K_s,
    K_DOWN,
    K_a,
    K_LEFT,
    K_d,
    K_RIGHT,
    K_h,
    K_KP_ENTER,
    K_RETURN,
    K_SPACE,
)
import funcoes
from funcoes import (
    abc,
    variaveisPadrao,
    inicioJogo,
    verificarSequencias,
    salvar_pontuacao,
    printMatriz,
    posQuadrado,
    guardarSequencias,
    subirPreto,
    preencherPreto,
    botaoMenu,
    clock,
    tela,
    preto,
    cores,
    tamanhoMatriz,
    font,
    font2,
    font3,
    Fundo,
)
import animation
from paths import get_asset_path


def run_game():
    botaoMenu()

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
    a = b = 0
    dicaDirecao = False

    while True:
        clock.tick(tempo)
        tela.fill(preto)

        if primeiraRodada:
            funcoes.matriz, funcoes.pontuacao, funcoes.qtdJogadas, funcoes.dicaTela = inicioJogo(tamanhoMatriz, cores)
            primeiraRodada = False

        if funcoes.qtdJogadas == 0:
            if verificarSequencias(funcoes.matriz):
                gameOver = False
            else:
                pygame.time.wait(80)
                gameOver = True

        if contadorGame == 49:
            if começaTocar:
                pygame.mixer.music.load(get_asset_path("audio", "GameOverSong.mp3"))
                pygame.mixer.music.play(1)
                pygame.mixer.music.set_volume(0.5)
                começaTocar = False

        if gameOver:
            tempo = 10

            if contadorGame == 0:
                pygame.mixer.music.stop()

            if contadorGame < 49:
                tela.blit(animation.listaGameOver[contadorGame], (200, 50))
                contadorGame += 1

                if contadorGame == 20:
                    pygame.mixer.music.load(get_asset_path("audio", "broken.mp3"))
                    pygame.mixer.music.play(1)
                    pygame.mixer.music.set_volume(0.8)

            elif contadorGame == 49 and not perguntaReset:
                textoGameOver = font2.render("GameOver", True, (255, 255, 255))
                textoInfoPontuacao = font.render(f"Sua pontuacao foi de {funcoes.pontuacao}", True, (255, 255, 255))
                textoMensagem = font.render("(Isso te enche de determinacao.)", True, (255, 255, 255))

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

            if perguntaReset:
                salvar_pontuacao(funcoes.pontuacao)

                textoInfoPontuacao = font.render("Deseja reiniciar o jogo?", True, (255, 255, 255))
                letra2 = font.render(abc[segundaLetra], True, (255, 255, 255))

                tela.blit(animation.listaGameOver[48], (200, 50))
                tela.blit(textoInfoPontuacao, (165, 500))
                tela.blit(letra2, (400, 600))

            if reset:
                if abc[segundaLetra] == "S":
                    if contadorGame < 73:
                        tela.blit(animation.listaRefused[contadorGame], (200, 50))
                        contadorGame += 1
                        if contadorGame == 28:
                            pygame.mixer.music.load(get_asset_path("audio", "somQuebra.mp3"))
                            pygame.mixer.music.play(1)
                            pygame.mixer.music.set_volume(0.8)
                        if contadorGame == 73:
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

                if abc[segundaLetra] == "N":
                    if contadorGame < 29:
                        tela.blit(animation.listaExplode[contadorGame], (178, 165))
                        if contadorGame == 19:
                            pygame.mixer.music.load(get_asset_path("audio", "somQuebra.mp3"))
                            pygame.mixer.music.play(1)
                            pygame.mixer.music.set_volume(0.8)
                        contadorGame += 1
                    else:
                        tela.blit(Fundo, (0, 0))
                        pygame.display.update()
                        pygame.mixer.music.load(get_asset_path("audio", "Ah, isso foi intenso.mp3"))
                        pygame.mixer.music.play(1)
                        pygame.mixer.music.set_volume(0.8)
                        pygame.time.wait(2000)
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
                        botaoMenu()

        else:
            pygame.draw.rect(tela, (18, 18, 18), (220, 220, 360, 360), border_radius=10)
            pygame.draw.rect(tela, (xcor, ycor, zcor), (ySelecao, xSelecao, 50, 50), 2)

            if funcoes.dicaTela:
                funcoes.desenhoDica(a, b, dicaDirecao)

            if contadorGame < 12:
                tela.blit(animation.listaPulso[contadorGame], (325, 10))
                contadorGame += 1
            else:
                contadorGame = 0

            textoPontuacao = font.render(f"Pontuacao: {funcoes.pontuacao}", True, (255, 255, 255))
            textoJogadas = font.render(f"Jogadas: {funcoes.qtdJogadas}", True, (255, 255, 255))
            textoInstrucao = font3.render("W/A/S/D ou SETAS para mover", True, (255, 255, 255))
            textoInstrucao2 = font3.render("ENTER para selecionar", True, (255, 255, 255))
            textoInstrucao3 = font3.render("H para pedir dica (Custo: 250p)", True, (255, 255, 255))
            textoInstrucao4 = font3.render("ESPACO para voltar ao menu", True, (255, 255, 255))
            textoInstrucao5 = font3.render("ESC para fechar o jogo", True, (255, 255, 255))

            tela.blit(textoPontuacao, (10, 10))
            tela.blit(textoJogadas, (560, 10))
            tela.blit(textoInstrucao, (200, 600))
            tela.blit(textoInstrucao2, (250, 640))
            tela.blit(textoInstrucao3, (170, 680))
            tela.blit(textoInstrucao4, (215, 720))
            tela.blit(textoInstrucao5, (235, 760))

            printMatriz(x, y)

            funcoes.pontuacao = guardarSequencias(funcoes.pontuacao)

            subirPreto()
            preencherPreto()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_w or event.key == K_UP:
                    if funcoes.qtdJogadas > 0:
                        if xSelecao > 225:
                            xSelecao -= 60
                            xcor = ycor = zcor = 255
                            if enter:
                                pos_x, pos_y, enter = posQuadrado(ySelecao, xSelecao, enter)
                                funcoes.matriz[pos_y][pos_x], funcoes.matriz[pos_y][pos_x + 1] = (
                                    funcoes.matriz[pos_y][pos_x + 1],
                                    funcoes.matriz[pos_y][pos_x],
                                )
                                sequencia = verificarSequencias(funcoes.matriz)
                                if not sequencia:
                                    funcoes.matriz[pos_y][pos_x], funcoes.matriz[pos_y][pos_x + 1] = (
                                        funcoes.matriz[pos_y][pos_x + 1],
                                        funcoes.matriz[pos_y][pos_x],
                                    )

                                else:
                                    funcoes.qtdJogadas -= 1
                                if funcoes.dicaTela:
                                    funcoes.dicaTela = False
                                    funcoes.pontuacao -= 250

                    if gameOver:
                        if prima:
                            if primeiraLetra > 0:
                                primeiraLetra -= 1
                            else:
                                primeiraLetra = 26
                        if segunda:
                            if segundaLetra > 0:
                                segundaLetra -= 1
                            else:
                                segundaLetra = 26
                        if terca:
                            if terceiraLetra > 0:
                                terceiraLetra -= 1
                            else:
                                terceiraLetra = 26
                        if perguntaReset:
                            segundaLetra = 18

                if event.key == K_s or event.key == K_DOWN:
                    if funcoes.qtdJogadas > 0:
                        if xSelecao < 525:
                            xSelecao += 60
                            xcor = ycor = zcor = 255
                            if enter:
                                pos_x, pos_y, enter = posQuadrado(ySelecao, xSelecao, enter)
                                funcoes.matriz[pos_y][pos_x], funcoes.matriz[pos_y][pos_x - 1] = (
                                    funcoes.matriz[pos_y][pos_x - 1],
                                    funcoes.matriz[pos_y][pos_x],
                                )
                                sequencia = verificarSequencias(funcoes.matriz)
                                if not sequencia:
                                    funcoes.matriz[pos_y][pos_x], funcoes.matriz[pos_y][pos_x - 1] = (
                                        funcoes.matriz[pos_y][pos_x - 1],
                                        funcoes.matriz[pos_y][pos_x],
                                    )
                                else:
                                    funcoes.qtdJogadas -= 1
                                if funcoes.dicaTela:
                                    funcoes.dicaTela = False
                                    funcoes.pontuacao -= 250

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

                if event.key == K_a or event.key == K_LEFT:
                    if funcoes.qtdJogadas > 0:
                        if ySelecao > 225:
                            ySelecao -= 60
                            xcor = ycor = zcor = 255
                            if enter:
                                pos_x, pos_y, enter = posQuadrado(ySelecao, xSelecao, enter)
                                funcoes.matriz[pos_y][pos_x], funcoes.matriz[pos_y + 1][pos_x] = (
                                    funcoes.matriz[pos_y + 1][pos_x],
                                    funcoes.matriz[pos_y][pos_x],
                                )
                                sequencia = verificarSequencias(funcoes.matriz)
                                if not sequencia:
                                    funcoes.matriz[pos_y][pos_x], funcoes.matriz[pos_y + 1][pos_x] = (
                                        funcoes.matriz[pos_y + 1][pos_x],
                                        funcoes.matriz[pos_y][pos_x],
                                    )
                                else:
                                    funcoes.qtdJogadas -= 1
                                if funcoes.dicaTela:
                                    funcoes.dicaTela = False
                                    funcoes.pontuacao -= 250

                if event.key == K_d or event.key == K_RIGHT:
                    if funcoes.qtdJogadas > 0:
                        if ySelecao < 525:
                            ySelecao += 60
                            xcor = ycor = zcor = 255
                            if enter:
                                pos_x, pos_y, enter = posQuadrado(ySelecao, xSelecao, enter)
                                funcoes.matriz[pos_y][pos_x], funcoes.matriz[pos_y - 1][pos_x] = (
                                    funcoes.matriz[pos_y - 1][pos_x],
                                    funcoes.matriz[pos_y][pos_x],
                                )
                                sequencia = verificarSequencias(funcoes.matriz)
                                if not sequencia:
                                    funcoes.matriz[pos_y][pos_x], funcoes.matriz[pos_y - 1][pos_x] = (
                                        funcoes.matriz[pos_y - 1][pos_x],
                                        funcoes.matriz[pos_y][pos_x],
                                    )
                                else:
                                    funcoes.qtdJogadas -= 1
                                if funcoes.dicaTela:
                                    funcoes.dicaTela = False
                                    funcoes.pontuacao -= 250

                if event.key == K_h:
                    if funcoes.pontuacao >= 250:
                        funcoes.dicaTela = True
                    a, b, dicaDirecao = funcoes.dicas(funcoes.matriz)

                if event.key == K_KP_ENTER or event.key == K_RETURN:
                    enter = True
                    ycor = zcor = 0

                    if gameOver:
                        if perguntaReset:
                            if abc[segundaLetra] == "S" or abc[segundaLetra] == "N":
                                reset = True
                                contadorGame = 0
                                perguntaReset = False
                        else:
                            if prima and primeiraLetra != 26:
                                prima = False
                                segunda = True
                            elif segunda and segundaLetra != 26:
                                segunda = False
                                terca = True
                            elif terca and terceiraLetra != 26:
                                terca = False
                                nomeJogador = abc[primeiraLetra] + abc[segundaLetra] + abc[terceiraLetra]
                                primeiraLetra = segundaLetra = terceiraLetra = 26
                                funcoes.pontuacoes[nomeJogador] = funcoes.pontuacao
                                funcoes.pontuacoes = dict(
                                    sorted(funcoes.pontuacoes.items(), key=lambda item: int(item[1]), reverse=True)
                                )
                                for chave, valor in funcoes.pontuacoes.items():
                                    funcoes.pontuacoes[chave] = str(valor)
                                perguntaReset = True

                if event.key == K_SPACE:
                    primeiraRodada = True
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
                    botaoMenu()

        pygame.display.flip()


if __name__ == "__main__":
    run_game()
