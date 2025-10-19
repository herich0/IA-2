import matplotlib.pyplot as plt


def plotar_historico_fitness(historico_melhor, historico_medio=None, nome_execucao="AG Multiagente"):
    geracoes = range(len(historico_melhor))
    plt.figure(figsize=(10, 6))
    plt.plot(geracoes, historico_melhor, label='Melhor Fitness', linewidth=2)
    if historico_medio is not None:
        plt.plot(geracoes, historico_medio, label='Fitness Médio', linestyle='--', linewidth=1)
    plt.title(nome_execucao)
    plt.xlabel('Geração')
    plt.ylabel('Fitness')
    plt.legend()
    plt.grid(True)
    plt.show()