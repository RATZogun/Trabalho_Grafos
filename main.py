import os
import heapq


def modelar_grafo(conteudo):
    linhas = conteudo.splitlines()

    # Identificar os nós e criar um mapeamento de índices
    nos = {}
    secao_nos = False
    for linha in linhas:
        if linha.startswith("ReN."):
            secao_nos = True
            continue
        if secao_nos and linha.strip() == "":
            secao_nos = False
        if secao_nos:
            partes = linha.split()
            no = partes[0]
            if no not in nos:
                nos[no] = len(nos)  # Atribuir um índice único para cada nó

    # Criar uma matriz de adjacência inicializada com zeros
    tamanho = len(nos)
    matriz_adjacencia = [[0] * tamanho for _ in range(tamanho)]
    matriz_predessores = [[-1] * tamanho for _ in range(tamanho)]

    # Preencher a matriz com os valores do arquivo
    secao_arestas = False
    secao_arcos = False
    for linha in linhas:
        if linha.startswith("ReE."):
            secao_arestas = True
            secao_arcos = False
            continue
        if linha.startswith("ReA."):
            secao_arcos = True
            secao_arestas = False
            continue
        if linha.strip() == "":
            secao_arestas = False
            secao_arcos = False
        if secao_arestas or secao_arcos:
            partes = linha.split()
            de = f"N{partes[1]}"
            para = f"N{partes[2]}"
            custo_transporte = int(partes[3])
            if de in nos and para in nos:
                matriz_adjacencia[nos[de]][nos[para]] = custo_transporte
                matriz_predessores[nos[de]][nos[para]] = nos[de]
                if secao_arestas:
                    matriz_adjacencia[nos[para]][nos[de]] = custo_transporte
                    matriz_predessores[nos[para]][nos[de]] = nos[para]

    return matriz_adjacencia, matriz_predessores


def ler_arquivo(nome_arquivo):
    caminho = os.path.join("selected_instances/", nome_arquivo)
    try:
        with open(caminho, "r") as file:
            conteudo = file.read()
            return conteudo
    except FileNotFoundError:
        return "Erro: O arquivo não foi encontrado. Verifique o nome e tente novamente."
    except Exception as e:
        return f"Erro ao acessar o arquivo: {e}"


def calcular_quantidade_vertices(matriz_adjacencia):
    return len(matriz_adjacencia)


def calcular_quantidade_arestas(matriz_adjacencia):
    quantidade_arestas = 0
    for i in range(len(matriz_adjacencia)):
        for j in range(len(matriz_adjacencia[i])):
            if matriz_adjacencia[i][j] != 0:
                quantidade_arestas += 1
    return quantidade_arestas // 2  # Dividir por 2 para evitar contagem dupla


def calcular_quantidade_arcos(matriz_adjacencia):
    quantidade_arcos = 0
    for i in range(len(matriz_adjacencia)):
        for j in range(len(matriz_adjacencia[i])):
            if matriz_adjacencia[i][j] != 0:
                quantidade_arcos += 1
    return quantidade_arcos  # Contagem direta, pois arcos são direcionais


def calcular_quantidade_vertices_requeridos(matriz_adjacencia):
    vertices_requeridos = set()
    for i in range(len(matriz_adjacencia)):
        for j in range(len(matriz_adjacencia[i])):
            if matriz_adjacencia[i][j] != 0:
                vertices_requeridos.add(i)
                vertices_requeridos.add(j)
    return len(
        vertices_requeridos
    )  # Retorna a quantidade de vértices únicos requeridos


def calcular_quantidade_arestas_requeridas(matriz_adjacencia):
    quantidade_arestas_requeridas = 0
    for i in range(len(matriz_adjacencia)):
        for j in range(len(matriz_adjacencia[i])):
            if matriz_adjacencia[i][j] != 0:
                quantidade_arestas_requeridas += 1
    return (
        quantidade_arestas_requeridas // 2
    )  # Dividir por 2 para evitar contagem dupla


def calcular_quantidade_arcos_requeridos(matriz_adjacencia):
    quantidade_arcos_requeridos = 0
    for i in range(len(matriz_adjacencia)):
        for j in range(len(matriz_adjacencia[i])):
            if matriz_adjacencia[i][j] != 0:
                quantidade_arcos_requeridos += 1
    return quantidade_arcos_requeridos  # Contagem direta, pois arcos são direcionais


def calcular_densidade_grafo(matriz_adjacencia):
    quantidade_vertices = calcular_quantidade_vertices(matriz_adjacencia)
    quantidade_arestas = calcular_quantidade_arestas(matriz_adjacencia)
    if quantidade_vertices > 1:
        densidade = (2 * quantidade_arestas) / (
            quantidade_vertices * (quantidade_vertices - 1)
        )
    else:
        densidade = 0
    return densidade


def retorna_componentes_conectados(matriz_adjacencia):
    componentes = []
    visitados = set()

    for i in range(len(matriz_adjacencia)):
        if i not in visitados:
            componente = []
            pilha = [i]

            while pilha:
                vertice = pilha.pop()
                if vertice not in visitados:
                    visitados.add(vertice)
                    componente.append(vertice)
                    for j in range(len(matriz_adjacencia[vertice])):
                        if matriz_adjacencia[vertice][j] != 0 and j not in visitados:
                            pilha.append(j)

            componentes.append(componente)

    return componentes


def calcular_grau_minimo_vertices(matriz_adjacencia):
    grau_minimo = float("inf")
    for i in range(len(matriz_adjacencia)):
        grau = sum(
            1 for j in range(len(matriz_adjacencia[i])) if matriz_adjacencia[i][j] != 0
        )
        if grau < grau_minimo:
            grau_minimo = grau
    return grau_minimo


def calcular_grau_maximo_vertices(matriz_adjacencia):
    grau_maximo = float("-inf")
    for i in range(len(matriz_adjacencia)):
        grau = sum(
            1 for j in range(len(matriz_adjacencia[i])) if matriz_adjacencia[i][j] != 0
        )
        if grau > grau_maximo:
            grau_maximo = grau
    return grau_maximo


def dijkstra(matriz, origem, matriz_predessores):
    distancias = [float("inf")] * len(matriz)
    distancias[origem] = 0
    heap = [(0, origem)]

    while heap:
        distancia_atual, no_atual = heapq.heappop(heap)

        if distancia_atual > distancias[no_atual]:
            continue

        for vizinho in range(len(matriz[no_atual])):
            if matriz[no_atual][vizinho] != 0:
                nova_distancia = distancia_atual + matriz[no_atual][vizinho]
                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
                    matriz_predessores[origem][vizinho] = no_atual
                    heapq.heappush(heap, (nova_distancia, vizinho))

    return distancias


def calcular_intermediacao(matriz_adjacencia, matriz_predessores):
    intermediacao = [0] * len(matriz_adjacencia)

    for origem in range(len(matriz_adjacencia)):
        dijkstra(matriz_adjacencia, origem, matriz_predessores)

        for destino in range(len(matriz_adjacencia)):
            if origem != destino:
                caminho = []
                atual = destino
                while atual != -1 and atual != origem:
                    caminho.append(atual)
                    atual = matriz_predessores[origem][atual]
                caminho.reverse()

                for no in caminho[1:-1]:  # Exclui origem e destino
                    intermediacao[no] += 1

    return intermediacao


def calcular_caminho_medio(matriz_adjacencia, matriz_predessores):
    total_caminhos = 0
    total_distancia = 0

    for origem in range(len(matriz_adjacencia)):
        distancias = dijkstra(matriz_adjacencia, origem, matriz_predessores)
        for destino in range(len(distancias)):
            if origem != destino and distancias[destino] != float("inf"):
                total_caminhos += 1
                total_distancia += distancias[destino]

    if total_caminhos > 0:
        return total_distancia / total_caminhos
    else:
        return 0


def calcular_diametro(matriz_adjacencia, matriz_predessores):
    diametro = 0

    for origem in range(len(matriz_adjacencia)):
        distancias = dijkstra(matriz_adjacencia, origem, matriz_predessores)
        for destino in range(len(distancias)):
            if origem != destino and distancias[destino] != float("inf"):
                if distancias[destino] > diametro:
                    diametro = distancias[destino]

    return diametro


def imprimir_matriz(matriz, matriz_predessores):
    tamanho = len(matriz)

    # Imprimir cabeçalho da matriz de adjacência
    print("Matriz de Adjacência:")
    print("\t" + "\t".join(str(i + 1) for i in range(tamanho)))

    # Imprimir linhas da matriz de adjacência
    for i in range(tamanho):
        linha = [str(matriz[i][j]) for j in range(tamanho)]
        print(f"{i + 1}\t" + "\t".join(linha))

    print("\nMatriz de Predecessores:")
    print("\t" + "\t".join(str(i + 1) for i in range(tamanho)))

    # Imprimir linhas da matriz de predecessores
    for i in range(tamanho):
        linha = [str(matriz_predessores[i][j]) for j in range(tamanho)]
        print(f"{i + 1}\t" + "\t".join(linha))


def exibir_metricas(matriz_adjacencia, matriz_predessores):
    print("\nMétricas do Grafo:")
    print(
        f"1. Quantidade de vértices: "
        f"{calcular_quantidade_vertices(matriz_adjacencia)}"
    )
    print(
        f"2. Quantidade de arestas: "
        f"{calcular_quantidade_arestas(matriz_adjacencia)}"
    )
    print(
        f"3. Quantidade de arcos: "
        f"{calcular_quantidade_arcos(matriz_adjacencia)}"
    )
    print(
        f"4. Quantidade de vértices requeridos: "
        f"{calcular_quantidade_vertices_requeridos(matriz_adjacencia)}"
    )
    print(
        f"5. Quantidade de arestas requeridas: "
        f"{calcular_quantidade_arestas_requeridas(matriz_adjacencia)}"
    )
    print(
        f"6. Quantidade de arcos requeridos: "
        f"{calcular_quantidade_arcos_requeridos(matriz_adjacencia)}"
    )
    print(
        f"7. Densidade do grafo: "
        f"{calcular_densidade_grafo(matriz_adjacencia):.4f}"
    )
    print(
        f"8. Componentes conectados: "
        f"{retorna_componentes_conectados(matriz_adjacencia)}"
    )
    print(
        f"9. Grau mínimo dos vértices: "
        f"{calcular_grau_minimo_vertices(matriz_adjacencia)}"
    )
    print(
        f"10. Grau máximo dos vértices: "
        f"{calcular_grau_maximo_vertices(matriz_adjacencia)}"
    )
    print(
        f"11. Intermediação: "
        f"{calcular_intermediacao(matriz_adjacencia, matriz_predessores)}"
    )
    print(
        f"12. Caminho médio: "
        f"{calcular_caminho_medio(matriz_adjacencia, matriz_predessores):.4f}"
    )
    print(
        f"13. Diâmetro: "
        f"{calcular_diametro(matriz_adjacencia, matriz_predessores)}"
    )


def main():
    print("Bem-vindo ao programa de análise de grafos!")
    matriz_adjacencia = None

    while True:
        if matriz_adjacencia is None:
            arquivo = input(
                "\nPor favor, insira o nome do arquivo que deseja acessar: "
            )
            conteudo = ler_arquivo(arquivo)
            if conteudo.startswith("Erro"):
                print("\nResultado:")
                print(conteudo)
                continue
            else:
                matriz_adjacencia, matriz_predessores = modelar_grafo(conteudo)

        print("\nMenu:")
        print("1. Ler novo arquivo")
        print("2. Exibir matriz do grafo")
        print("3. Exibir métricas do grafo")
        print("4. Fechar programa")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            matriz_adjacencia = None
        elif opcao == "2":
            imprimir_matriz(matriz_adjacencia, matriz_predessores)
        elif opcao == "3":
            exibir_metricas(matriz_adjacencia, matriz_predessores)
        elif opcao == "4":
            print("Encerrando o programa. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
