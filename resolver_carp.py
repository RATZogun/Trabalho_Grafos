import os
from carp_reader import ler_instancia_carp
from carp_solver import CARPSolver


def main():
    # Lista todas as instâncias disponíveis
    instancias = [
        f for f in os.listdir("selected_instances")
        if f.endswith(".dat")
    ]
    
    print("Instâncias disponíveis:")
    for i, instancia in enumerate(instancias, 1):
        print(f"{i}. {instancia}")
    
    # Solicita a escolha da instância
    while True:
        try:
            escolha = int(input("\nEscolha o número da instância: "))
            if 1 <= escolha <= len(instancias):
                break
            print("Escolha inválida. Tente novamente.")
        except ValueError:
            print("Por favor, digite um número válido.")
    
    nome_arquivo = instancias[escolha - 1]
    caminho_arquivo = os.path.join("selected_instances", nome_arquivo)
    
    print("\nResolvendo a instância:", nome_arquivo)
    
    try:
        # Lê a instância
        matriz_adjacencia, arestas_requeridas, capacidade, deposito = \
            ler_instancia_carp(caminho_arquivo)
        
        print("\nInformações da instância:")
        print(f"- Número de vértices: {len(matriz_adjacencia)}")
        print("- Número de arestas requeridas: "
              f"{sum(1 for a in arestas_requeridas if a.requerida)}")
        print(f"- Capacidade do veículo: {capacidade}")
        print(f"- Vértice do depósito: {deposito}")
        
        # Cria e executa o solver
        solver = CARPSolver(
            matriz_adjacencia,
            arestas_requeridas,
            capacidade,
            deposito
        )
        
        print("\nResolvendo o problema...")
        rotas, custo_total = solver.resolver()
        
        print("\nSolução encontrada:")
        print(f"- Custo total: {custo_total}")
        print(f"- Número de rotas: {len(rotas)}")
        
        # Gera o arquivo de solução
        nome_solucao = f"solucao_{nome_arquivo[:-4]}.dat"
        solver.gerar_arquivo_solucao(rotas, custo_total, nome_solucao)
        print("\nSolução salva em:", nome_solucao)
        
    except Exception as e:
        print("Erro ao resolver a instância:", e)