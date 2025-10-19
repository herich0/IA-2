import random
from config import (
MOVIMENTOS_POSSIVEIS, MAX_PASSOS_CROMOSSOMO, TAMANHO_MATRIZ,
PONTOS_INICIAIS_EQUIPE, PONTOS_TESOUROS, OBSTACULOS,
FITNESS_COLETA_PESO, FITNESS_DISTANCIA_PESO, FITNESS_COLISAO_PENALIDADE,
FITNESS_REDUNDANCIA_PENALIDADE
)


class Cromossomo:
    def __init__(self, movimentos=None):
        # movimentos é uma lista de 4 listas (uma por agente)
        if movimentos is None:
            self.movimentos = [self._gerar_movimentos_aleatorios() for _ in range(4)]
        else:
            self.movimentos = movimentos
        self.fitness = 0.0

    def _gerar_movimentos_aleatorios(self):
        return [random.choice(MOVIMENTOS_POSSIVEIS) for _ in range(MAX_PASSOS_CROMOSSOMO)]

    def __repr__(self):
        # mostra os primeiros genes de cada agente para debug
        genes_preview = [''.join(m[:20]) + ('...' if len(m) > 20 else '') for m in self.movimentos]
        return f"Cromossomo(Fitness: {self.fitness:.2f}, Genes: {genes_preview})"


def calcular_fitness(cromossomo):
    """
    Simula os 4 agentes em paralelo no tempo (passo a passo).
    Recompensa: número total de tesouros coletados pela equipe.
    Penalidades: colisões com obstáculos/bordas, redundância (dois agentes pegando o mesmo tesouro), passos inválidos.
    """
    posicoes = list(PONTOS_INICIAIS_EQUIPE)
    tesouros_restantes = set(PONTOS_TESOUROS)
    # para marcar qual agente coletou qual tesouro (para penalizar redundância se necessário)
    coletados_por_agente = [set() for _ in range(4)]

    colisoes = 0
    redundancia = 0
    passos_validos = 0

    delta = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}

    for passo in range(MAX_PASSOS_CROMOSSOMO):
        # cada agente realiza seu movimento no mesmo passo de tempo
        novas_posicoes = list(posicoes)
        for i in range(4):
            movimento = cromossomo.movimentos[i][passo]
            dr, dc = delta[movimento]
            nova = (posicoes[i][0] + dr, posicoes[i][1] + dc)

            # verifica limites e obstáculos
            if not (0 <= nova[0] < TAMANHO_MATRIZ and 0 <= nova[1] < TAMANHO_MATRIZ) or nova in OBSTACULOS:
                colisoes += 1
                # agente não se move neste passo (fica na posição anterior)
                continue

            novas_posicoes[i] = nova
            passos_validos += 1

        # atualiza as posições de todos os agentes (simultâneo)
        posicoes = novas_posicoes

        # checa coleta de tesouros (se dois chegam ao mesmo tesouro no mesmo passo, premia um e penaliza redundância)
        pos_para_agentes = {}
        for i, p in enumerate(posicoes):
            pos_para_agentes.setdefault(p, []).append(i)

        for pos, agentes_na_pos in pos_para_agentes.items():
            if pos in tesouros_restantes:
                # se vários agentes chegam ao mesmo tesouro, apenas um coleta (escolhemos o primeiro da lista)
                coletor = agentes_na_pos[0]
                tesouros_restantes.remove(pos)
                coletados_por_agente[coletor].add(pos)
                # penalidade de redundância para os demais agentes que chegaram ao mesmo ponto
                if len(agentes_na_pos) > 1:
                    redundancia += (len(agentes_na_pos) - 1)

    tesouros_coletados = sum(len(s) for s in coletados_por_agente)

    # distância final mínima dos agentes aos tesouros restantes (melhor aproximação)
    if tesouros_restantes:
        distancias_min = []
        for pos in posicoes:
            d = min(abs(tx - pos[0]) + abs(ty - pos[1]) for tx, ty in tesouros_restantes)
            distancias_min.append(d)
        distancia_media_min = sum(distancias_min) / len(distancias_min)
    else:
        distancia_media_min = 0.0

    # fitness composto
    fitness = (tesouros_coletados * FITNESS_COLETA_PESO) \
              + (FITNESS_DISTANCIA_PESO / (distancia_media_min + 1)) \
              - (colisoes * FITNESS_COLISAO_PENALIDADE) \
              - (redundancia * FITNESS_REDUNDANCIA_PENALIDADE) \
              - ( (MAX_PASSOS_CROMOSSOMO - passos_validos) * 0.1 )

    cromossomo.fitness = fitness
    return fitness