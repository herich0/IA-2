# PARÂMETROS DO AG
TAMANHO_POPULACAO = 100
MAX_GERACOES = 50
TAXA_CRUZAMENTO = 0.8
TAXA_MUTACAO = 0.05
MAX_PASSOS_CROMOSSOMO = 75  # Tamanho do cromossomo
MOVIMENTOS_POSSIVEIS = ['R', 'L', 'U', 'D']

# Tamanho do mapa
TAMANHO_MATRIZ = 40

# Tesouros espalhados em posições variadas
PONTOS_TESOUROS = [
    (3, 5), (8, 25), (12, 15), (18, 30),
    (22, 3), (27, 27), (31, 12), (36, 35),
    (5, 18), (25, 38)
]

# Pontos iniciais dos 4 agentes do mesmo cromossomo
PONTOS_INICIAIS_EQUIPE = [(0, 0), (0, 39), (39, 0), (39, 39)]

# Obstáculos tipo labirinto mais complexos
OBSTACULOS = []

# Linhas horizontais de obstáculos
for i in range(5, 35, 4):
    for j in range(5, 35):
        if j % 3 != 0:  # deixa espaços para passagem
            OBSTACULOS.append((i, j))

# Linhas verticais de obstáculos
for j in range(5, 35, 5):
    for i in range(5, 35):
        if i % 4 != 0:
            OBSTACULOS.append((i, j))

# Alguns obstáculos soltos aleatórios para quebrar padrão
OBSTACULOS += [(10, 10), (15, 22), (20, 18), (30, 25), (28, 7), (5, 32)]

# PESOS DA FUNÇÃO DE FITNESS
FITNESS_COLETA_PESO = 1000.0   # Encontrar o tesouro
FITNESS_DISTANCIA_PESO = 100.0 # Proximidade final
FITNESS_COLISAO_PENALIDADE = 200.0 # Bater no obstáculo/limite
FITNESS_REDUNDANCIA_PENALIDADE = 50.0

# Semente (opcional) para reprodutibilidade
SEED = None
