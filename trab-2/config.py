# configuracao.py (nova versão ajustada)

# PARÂMETROS DO AG
TAMANHO_POPULACAO = 100
MAX_GERACOES = 50
TAXA_CRUZAMENTO = 0.8
TAXA_MUTACAO = 0.05
MAX_PASSOS_CROMOSSOMO = 60  # ligeiramente menor para compensar o mapa menor
MOVIMENTOS_POSSIVEIS = ['R', 'L', 'U', 'D']

# Tamanho do mapa
TAMANHO_MATRIZ = 25

# Tesouros espalhados (melhor distribuição)
PONTOS_TESOUROS = [
    (3, 4), (6, 18), (9, 9), (12, 20), (15, 5),
    (18, 12), (21, 7), (22, 19), (10, 3), (5, 14)
]

# Pontos iniciais dos 4 agentes — mais próximos do centro
PONTOS_INICIAIS_EQUIPE = [(10, 10), (10, 14), (14, 10), (14, 14)]

# Obstáculos com padrão de labirinto leve (muito mais espaçado)
OBSTACULOS = []

# Linhas horizontais a cada 6 blocos, com aberturas mais frequentes
for i in range(4, TAMANHO_MATRIZ, 6):
    for j in range(TAMANHO_MATRIZ):
        if j % 3 != 0:  # deixa 1/3 de aberturas
            OBSTACULOS.append((i, j))

# Linhas verticais a cada 6 blocos, com aberturas também
for j in range(4, TAMANHO_MATRIZ, 6):
    for i in range(TAMANHO_MATRIZ):
        if i % 3 != 0:
            OBSTACULOS.append((i, j))

# PESOS DA FUNÇÃO DE FITNESS
FITNESS_COLETA_PESO = 1000.0
FITNESS_DISTANCIA_PESO = 100.0
FITNESS_COLISAO_PENALIDADE = 100.0
FITNESS_REDUNDANCIA_PENALIDADE = 50.0

# Bônus opcional de diversidade (se quiser ativar)
FITNESS_DIVERSIDADE_AREA = 10.0

SEED = None
