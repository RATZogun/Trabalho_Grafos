# Trabalho de Grafos - Programa em Python

Programa para análise de grafos direcionados e não direcionados a partir de arquivos de texto, calculando diversas métricas e propriedades dos grafos.

Feito para a Disciplina GCC262 - Grafos e suas Aplicações

Professor: Meyron César de O. Moreira
Aluno: Gilson dos Santos Júnior

## 📋 Funcionalidades Principais

- Leitura de arquivos no formato específico
- Cálculo de métricas de grafos:
  - Quantidade de vértices, arestas e arcos
  - Densidade do grafo
  - Componentes conectados
  - Grau mínimo e máximo dos vértices
  - Centralidade de intermediação
  - Caminho médio e diâmetro
- Visualização de matrizes de adjacência e predecessores

## 🛠️ Funções Principais

### `modelar_grafo(conteudo)`
Processa o conteúdo do arquivo para criar:
- Matriz de adjacência com custos de transporte
- Matriz de predecessores para reconstrução de caminhos

**Processo:**
1. Identifica nós únicos e cria mapeamento de índices
2. Inicializa matrizes com zeros
3. Preenche valores para arestas (não direcionadas) e arcos (direcionados)

### `ler_arquivo(nome_arquivo)`
Carrega conteúdo de arquivo do diretório `selected_instances/`

**Tratamento de erros:**
- Arquivo não encontrado
- Erros genéricos de leitura

### `dijkstra(matriz, origem, predessores)`
Implementação do algoritmo de Dijkstra para encontrar caminhos mínimos

**Saída:**
- Lista de distâncias mínimas da origem
- Atualização da matriz de predecessores

### `calcular_intermediacao(matriz_adjacencia, matriz_predessores)`
Calcula a centralidade de intermediação para cada vértice

### `exibir_metricas(matriz_adjacencia, matriz_predessores)`
Exibe todas as métricas calculadas em formato legível

## 📊 Métricas Calculadas

| Métrica | Descrição |
|---------|-----------|
| Densidade | Razão entre arestas existentes e possíveis |
| Componentes Conectados | Grupos de vértices interconectados |
| Diâmetro | Maior distância entre qualquer par de vértices |
| Caminho Médio | Média das distâncias entre todos os pares de vértices |
| Grau dos Vértices | Mínimo e máximo de conexões por vértice |
