import os
import time
import msvcrt
import random
LINHA = 17
COLUNA = 17
tela = [['▫' for i in range(COLUNA)] for i in range(LINHA)]
VERMELHO = '\033[31m'
VERDE = '\033[32m'
AMARELO = '\033[33m'
AZUL = '\033[34m'
ROXO = '\033[35m'
CIANO = '\033[36m'
RESET = '\033[0m'
DIRECAO = {
    "cima": [0, -1],
    "esquerda": [-1, 0],
    "baixo": [0, 1],
    "direita": [1, 0]
}
PROJETIL = {
    "cima":f"{AMARELO}↑{RESET}",
    "esquerda":f"{AMARELO}←{RESET}",
    "baixo":f"{AMARELO}↓{RESET}",
    "direita":f"{AMARELO}→{RESET}",
    "rcima":f"{ROXO}↑{RESET}",
    "resquerda":f"{ROXO}←{RESET}",
    "rbaixo":f"{ROXO}↓{RESET}",
    "rdireita":f"{ROXO}→{RESET}"
}
PERSONAGEM = f"{CIANO}☻{RESET}"
Pontuacao = 0
vida = 2
buffDano = False
buffCongelamento = False
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
    if foraDoLimite(coordenada):
        return ""
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
def foraDoLimite(coordenada):
    x, y = coordenada
    return ((x > (COLUNA - 1)) or (y > (LINHA - 1)) or (x < 0) or (y < 0))
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
def geraBuff(coordenada):
    if random.random() > 0.1: return
    escolha = random.randint(1, 3)
    buff = '▫'
    if escolha == 1:
        buff = f'{VERDE}♥{RESET}'
    elif escolha == 2:
        buff = f'{ROXO}⚔{RESET}'
    elif escolha == 3:
        buff = f'{AZUL}❄{RESET}'
    inserirNaTela(buff, coordenada)
def escolherProjetil(direcao):
    if buffDano:
        return PROJETIL["r" + direcao]
    return PROJETIL[direcao]
def mover(posicao, direcao):
    Nposicao = somaCoord(posicao, DIRECAO[direcao])
    proximoCaractere = procurarNaTela(Nposicao)
    
    if proximoCaractere == "": 
        return posicao
    if VERMELHO in proximoCaractere:
        removerDaTela(posicao)
        return [0, 0]
    if VERDE in proximoCaractere:
        global vida
        vida +=1
    elif ROXO in proximoCaractere:
        global buffDano
        buffDano = True
    elif AZUL in proximoCaractere:
        global buffCongelamento
        buffCongelamento = True
    removerDaTela(posicao)
    inserirNaTela(PERSONAGEM, Nposicao)
    return  Nposicao
def moverProjetil(posicaoProj, direcao):
    projetil = escolherProjetil(direcao)
    NposicaoProj = somaCoord(posicaoProj, DIRECAO[direcao])
    proximoCaractere = procurarNaTela(NposicaoProj)
    
    while (VERDE in proximoCaractere) or (ROXO in proximoCaractere) or (AZUL in proximoCaractere):
        NposicaoProj = somaCoord(NposicaoProj, DIRECAO[direcao])
        proximoCaractere = procurarNaTela(NposicaoProj)
    if proximoCaractere == "": 
        removerDaTela(posicaoProj)
        return
    if VERMELHO in proximoCaractere:
        removerDaTela(posicaoProj)
        digito = int(procurarNaTela(NposicaoProj)[5])
        global Pontuacao
        if buffDano:
            removerDaTela(NposicaoProj)
            geraBuff(NposicaoProj)
            Pontuacao += 500 
            return
        elif digito == 1:
            removerDaTela(NposicaoProj)
            geraBuff(NposicaoProj)
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
    if buffCongelamento:
        return
    NposInimigo = somaCoord(posInimigo, mov)
    removerDaTela(posInimigo)
    inserirNaTela(inimigo, NposInimigo)
    return False
def numberShooter():
    global vida
    global buffDano
    global buffCongelamento
    global tela
    global Pontuacao
    global debug 
    meio = int((LINHA - 1)/2)
    posicao = [meio, meio]
    inserirNaTela(PERSONAGEM, posicao)
    contador1 = 0
    contador2 = 0
    contadorBuff1 = 0
    contadorBuff2 = 0
    onda = 0
    tempOnda = 170
    tempMovInimigo = 10
    temp = 0
    minInimig = 1
    maxInimig = 3
    Perdeu = True
    while True:
        Perdeu = True
        if msvcrt.kbhit():
            tecla = msvcrt.getch()
            if tecla == b'w': 
                posicao = mover(posicao, "cima")
            elif tecla== b'a': 
                posicao = mover(posicao, "esquerda")
            elif tecla == b's': 
                posicao = mover(posicao, "baixo")
            elif tecla == b'd': 
                posicao = mover(posicao, "direita")
            elif tecla == b'\xe0':
                tecla2 = msvcrt.getch()
                if tecla2 == b'H':
                    moverProjetil(posicao, "cima")
                elif tecla2 == b'K':
                    moverProjetil(posicao, "esquerda")
                elif tecla2 == b'P':
                    moverProjetil(posicao, "baixo")
                elif tecla2 == b'M':
                    moverProjetil(posicao, "direita")
        if contador1 % tempOnda == 0:
            onda += 1
            if (onda % 10) == 0:
                maxInimig += 2
                tempOnda -= int(0.1*tempOnda)
            if (onda % 5) == 0:
                tempMovInimigo -= int(0.15*tempMovInimigo)
                minInimig += 1
            geraInimigos(minInimig, maxInimig)
            contador1 = 0          
        for i in range(LINHA):
            for j in range(COLUNA):
                caractere = tela[i][j] 
                coordenadaAtual = [j, i]
                if  caractere == PERSONAGEM:
                    Perdeu = False
                if (caractere == PROJETIL["cima"]) or (caractere == PROJETIL ["rcima"]):
                    moverProjetil(coordenadaAtual, "cima")
                elif (caractere == PROJETIL["esquerda"]) or (caractere == PROJETIL ["resquerda"]):
                    moverProjetil(coordenadaAtual, "esquerda")
                if (contador2 % tempMovInimigo == 0) and (VERMELHO in caractere):
                    mov = melhorMov(posicao, coordenadaAtual)
                    if (mov == DIRECAO["cima"]) or (mov == DIRECAO["esquerda"]):
                        moverInimigo(mov, coordenadaAtual, caractere)
                        contador2 = 0
        for i in reversed(range(LINHA)):
            for j in reversed(range(COLUNA)):
                caractere = tela[i][j]
                coordenadaAtual = [j, i]
                if (caractere == PROJETIL["baixo"]) or (caractere == PROJETIL ["rbaixo"]):
                    moverProjetil(coordenadaAtual, "baixo")
                elif (caractere == PROJETIL["direita"]) or (caractere == PROJETIL ["rdireita"]):
                    moverProjetil(coordenadaAtual, "direita")
                if (contador2 % tempMovInimigo == 0) and (VERMELHO in caractere):
                    mov = melhorMov(posicao, coordenadaAtual)
                    if (mov == DIRECAO["baixo"]) or (mov == DIRECAO["direita"]):
                        moverInimigo(mov, coordenadaAtual, caractere)
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
        if buffDano:
            contadorBuff1 +=1
        if (contadorBuff1 % 100) == 0:
            buffDano = False
            contadorBuff1 = 0
        if buffCongelamento:
            contadorBuff2 +=1
        if (contadorBuff2 % 75) == 0:
            buffCongelamento = False
            contadorBuff2 = 0
        debug = f"{CIANO}\nUse WASD para se mover\nUse as setas (←↑↓→) para atirar\nOnda atual: {onda}\nProxima onda: {tempOnda}/{contador1}\nPontuação: {Pontuacao}\nVidas extras: {RESET}{VERDE}{('❤ ' * vida)}{RESET}"
        contador1 += 1
        contador2 += 1
        atualizarTela()
        time.sleep(0.05)
    print(f'{VERMELHO}FIM DE JOGO{RESET}')
    time.sleep(1)
    inpt = input("Digite r para recomeçar: ")
    if inpt.lower() == 'r':
        vida = 2
        buffDano = False
        buffCongelamento = False
        Pontuacao = 0
        limparTela()
        numberShooter()
numberShooter()