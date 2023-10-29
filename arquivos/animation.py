import pygame

largura_nova = 200
altura_nova = 250

largura_nova2 = 250
altura_nova2 = 300

largura_nova3 = 600
altura_nova3 = 600

lista = []
lista2 = []
lista3 = []
listaGameOver = []
listaRefused = []
listaExplode = []
listaPulso = []

for i in range(1, 44):
    if i < 10:
        nome_arquivo = f'frame-0{i}.gif'
    else:
        nome_arquivo = f'frame-{i}.gif'
    imagem = pygame.image.load(nome_arquivo)
    lista.append(imagem)

for i in range(1, 9):
    nome_arquivo = f'frame{i}.gif'
    imagem = pygame.image.load(nome_arquivo)
    lista2.append(imagem)

for i in range(1, 50):
    nome_arquivo = f'frame0{i}.gif'
    imagem = pygame.image.load(nome_arquivo)
    lista3.append(imagem)

for i in range(1, 50):
    numero_frame = f"{i:03d}" 
    nome_arquivo = f"frame_{numero_frame}.gif"
    imagem = pygame.image.load(nome_arquivo)
    listaGameOver.append(imagem)

for i in range(56, 129):
    nome_arquivo = f'{i}.gif'
    imagem = pygame.image.load(nome_arquivo)
    listaRefused.append(imagem)

for i in range(13, 42):
    nome_arquivo = f'f{i}.gif'
    imagem = pygame.image.load(nome_arquivo)
    listaExplode.append(imagem)

for i in range(1, 13):
    nome_arquivo = f'c{i}.gif'
    imagem = pygame.image.load(nome_arquivo)
    listaPulso.append(imagem)

for i in range(43):
    lista[i] = pygame.transform.scale(lista[i], (largura_nova, altura_nova))

for i in range(8):
    lista2[i] = pygame.transform.scale(lista2[i], (largura_nova2, altura_nova2))

for i in range(49):
    lista3[i] = pygame.transform.scale(lista3[i], (largura_nova3, altura_nova3))

for i in range(49):
    listaGameOver[i] = pygame.transform.scale(listaGameOver[i], (400, 400))

for i in range(73):
    listaRefused[i] = pygame.transform.scale(listaRefused[i], (400, 400))

for i in range(29):
    listaExplode[i] = pygame.transform.scale(listaExplode[i], (450, 420))

for i in range(12):
    listaPulso[i] = pygame.transform.scale(listaPulso[i], (150, 120))