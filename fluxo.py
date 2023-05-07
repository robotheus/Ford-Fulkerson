#comando para execução python3 nomeDoArquivo verticeDeOrigem verticeDeDestino
#exemplo: python3 input.txt S T

import networkx as nx
import matplotlib.pyplot as plt
import sys

def main():
    try:
        grafo = constroiGrafo(sys.argv[1])
    except:
        print("Arquivo de entrada não encontrado.")
    
    try:
        fluxo = FordFulkerson(grafo, sys.argv[2], sys.argv[3])
    except:
        print("Um dos vértices não pertence ao grafo")
        return

    print(f'Fluxo maximo do grafo: {fluxo}')
    plotaGrafo(grafo)
    
def plotaGrafo(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

def constroiGrafo(fileName):
    input = open(fileName)
    G = nx.DiGraph()

    for x in input.readlines():
        a, b, c = x.split()
        G.add_weighted_edges_from([(a,  b, int(c))])
    
    input.close()
    return G

def fluxoMaximoDoCaminho(G, caminho):
    fluxo = float('inf')

    for i in range(len(caminho) - 1):
        menor = G[caminho[i]][caminho[i+1]]['weight']
        
        if menor < fluxo:
            fluxo = menor
    
    return fluxo

def montaGF(G):
    R = nx.DiGraph()
    
    for u in G:
        for v in G[u]:
            R.add_node(u)
            R.add_node(v)
            R.add_edge(u, v, weight=G[u][v]["weight"])
    
    return R

def FordFulkerson(G, s, t):
    GF = montaGF(G)
    fluxo = 0       
    
    if(nx.has_path(GF, s, t)):
        caminho = nx.shortest_path(G, s, t)
    else:
        print("Não há caminhos válidos entre os vértices " + s + " e " + t)
        return

    while(nx.has_path(GF, s, t)):
        fluxoMAXdoCaminho = fluxoMaximoDoCaminho(G, caminho)
        
        for u in range(len(caminho) - 1):
            GF[caminho[u]][caminho[u+1]]["weight"] -= fluxoMAXdoCaminho
            
            if (GF[caminho[u]][caminho[u+1]]["weight"] == 0): 
                GF.remove_edge(caminho[u], caminho[u+1])
                fluxo += G[caminho[u]][caminho[u+1]]["weight"] 

            GF.add_edge(caminho[u+1], caminho[u], weight=fluxoMAXdoCaminho)
        
        if(nx.has_path(GF, s, t)): 
            caminho = nx.shortest_path(GF, s, t)

    return fluxo

main()