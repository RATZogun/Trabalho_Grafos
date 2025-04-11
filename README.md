<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Documentação do Programa do Trabalho de Grafos</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }
        h1 { color: #2c3e50; }
        h2 { color: #34495e; margin-top: 20px; }
        code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
        .funcao { margin-bottom: 15px; padding: 10px; border-left: 4px solid #3498db; }
    </style>
</head>
<body>
    <h1>Análise de Grafos - Documentação</h1>
    <p>Este programa realiza análise de grafos a partir de arquivos de texto, calculando métricas como densidade, componentes conectados, caminhos mínimos e outras propriedades.</p>

    <h2>Estrutura do Programa</h2>
    <ul>
        <li><strong>modelar_grafo(conteudo)</strong>: Processa o conteúdo do arquivo para criar matrizes de adjacência e predecessores.</li>
        <li><strong>ler_arquivo(nome_arquivo)</strong>: Lê o conteúdo de um arquivo no diretório "selected_instances/".</li>
        <!-- Lista todas as funções principais -->
    </ul>

    <h2>Detalhamento das Funções</h2>

    <div class="funcao">
        <h3>1. modelar_grafo(conteudo)</h3>
        <p><strong>Objetivo:</strong> Converte o conteúdo do arquivo em matrizes de adjacência e predecessores.</p>
        <p><strong>Processo:</strong></p>
        <ul>
            <li>Identifica nós únicos e mapeia seus índices</li>
            <li>Cria matrizes inicializadas com zeros</li>
            <li>Preenche valores para arestas (não direcionadas) e arcos (direcionados)</li>
        </ul>
    </div>

    <div class="funcao">
        <h3>2. ler_arquivo(nome_arquivo)</h3>
        <p><strong>Objetivo:</strong> Carrega o conteúdo do arquivo especificado.</p>
        <p><strong>Tratamento de erros:</strong> Retorna mensagens para arquivo não encontrado ou outros erros.</p>
    </div>

    <div class="funcao">
        <h3>3. calcular_quantidade_vertices(matriz)</h3>
        <p>Retorna o número total de vértices do grafo.</p>
    </div>

    <div class="funcao">
        <h3>4. calcular_quantidade_arestas(matriz)</h3>
        <p>Calcula arestas não direcionadas (divide por 2 para evitar dupla contagem).</p>
    </div>

    <div class="funcao">
        <h3>5. dijkstra(matriz, origem, predessores)</h3>
        <p><strong>Algoritmo:</strong> Calcula os caminhos mínimos de um vértice origem para todos os outros.</p>
        <p><strong>Saída:</strong> Lista de distâncias e atualização da matriz de predecessores.</p>
    </div>

    <h2>Métricas Calculadas</h2>
    <ul>
        <li><strong>Densidade:</strong> Razão entre arestas existentes e possíveis</li>
        <li><strong>Componentes Conectados:</strong> Grupos de vértices interconectados</li>
        <li><strong>Betweenness Centrality:</strong> Quantos caminhos mínimos passam por cada vértice</li>
        <li><strong>Diâmetro:</strong> Maior distância entre qualquer par de vértices</li>
    </ul>

    <h2>Como Utilizar</h2>
    <ol>
        <li>Execute o programa e insira o nome do arquivo</li>
        <li>Use o menu para:
            <ul>
                <li><strong>Opção 1:</strong> Carregar novo arquivo</li>
                <li><strong>Opção 2:</strong> Visualizar matrizes</li>
                <li><strong>Opção 3:</strong> Exibir todas as métricas</li>
            </ul>
        </li>
    </ol>

    <h2>Dependências</h2>
    <ul>
        <li>Python 3.x</li>
        <li>Bibliotecas: <code>os</code>, <code>heapq</code></li>
    </ul>
</body>
</html>