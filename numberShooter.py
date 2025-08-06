import os
import time
import msvcrt
import random
LINHA = 17
COLUNA = 17
tela = [['▫' for i in range(COLUNA)] for i in range(LINHA)]
DIRECAO = {
    "cima": [0, -1],
    "esquerda": [-1, 0],
    "baixo": [0, 1],
    "direita": [1, 0]
}
VERMELHO = '\033[31m'
VERDE = '\033[32m'
AMARELO = '\033[33m'
CIANO = '\033[36m'
RESET = '\033[0m'
PROJETIL = {
    "↑":f"{AMARELO}↑{RESET}",
    "←":f"{AMARELO}←{RESET}",
    "↓":f"{AMARELO}↓{RESET}",
    "→":f"{AMARELO}→{RESET}"
}
PERSONAGEM = f"{CIANO}☻{RESET}"
Pontuacao = 0
debug = ""
def inserirNaTela(caractere, coordenada):
    x, y = coordenada
    tela[y].pop(x)
    tela[y].insert(x, caractere)
def removerDaTela(coordenada):
    x, y = coordenada
    tela[y].pop(x)
    tela[y].insert(x, '▫')
def procurarNaTela(coordenada):
    x, y = coordenada
    return tela[y][x]
def limparTela():
    for i in range(LINHA):
        for j in range(COLUNA):
            removerDaTela([j, i])
def formatarTela():
    fTela = ""
    for i in range(LINHA):
        for j in range(COLUNA):
            fTela += f"{tela[i][j]} "
        fTela += "\n"
    return fTela
def atualizarTela():
    fTela = formatarTela()
    fTela += debug
    os.system('cls')
    print(fTela)
def calcularDistancia(coordenadas1, coordenadas2):
    x1, y1 = coordenadas1
    x2, y2 = coordenadas2
    return (abs(x2 - x1) + abs(y2 - y1))
def somaCoord(coordenadas1, coordenadas2):
    x = coordenadas1[0] + coordenadas2[0]
    y = coordenadas1[1] + coordenadas2[1]
    return [x, y]
def mover(posicao, vetor):
    Nposicao = somaCoord(posicao, vetor)
    x, y = Nposicao
    if (x > (COLUNA - 1)) or (y > (LINHA - 1)): return posicao
    if (x < 0) or (y < 0): return posicao
    if VERMELHO in tela[y][x]:
        removerDaTela(posicao)
        return [0, 0]       
    removerDaTela(posicao)
    inserirNaTela(PERSONAGEM, Nposicao)
    return  Nposicao
def geraInimigos(minimo, maximo):
    numInimigos = random.randint(minimo, maximo)
    for i in range(numInimigos):
        cbed = random.randint(1, 4)
        if cbed == 1:
            posInimigo = [random.randrange(0, COLUNA), 0]
        elif cbed == 2:
            posInimigo = [random.randrange(0, COLUNA), LINHA-1]
        elif cbed == 3:
            posInimigo = [0, random.randrange(0, LINHA)]
        elif cbed == 4:
            posInimigo = [COLUNA-1, random.randrange(0, LINHA)]
        inserirNaTela(f'{VERMELHO}{random.randint(1, 9)}{RESET}', posInimigo)
def moverProjetil(posicaoProj, vetor, projetil):
    NposicaoProj = somaCoord(posicaoProj, vetor)
    x, y = NposicaoProj
    if (x > (COLUNA - 1)) or (y > (LINHA - 1)): 
        removerDaTela(posicaoProj)
        return
    if (x < 0) or (y < 0): 
        removerDaTela(posicaoProj)
        return
    if VERMELHO in tela[y][x]:
        removerDaTela(posicaoProj)
        digito = int(procurarNaTela(NposicaoProj)[5])
        global Pontuacao
        if digito == 1:
            removerDaTela(NposicaoProj)
            Pontuacao += 500 
        else:
            digito = digito - 1
            Pontuacao += 100
            inserirNaTela(f'{VERMELHO}{digito}{RESET}', NposicaoProj)
        return
    if not (PERSONAGEM == procurarNaTela(posicaoProj)):
        removerDaTela(posicaoProj)
    inserirNaTela(projetil, NposicaoProj)
def melhorMov(coordenada1, coordenada2):
    distancia = calcularDistancia(coordenada1, coordenada2)
    if distancia > calcularDistancia(coordenada1, somaCoord(coordenada2, DIRECAO["cima"])):
        return DIRECAO["cima"]
    if distancia > calcularDistancia(coordenada1, somaCoord(coordenada2, DIRECAO["esquerda"])):
        return DIRECAO["esquerda"]
    if distancia > calcularDistancia(coordenada1, somaCoord(coordenada2, DIRECAO["baixo"])):
        return DIRECAO["baixo"]
    if distancia > calcularDistancia(coordenada1, somaCoord(coordenada2, DIRECAO["direita"])):
        return DIRECAO["direita"]
    return [0, 0]
def moverInimigo(mov, posInimigo, inimigo):
    NposInimigo = somaCoord(posInimigo, mov)
    removerDaTela(posInimigo)
    inserirNaTela(inimigo, NposInimigo)
    return False
def numberShooter(): 
    meio = int((LINHA - 1)/2)
    posicao = [meio, meio]
    inserirNaTela(PERSONAGEM, posicao)
    contador1 = 0
    contador2 = 0
    onda = 0
    tempOnda = 170
    tempMovInimigo = 10
    minInimig = 2
    maxInimig = 5
    Perdeu = True
    vida = 2
    global tela
    global Pontuacao
    global debug
    while True:
        Perdeu = True
        if msvcrt.kbhit():
            tecla = msvcrt.getch()
            if tecla == b'w': 
                posicao = mover(posicao, DIRECAO["cima"])
            elif tecla== b'a': 
                posicao = mover(posicao, DIRECAO["esquerda"])
            elif tecla == b's': 
                posicao = mover(posicao, DIRECAO["baixo"])
            elif tecla == b'd': 
                posicao = mover(posicao, DIRECAO["direita"])
            elif tecla == b'\xe0':
                tecla2 = msvcrt.getch()
                if tecla2 == b'H':
                    moverProjetil(posicao, DIRECAO["cima"], PROJETIL["↑"])
                elif tecla2 == b'K':
                    moverProjetil(posicao, DIRECAO["esquerda"], PROJETIL["←"])
                elif tecla2 == b'P':
                    moverProjetil(posicao, DIRECAO["baixo"], PROJETIL["↓"])
                elif tecla2 == b'M':
                    moverProjetil(posicao, DIRECAO["direita"], PROJETIL["→"])
        if contador1 % tempOnda == 0:
            onda += 1
            if (onda % 10) == 0:
                maxInimig +=2
                tempOnda -= int(0.15*tempOnda)
            if (onda % 5) == 0:
                tempMovInimigo -= int(0.2*tempMovInimigo)
                minInimig += 1
            geraInimigos(minInimig, maxInimig)
            contador1 = 0          
        for i in range(LINHA):
            for j in range(COLUNA):
                caractere = tela[i][j] 
                if  caractere == PERSONAGEM:
                    Perdeu = False
                if caractere == PROJETIL["↑"]:
                    moverProjetil([j, i], DIRECAO["cima"], PROJETIL["↑"])
                elif caractere == PROJETIL["←"]:
                    moverProjetil([j, i], DIRECAO["esquerda"], PROJETIL["←"])
                if (contador2 % tempMovInimigo == 0) and (VERMELHO in caractere):
                    mov = melhorMov(posicao, [j, i])
                    if (mov == DIRECAO["cima"]) or (mov == DIRECAO["esquerda"]):
                        moverInimigo(mov, [j, i], caractere)
                        contador2 = 0
        for i in reversed(range(LINHA)):
            for j in reversed(range(COLUNA)):
                caractere = tela[i][j]
                if caractere == PROJETIL["↓"]:
                    moverProjetil([j, i], DIRECAO["baixo"], PROJETIL["↓"])
                elif caractere == PROJETIL["→"]:
                    moverProjetil([j, i], DIRECAO["direita"], PROJETIL["→"])
                if (contador2 % tempMovInimigo == 0) and (VERMELHO in caractere):
                    mov = melhorMov(posicao, [j, i])
                    if (mov == DIRECAO["baixo"]) or (mov == DIRECAO["direita"]):
                        moverInimigo(mov, [j, i], caractere)
                        contador2 = 0
        if Perdeu:
            if vida == 0:
                atualizarTela()
                break
            else:
                vida -= 1
                limparTela()
                posicao = [meio, meio]
                inserirNaTela(PERSONAGEM, posicao)
                i = 0
                while i != 3:
                    os.system('cls')
                    time.sleep(0.15)
                    atualizarTela()
                    time.sleep(0.15)
                    i += 1
        debug = f"{CIANO}\nUse WASD para se mover\nUse as setas (←↑↓→) para atirar\nOnda atual: {onda}\nProxima onda: {tempOnda}/{contador1}\nPontuação: {Pontuacao}\nVidas extras: {RESET}{VERDE}{('❤ ' * vida)}{RESET}"
        contador1 += 1
        contador2 += 1
        atualizarTela()
        time.sleep(0.05)
    print(f'{VERMELHO}FIM DE JOGO{RESET}')
    time.sleep(1)
    inpt = input("Digite r para recomeçar: ")
    if inpt.lower() == 'r':
        Pontuacao = 0
        limparTela()
        numberShooter()
numberShooter()