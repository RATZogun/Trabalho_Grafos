from typing import Tuple, List
from carp_solver import Aresta


def ler_instancia_carp(
    nome_arquivo: str
) -> Tuple[List[List[int]], List[Aresta], int, int]:
    """
    Lê um arquivo de instância do CARP e retorna os dados necessários.
    
    Args:
        nome_arquivo: Nome do arquivo de instância
        
    Returns:
        Tuple contendo:
        - matriz_adjacencia: Matriz de adjacência do grafo
        - arestas_requeridas: Lista de arestas requeridas
        - capacidade_veiculo: Capacidade do veículo
        - deposito: Vértice do depósito
    """
    with open(nome_arquivo, 'r') as f:
        linhas = f.readlines()
    
    # Encontra a capacidade do veículo e o depósito no cabeçalho do arquivo
    capacidade_veiculo = None
    deposito = None
    
    for linha in linhas:
        if linha.startswith('Capacity:'):
            capacidade_veiculo = int(linha.split(':')[1].strip())
        elif linha.startswith('Depot Node:'):
            deposito = int(linha.split(':')[1].strip())
        
        if capacidade_veiculo is not None and deposito is not None:
            break
    
    if capacidade_veiculo is None:
        raise ValueError("Capacidade do veículo não encontrada no arquivo")
    
    if deposito is None:
        raise ValueError("Depósito não encontrado no arquivo")
    
    # Primeiro, vamos identificar todos os vértices para criar a matriz
    vertices = set()
    arestas_requeridas = []
    
    # Processa as linhas do arquivo
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue
            
        partes = linha.split()
        if not partes:
            continue
            
        # Verifica se é uma aresta requerida (E1, E2, etc)
        if (partes[0].startswith('E') and 
                len(partes[0]) > 1 and 
                partes[0][1:].isdigit()):
            if len(partes) >= 6:
                origem = int(partes[1])
                destino = int(partes[2])
                custo = int(partes[3])
                demanda = int(partes[4])
                custo_servico = int(partes[5])
                
                vertices.add(origem)
                vertices.add(destino)
                
                arestas_requeridas.append(
                    Aresta(origem, destino, custo, demanda, 
                        custo_servico, True)
                )
        
        # Verifica se é uma aresta não requerida (NrE1, NrE2, etc)
        elif (partes[0].startswith('NrE') and 
                len(partes[0]) > 3 and 
                partes[0][3:].isdigit()):
            if len(partes) >= 4:
                origem = int(partes[1])
                destino = int(partes[2])
                custo = int(partes[3])
                
                vertices.add(origem)
                vertices.add(destino)
                
                arestas_requeridas.append(
                    Aresta(origem, destino, custo, 0, 0, False)
                )
                
        # Verifica se é um arco requerido (A1, A2, etc)
        elif (partes[0].startswith('A') and 
                len(partes[0]) > 1 and 
                partes[0][1:].isdigit()):
            if len(partes) >= 6:
                origem = int(partes[1])
                destino = int(partes[2])
                custo = int(partes[3])
                demanda = int(partes[4])
                custo_servico = int(partes[5])
                
                vertices.add(origem)
                vertices.add(destino)
                
                arestas_requeridas.append(
                    Aresta(origem, destino, custo, demanda, 
                        custo_servico, True)
                )
        
        # Verifica se é um arco não requerido (NrA1, NrA2, etc)
        elif (partes[0].startswith('NrA') and 
                len(partes[0]) > 3 and 
                partes[0][3:].isdigit()):
            if len(partes) >= 4:
                origem = int(partes[1])
                destino = int(partes[2])
                custo = int(partes[3])
                
                vertices.add(origem)
                vertices.add(destino)
                
                arestas_requeridas.append(
                    Aresta(origem, destino, custo, 0, 0, False)
                )
    
    # Cria a matriz de adjacência
    num_vertices = max(vertices) + 1  # +1 porque os vértices começam em 1
    matriz_adjacencia = [[0] * num_vertices for _ in range(num_vertices)]
    
    # Preenche a matriz com todas as arestas e arcos
    for aresta in arestas_requeridas:
        matriz_adjacencia[aresta.origem][aresta.destino] = aresta.custo
        if not aresta.requerida:  # Se não é requerida, é bidirecional
            matriz_adjacencia[aresta.destino][aresta.origem] = aresta.custo
    
    return matriz_adjacencia, arestas_requeridas, capacidade_veiculo, deposito 