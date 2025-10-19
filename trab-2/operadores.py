import random
from config import (TAMANHO_POPULACAO, TAXA_CRUZAMENTO, TAXA_MUTACAO, MAX_PASSOS_CROMOSSOMO)
from cromossomo import Cromossomo


def inicializar_populacao():
    return [Cromossomo() for _ in range(TAMANHO_POPULACAO)]


def selecao_torneio(populacao, k=5):
    torneio = random.sample(populacao, k)
    return max(torneio, key=lambda c: c.fitness)


def cruzamento_ponto_unico(pai1, pai2):
    # Cruzamento independente por agente (cada agente tem seu próprio ponto)
    filhos_movs_1 = []
    filhos_movs_2 = []
    for agente in range(4):
        seq1 = pai1.movimentos[agente]
        seq2 = pai2.movimentos[agente]
        if random.random() < TAXA_CRUZAMENTO:
            ponto = random.randint(1, MAX_PASSOS_CROMOSSOMO - 1)
            f1 = seq1[:ponto] + seq2[ponto:]
            f2 = seq2[:ponto] + seq1[ponto:]
        else:
            f1 = seq1[:]
            f2 = seq2[:]
        filhos_movs_1.append(f1)
        filhos_movs_2.append(f2)

    filho1 = Cromossomo(movimentos=filhos_movs_1)
    filho2 = Cromossomo(movimentos=filhos_movs_2)
    return filho1, filho2


def mutacao(cromossomo):
    for agente in range(4):
        for i in range(len(cromossomo.movimentos[agente])):
            if random.random() < TAXA_MUTACAO:
                cromossomo.movimentos[agente][i] = random.choice(['R', 'L', 'U', 'D'])
    return cromossomo