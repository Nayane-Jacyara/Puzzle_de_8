import random

# Gera um tabuleiro aleatório válido para o quebra-cabeça de 8 peças.
def gerar_tabuleiro_aleatorio():
    numeros = list(range(9))  # Lista de números de 0 a 8
    random.shuffle(numeros)  # Embaralha os números
    tabuleiro = [[numeros.pop() for _ in range(3)] for _ in range(3)]  # Cria o tabuleiro 3x3

    return tabuleiro

# Gerar tabuleiro inicial aleatório
tabuleiro_inicial = gerar_tabuleiro_aleatorio()

# Converter o tabuleiro em string
tabuleiro_str = str(tabuleiro_inicial)

obj_final = str([
                [1,2,3],
                [4,5,6],
                [7,8,0]
            ])


# Checa possíveis movimentos (os nós) da árvore
def move(tab_original):
    movimentos = []
    tab = eval(tab_original)
    i = 0
    j = 0
    while 0 not in tab[i]: 
        i += 1
    j = tab[i].index(0)

    # Defina os movimentos possíveis para cima, baixo, esquerda e direita
    movimentos_possiveis = []
    if i < 2:
        movimentos_possiveis.append((i + 1, j))  # Movimento para baixo
    if i > 0:        movimentos_possiveis.append((i - 1, j))  # Movimento para cima
    if j < 2:
        movimentos_possiveis.append((i, j + 1))  # Movimento para direita
    if j > 0:
        movimentos_possiveis.append((i, j - 1))  # Movimento para esquerda

    # Embaralhe os movimentos possíveis para criar uma ordem aleatória
    random.shuffle(movimentos_possiveis)

    # Aplique os movimentos possíveis
    for move_i, move_j in movimentos_possiveis:
        tab_copia = [linha[:] for linha in tab]  # Cria uma cópia do tabuleiro
        tab_copia[i][j], tab_copia[move_i][move_j] = tab_copia[move_i][move_j], tab_copia[i][j]
        movimentos.append(str(tab_copia))

    return movimentos

# Implementa a heurística de checar quantas peças estão fora do lugar
def h_pecas_fora_do_lugar(tabuleiro): 
    pecas_fora_do_lugar = 0
    comparador = 1
    tab = eval(tabuleiro)
    for i in range(0, 3):
        for j in range(0, 3):
            if tab[i][j] != comparador:
                pecas_fora_do_lugar += 1
            comparador += 1
    return pecas_fora_do_lugar

# Usa busca gulosa para resolver o quebra-cabeça
def busca_gulosa(start, end):
    explorado = []
    banco = [[h_pecas_fora_do_lugar(start), start]]
    while banco:
        i = 0
        for j in range(1, len(banco)):
            if banco[i][0] > banco[j][0]:
                i = j
        caminho = banco[i]
        banco = banco[:i] + banco[i+1:]
        final = caminho[-1]
        if final in explorado: 
            continue
        for movimento in move(final):
            if movimento in explorado: 
                continue
            h = h_pecas_fora_do_lugar(movimento)  # Aqui usamos apenas a heurística como função de avaliação
            novo = [h, movimento]
            banco.append(novo)
        explorado.append(final)
        if final == end: 
            break
    return caminho


print("Tabuleiro Inicial Aleatório:")
print(tabuleiro_str)
print("Usando Busca Gulosa:")
for i in busca_gulosa(tabuleiro_str, obj_final):
    print(i, end="\n")
