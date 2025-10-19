import random
import copy
from config import (
    TAMANHO_POPULACAO,
    TAXA_MUTACAO,
    TAXA_CRUZAMENTO,
    MAX_GERACOES,
    TAMANHO_MATRIZ,
    PONTOS_TESOUROS,
    PONTOS_INICIAIS_EQUIPE,
    FITNESS_COLETA_PESO,
    FITNESS_DISTANCIA_PESO,
    FITNESS_COLISAO_PENALIDADE,
    FITNESS_REDUNDANCIA_PENALIDADE,
    SEED,
    OBSTACULOS,
)
from operadores import inicializar_populacao, selecao_torneio, cruzamento_ponto_unico, mutacao
from cromossomo import calcular_fitness
from analise_resultados import plotar_historico_fitness

# Semente opcional
if SEED is not None:
    random.seed(SEED)


def criar_mapa_printavel():
    from config import TAMANHO_MATRIZ
    mapa = [['.' for _ in range(TAMANHO_MATRIZ)] for _ in range(TAMANHO_MATRIZ)]
    for r, c in PONTOS_TESOUROS:
        mapa[r][c] = 'T'
    for r, c in OBSTACULOS:
        mapa[r][c] = 'X'
    for r, c in PONTOS_INICIAIS_EQUIPE:
        mapa[r][c] = 'S'
    # print('\n--- Mapa (T=Tesouro, X=Obstáculo, S=Start) ---')
    #for linha in mapa:
    #    print(''.join(ch + ' ' for ch in linha))
    #print('----------------------------------------------\n')

def mostrar_caminho(mapa, cromossomo, agentes_iniciais):
    import copy
    mapa_visu = copy.deepcopy(mapa)
    simbolos = ['1', '2', '3', '4']

    for i, movimentos in enumerate(cromossomo.movimentos):
        x, y = agentes_iniciais[i]
        for mov in movimentos:
            if mov == 'U': x -= 1
            elif mov == 'D': x += 1
            elif mov == 'L': y -= 1
            elif mov == 'R': y += 1

            # se sair do mapa ou bater num obstáculo, para
            if not (0 <= x < len(mapa_visu) and 0 <= y < len(mapa_visu[0])):
                break
            if mapa_visu[x][y] == 'X':
                break

            # marca o caminho sempre (pode sobrepor outro número)
            if mapa_visu[x][y] in ['.', '1', '2', '3', '4']:  
                mapa_visu[x][y] = simbolos[i]

    print("\n--- Caminho final (1–4 = agentes) ---")
    for linha in mapa_visu:
        print(" ".join(linha))
    print("--------------------------------------\n")



def algoritmo_genetico_main(nome_execucao="AG Multiagente (4 agentes)"):
    criar_mapa_printavel()
    populacao = inicializar_populacao()

    historico_melhor = []
    historico_medio = []
    melhor_global = None

    for geracao in range(MAX_GERACOES):
        fitness_scores = []
        for individuo in populacao:
            score = calcular_fitness(individuo)
            fitness_scores.append(score)

        fitness_medio = sum(fitness_scores) / len(populacao)
        melhor_da_geracao = max(populacao, key=lambda c: c.fitness)

        if melhor_global is None or melhor_da_geracao.fitness > melhor_global.fitness:
            melhor_global = melhor_da_geracao

        historico_melhor.append(melhor_global.fitness)
        historico_medio.append(fitness_medio)

        if geracao % 5 == 0 or geracao == MAX_GERACOES - 1:
            print(f"Geração {geracao:03d}: Melhor = {melhor_global.fitness:.2f} | Médio = {fitness_medio:.2f} | Tesouros coletados (melhor indivíduo) = {int((melhor_global.fitness // 1000))}")

        # critério simples de parada (se colher todos os tesouros)
        if melhor_global.fitness >= (len(PONTOS_TESOUROS) * FITNESS_COLETA_PESO):
            print('\nTodos os tesouros foram coletados por um indivíduo! Parando...')
            break

        # Geração seguinte com elitismo simples
        proxima = [melhor_da_geracao]
        while len(proxima) < TAMANHO_POPULACAO:
            p1 = selecao_torneio(populacao)
            p2 = selecao_torneio(populacao)
            f1, f2 = cruzamento_ponto_unico(p1, p2)
            mutacao(f1); mutacao(f2)
            proxima.extend([f1, f2])
        populacao = proxima[:TAMANHO_POPULACAO]
    mapa_base = [['.' for _ in range(TAMANHO_MATRIZ)] for _ in range(TAMANHO_MATRIZ)]
    for r, c in PONTOS_TESOUROS:
        mapa_base[r][c] = 'T'
    for r, c in OBSTACULOS:
        mapa_base[r][c] = 'X'
    for r, c in PONTOS_INICIAIS_EQUIPE:
        mapa_base[r][c] = 'S'
    mostrar_caminho(mapa_base, melhor_global, PONTOS_INICIAIS_EQUIPE)

    return melhor_global, historico_melhor, historico_medio

if __name__ == '__main__':
    nome = 'AG Caça ao Tesouro - 4 Agentes por Indivíduo'
    resultado, hist_melhor, hist_medio = algoritmo_genetico_main(nome_execucao=nome)
    plotar_historico_fitness(hist_melhor, hist_medio, nome_execucao=nome)

    print('\n--- Resultado Final ---')
    print(f'Melhor Fitness Final: {resultado.fitness:.2f}')
    # mostra quantos tesouros coletou (apenas aproximação: cada tesouro vale FITNESS_COLETA_PESO)
    from config import FITNESS_COLETA_PESO
    coletados_aproximados = int(resultado.fitness // FITNESS_COLETA_PESO)
    print(f'Tesouros coletados (aprox.): {coletados_aproximados} de {len(PONTOS_TESOUROS)}')
    for i, seq in enumerate(resultado.movimentos):
        print(f'Agente {i+1} - Movimentos: {"".join(seq)}')
    print('------------------------')
    