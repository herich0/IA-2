import random
from config import (
FITNESS_DIVERSIDADE_AREA, MOVIMENTOS_POSSIVEIS, MAX_PASSOS_CROMOSSOMO, TAMANHO_MATRIZ,
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
    Bônus: diversidade de áreas visitadas (agentes cobrindo diferentes partes do mapa).
    """
    posicoes = list(PONTOS_INICIAIS_EQUIPE)
    tesouros_restantes = set(PONTOS_TESOUROS)
    coletados_por_agente = [set() for _ in range(4)]

    colisoes = 0
    redundancia = 0
    passos_validos = 0

    # Guarda trajetórias completas dos agentes
    trajetorias_agentes = [set([p]) for p in posicoes]

    delta = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}

    for passo in range(MAX_PASSOS_CROMOSSOMO):
        novas_posicoes = list(posicoes)
        for i in range(4):
            movimento = cromossomo.movimentos[i][passo]
            dr, dc = delta[movimento]
            nova = (posicoes[i][0] + dr, posicoes[i][1] + dc)

            # verifica limites e obstáculos
            if not (0 <= nova[0] < TAMANHO_MATRIZ and 0 <= nova[1] < TAMANHO_MATRIZ) or nova in OBSTACULOS:
                colisoes += 1
                continue  # agente não se move
            novas_posicoes[i] = nova
            trajetorias_agentes[i].add(nova)
            passos_validos += 1

        posicoes = novas_posicoes

        # checa coleta de tesouros
        pos_para_agentes = {}
        for i, p in enumerate(posicoes):
            pos_para_agentes.setdefault(p, []).append(i)

        for pos, agentes_na_pos in pos_para_agentes.items():
            if pos in tesouros_restantes:
                coletor = agentes_na_pos[0]
                tesouros_restantes.remove(pos)
                coletados_por_agente[coletor].add(pos)
                if len(agentes_na_pos) > 1:
                    redundancia += (len(agentes_na_pos) - 1)

    tesouros_coletados = sum(len(s) for s in coletados_por_agente)

    # distância final mínima dos agentes aos tesouros restantes
    if tesouros_restantes:
        distancias_min = []
        for pos in posicoes:
            d = min(abs(tx - pos[0]) + abs(ty - pos[1]) for tx, ty in tesouros_restantes)
            distancias_min.append(d)
        distancia_media_min = sum(distancias_min) / len(distancias_min)
    else:
        distancia_media_min = 0.0

    # ---- 🎯 BÔNUS DE DIVERSIDADE DE ÁREA VISITADA ----
    areas_visitadas = set()
    for traj in trajetorias_agentes:
        areas_visitadas.update(traj)
    diversidade_bonus = len(areas_visitadas) * (FITNESS_DIVERSIDADE_AREA / 100)
    # ---------------------------------------------------

    # fitness composto
    fitness = (tesouros_coletados * FITNESS_COLETA_PESO) \
              + (FITNESS_DISTANCIA_PESO / (distancia_media_min + 1)) \
              - (colisoes * FITNESS_COLISAO_PENALIDADE) \
              - (redundancia * FITNESS_REDUNDANCIA_PENALIDADE) \
              - ((MAX_PASSOS_CROMOSSOMO - passos_validos) * 0.1) \
              + diversidade_bonus  # aplica o bônus aqui

    cromossomo.fitness = fitness
    return fitness