import heapq
from dataclasses import dataclass
from typing import List, Tuple
import time

@dataclass
class Aresta:
    origem: int
    destino: int
    custo: int
    demanda: int
    custo_servico: int
    requerida: bool = False
    id: int = 0

@dataclass
class Rota:
    sequencia: List[Tuple[int, int, int]]  # (origem, destino, id_servico)
    demanda_total: int
    custo_total: int


class CARPSolver:
    def __init__(self, matriz_adjacencia: List[List[int]], arestas_requeridas: List[Aresta], capacidade_veiculo: int, deposito: int):
        self.matriz_adjacencia = matriz_adjacencia
        self.arestas_requeridas = arestas_requeridas
        self.capacidade_veiculo = capacidade_veiculo
        self.deposito = deposito
        self.num_vertices = len(matriz_adjacencia)
        self.distancias = self._calcular_distancias()

    def _calcular_distancias(self) -> List[List[int]]:
        """Calcula as distâncias mínimas entre todos os pares de vértices usando Floyd-Warshall"""
        dist = [[float('inf')] * self.num_vertices for _ in range(self.num_vertices)]
        
        # Inicializa com as distâncias diretas da matriz de adjacência
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                if i == j:
                    dist[i][j] = 0
                elif self.matriz_adjacencia[i][j] != 0:
                    dist[i][j] = self.matriz_adjacencia[i][j]
        
        # Algoritmo Floyd-Warshall
        for k in range(self.num_vertices):
            for i in range(self.num_vertices):
                for j in range(self.num_vertices):
                    if dist[i][k] != float('inf') and dist[k][j] != float('inf'):
                        dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
        
        return dist

    def _encontrar_caminho(self, origem: int, destino: int) -> List[int]:
        """Encontra o caminho mais curto entre dois vértices usando Dijkstra"""
        distancias = [float('inf')] * self.num_vertices
        distancias[origem] = 0
        predecessores = [-1] * self.num_vertices
        heap = [(0, origem)]
        visitados = set()

        while heap:
            dist_atual, vertice_atual = heapq.heappop(heap)
            
            if vertice_atual in visitados:
                continue
                
            visitados.add(vertice_atual)
            
            if vertice_atual == destino:
                break
                
            for vizinho in range(self.num_vertices):
                if self.matriz_adjacencia[vertice_atual][vizinho] != 0:
                    nova_dist = dist_atual + self.matriz_adjacencia[vertice_atual][vizinho]
                    if nova_dist < distancias[vizinho]:
                        distancias[vizinho] = nova_dist
                        predecessores[vizinho] = vertice_atual
                        heapq.heappush(heap, (nova_dist, vizinho))

        # Reconstrói o caminho
        if predecessores[destino] == -1:
            return []
            
        caminho = []
        atual = destino
        while atual != -1:
            caminho.append(atual)
            atual = predecessores[atual]
        return list(reversed(caminho))

    def _calcular_custo_rota(self, rota: List[Tuple[int, int, int]]) -> int:
        """Calcula o custo total de uma rota"""
        if not rota:
            return 0
            
        custo_total = 0
        vertice_atual = self.deposito

        # Custo para ir do depósito até o primeiro serviço
        custo_total += self.distancias[vertice_atual][rota[0][0]]

        # Custo dos serviços e deslocamentos entre eles
        for i, (origem, destino, _) in enumerate(rota):
            # Custo do serviço
            for aresta in self.arestas_requeridas:
                if ((aresta.origem == origem and aresta.destino == destino) or
                    (not aresta.requerida and 
                     aresta.origem == destino and aresta.destino == origem)):
                    custo_total += aresta.custo_servico
                    break
            
            # Custo para ir até o próximo serviço
            if i < len(rota) - 1:
                proximo_origem = rota[i + 1][0]
                if destino != proximo_origem:
                    custo_total += self.distancias[destino][proximo_origem]
            
            vertice_atual = destino

        # Custo para retornar ao depósito
        custo_total += self.distancias[vertice_atual][self.deposito]

        return custo_total

    def _construir_solucao_inicial(self) -> List[Rota]:
        """Constrói uma solução inicial usando uma heurística construtiva path-scanning"""
        rotas: List[Rota] = []
        # Filtra apenas arestas requeridas e atribui IDs únicos
        arestas_nao_atendidas = []
        id_servico = 1
        for aresta in self.arestas_requeridas:
            if aresta.requerida:
                aresta.id = id_servico
                arestas_nao_atendidas.append(aresta)
                id_servico += 1
        
        while arestas_nao_atendidas:
            rota_atual: List[Tuple[int, int, int]] = []  # (origem, destino, id_servico)
            demanda_atual = 0
            vertice_atual = self.deposito
            
            while arestas_nao_atendidas:
                # Lista de arestas candidatas (que respeitam a capacidade)
                candidatas = [
                    aresta for aresta in arestas_nao_atendidas
                    if demanda_atual + aresta.demanda <= self.capacidade_veiculo
                ]
                
                if not candidatas:
                    break
                
                # Critérios de seleção
                melhor_aresta = None
                melhor_valor = float('inf')
                
                for aresta in candidatas:
                    # Custo para chegar na aresta
                    custo_ate_origem = self.distancias[vertice_atual][aresta.origem]
                    
                    # Distância até o depósito após servir a aresta
                    dist_deposito_origem = self.distancias[aresta.origem][self.deposito]
                    dist_deposito_destino = self.distancias[aresta.destino][self.deposito]
                    
                    # Critério 1: Minimizar custo/demanda
                    valor_servico = (aresta.custo_servico + custo_ate_origem) / aresta.demanda
                    
                    # Critério 2: Priorizar arestas mais distantes do depósito quando capacidade alta
                    if demanda_atual < self.capacidade_veiculo * 0.7:
                        valor_servico -= max(dist_deposito_origem, dist_deposito_destino) * 0.3
                    else:
                        valor_servico += min(dist_deposito_origem, dist_deposito_destino) * 0.3
                    
                    if valor_servico < melhor_valor:
                        melhor_valor = valor_servico
                        melhor_aresta = aresta
                
                # Adiciona a aresta à rota
                rota_atual.append(
                    (melhor_aresta.origem, melhor_aresta.destino, melhor_aresta.id)
                )
                demanda_atual += melhor_aresta.demanda
                vertice_atual = melhor_aresta.destino
                arestas_nao_atendidas.remove(melhor_aresta)
            
            if rota_atual:
                custo_total = self._calcular_custo_rota(rota_atual)
                rotas.append(Rota(rota_atual, demanda_atual, custo_total))
        
        return rotas

    def _melhorar_solucao(self, rotas: List[Rota], max_iteracoes: int = 1000) -> List[Rota]:
        """Melhora a solução usando múltiplas estratégias de busca local"""
        melhor_custo_total = sum(rota.custo_total for rota in rotas)
        
        for _ in range(max_iteracoes):
            melhorou = False
            
            # 1. Tenta mover serviços entre rotas
            for i in range(len(rotas)):
                for j in range(len(rotas)):
                    if i == j:
                        continue
                    
                    for pos_i in range(len(rotas[i].sequencia)):
                        servico = rotas[i].sequencia[pos_i]
                        
                        # Encontra a demanda do serviço
                        demanda_servico = next(
                            a.demanda for a in self.arestas_requeridas
                            if ((a.origem == servico[0] and a.destino == servico[1]) or
                                (a.origem == servico[1] and a.destino == servico[0]))
                        )
                        
                        # Verifica se é possível mover para a outra rota
                        if rotas[j].demanda_total + demanda_servico <= self.capacidade_veiculo:
                            # Tenta inserir em todas as posições possíveis
                            for pos_j in range(len(rotas[j].sequencia) + 1):
                                # Move o serviço
                                nova_rota_i = (
                                    rotas[i].sequencia[:pos_i] +
                                    rotas[i].sequencia[pos_i + 1:]
                                )
                                nova_rota_j = (
                                    rotas[j].sequencia[:pos_j] +
                                    [servico] +
                                    rotas[j].sequencia[pos_j:]
                                )
                                
                                # Calcula novos custos
                                novo_custo_i = self._calcular_custo_rota(nova_rota_i)
                                novo_custo_j = self._calcular_custo_rota(nova_rota_j)
                                novo_custo_total = (
                                    sum(r.custo_total for r in rotas[:i]) +
                                    novo_custo_i +
                                    sum(r.custo_total for r in rotas[i+1:j]) +
                                    novo_custo_j +
                                    sum(r.custo_total for r in rotas[j+1:])
                                )
                                
                                if novo_custo_total < melhor_custo_total:
                                    # Atualiza as rotas
                                    rotas[i].sequencia = nova_rota_i
                                    rotas[i].custo_total = novo_custo_i
                                    rotas[i].demanda_total -= demanda_servico
                                    
                                    rotas[j].sequencia = nova_rota_j
                                    rotas[j].custo_total = novo_custo_j
                                    rotas[j].demanda_total += demanda_servico
                                    
                                    melhor_custo_total = novo_custo_total
                                    melhorou = True
                                    break
                            
                            if melhorou:
                                break
                    
                    if melhorou:
                        break
                        
                if melhorou:
                    break
            
            # 2. Tenta inverter a ordem dos serviços em cada rota
            if not melhorou:
                for i in range(len(rotas)):
                    # Tenta inverter diferentes segmentos da rota
                    for inicio in range(len(rotas[i].sequencia)):
                        for fim in range(inicio + 2, len(rotas[i].sequencia) + 1):
                            # Cria uma nova sequência com o segmento invertido
                            nova_sequencia = (
                                rotas[i].sequencia[:inicio] +
                                list(reversed(rotas[i].sequencia[inicio:fim])) +
                                rotas[i].sequencia[fim:]
                            )
                            
                            # Calcula o novo custo
                            novo_custo = self._calcular_custo_rota(nova_sequencia)
                            
                            if novo_custo < rotas[i].custo_total:
                                rotas[i].sequencia = nova_sequencia
                                rotas[i].custo_total = novo_custo
                                melhor_custo_total = sum(r.custo_total for r in rotas)
                                melhorou = True
                                break
                        
                        if melhorou:
                            break
                    
                    if melhorou:
                        break
            
            if not melhorou:
                break
        
        return rotas

    def resolver(self) -> Tuple[List[Rota], int]:
        """Resolve o problema do CARP"""
        # Marca o início da execução
        inicio = time.process_time()
        
        # Constrói uma solução inicial
        rotas = self._construir_solucao_inicial()
        
        # Melhora a solução
        rotas = self._melhorar_solucao(rotas)
        
        # Calcula o custo total
        custo_total = sum(rota.custo_total for rota in rotas)
        
        # Marca o fim da execução
        fim = time.process_time()
        
        # Calcula o total de clocks
        clocks = int((fim - inicio) * 1e9)  # Converte para nanosegundos
        
        return rotas, custo_total, clocks

    def gerar_arquivo_solucao(
        self,
        rotas: List[Rota],
        custo_total: int,
        nome_arquivo: str,
        clocks: int
    ):
        """Gera o arquivo de solução no formato especificado"""
        with open(nome_arquivo, 'w') as f:
            # Primeira linha: custo total
            f.write(f"{custo_total}\n")
            
            # Segunda linha: número de rotas
            f.write(f"{len(rotas)}\n")
            
            # Terceira linha: total de clocks referência (usando mesmo valor)
            f.write(f"{clocks}\n")
            
            # Quarta linha: total de clocks da solução
            f.write(f"{clocks}\n")
            
            # Linhas das rotas
            for i, rota in enumerate(rotas, 1):
                # Calcula demanda total da rota
                demanda_total = sum(
                    next(
                        a.demanda for a in self.arestas_requeridas
                        if (a.origem == origem and a.destino == destino) or
                           (a.origem == destino and a.destino == origem)
                    )
                    for origem, destino, _ in rota.sequencia
                )
                
                # Total de visitas = serviços + 2 (depósito início e fim)
                total_visitas = len(rota.sequencia) + 2
                
                # Formato: índice_deposito dia_rota id_rota demanda custo total_visitas
                linha = f" 0 1 {i} {demanda_total} {rota.custo_total} {total_visitas}"
                
                # Adiciona a sequência de nós com o depósito no início e fim
                linha += " (D 0,1,1)"
                
                # Adiciona os serviços com seus IDs
                for origem, destino, id_servico in rota.sequencia:
                    linha += f" (S {id_servico},{origem},{destino})"
                
                linha += " (D 0,1,1)\n"
                f.write(linha) 