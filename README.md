# B. Complete The Graph

**Link do problema:** https://codeforces.com/problemset/problem/715/B

---

## Integrantes

- João Victor Feijó Vasconcelos

---

## Linguagem utilizada

Python 3

---

## Como executar

```bash
python src/main.py < dados/entrada1.txt
```

Ou com qualquer arquivo de entrada:

```bash
python src/main.py < <arquivo_de_entrada>
```

Também é possível digitar a entrada manualmente:

```bash
python src/main.py
# cole a entrada e pressione Ctrl+D para encerrar
```

---

## Modelagem do problema

**Vértices:** os `n` nós numerados de 0 a n-1.

**Arestas:** as `m` arestas não-direcionadas com peso. Arestas com peso `w = 0` são "apagadas" — precisam receber um valor inteiro positivo.

**Objetivo:** atribuir pesos às arestas apagadas de forma que `dist(s, t) = L` exatamente.

**Representação:** lista de adjacência (`adj[u]` contém pares `(v, índice_da_aresta)`), com um vetor `edges` separado armazenando `(u, v, w)` para cada aresta. Isso permite que o Dijkstra acesse o peso original em O(1) pelo índice.

---

## Algoritmo utilizado

Dijkstra com relaxamento de arestas e fila de prioridade mínima (`heapq`), com deleção preguiçosa (*lazy deletion*).

---

## Variação de Dijkstra usada

**Busca binária sobre o peso das arestas apagadas + Dijkstra com reconstrução de caminho.**

### Intuição

Defina `f(x)` = distância mínima de `s` a `t` quando todas as arestas apagadas recebem peso `x`. `f` é não-decrescente em `x`.

### Passos

1. **Verificação de viabilidade:**
   - Calcule `d_low = f(1)` (mínimo possível). Se `d_low > L` → **NO** (mesmo com pesos mínimos o caminho é longo demais).
   - Calcule `d_high = f(L+1)` (arestas apagadas desativadas). Se `d_high < L` → **NO** (arestas fixas já criam caminho mais curto que L).

2. **Busca binária:** encontre `x*` = menor `x ∈ [1, L+1]` tal que `f(x) ≥ L`.

3. **Construção da solução:**
   - Execute Dijkstra com todas as arestas apagadas valendo `x*`.
   - Reconstrua o caminho mínimo `P` de `s` a `t` (comprimento `f(x*) ≥ L`).
   - `delta = f(x*) - L`: reduza as primeiras `delta` arestas apagadas em `P` de `x*` para `x* - 1`.
   - Todas as demais arestas apagadas (fora de `P`) recebem `x*`.

### Correção

Após a redução, qualquer caminho `Q` que no Dijkstra com `x*` tinha comprimento ≥ `f(x*)` diminui no máximo `delta` (usa no máximo `delta` das arestas modificadas). Logo `Q ≥ f(x*) - delta = L`. O caminho `P` tem comprimento exatamente `L`. Portanto `dist(s, t) = L`. ✓

Os pesos reduzidos valem `x* - 1 ≥ 1`, pois `x* ≥ 2` sempre que `delta > 0` (quando `f(1) < L`, o `x*` encontrado pela busca binária é ≥ 2).

---

## Análise de complexidade

### Por chamada de Dijkstra

O Dijkstra com *lazy heap* (deleção preguiçosa) insere uma entrada na fila por relaxamento bem-sucedido. Com `m` arestas não-direcionadas (2m direcionadas) e `n` vértices:

| Operação | Custo |
|---|---|
| Inserções na heap (no máximo uma por relaxamento) | O(m) |
| Cada inserção/remoção (heap com no máximo O(m) entradas) | O(log m) = O(log n) |
| Varredura das listas de adjacência | O(n + m) |
| **Total por Dijkstra** | **O((n + m) log n)** |

> `log m = O(log n)` pois m ≤ n² → log m ≤ 2 log n.

### Caso geral

| Caso | Cenário | Complexidade |
|---|---|---|
| **Melhor** | Verificação de viabilidade falha (`d_low > L` ou `d_high < L`) — apenas 2 chamadas de Dijkstra | **O((n + m) log n)** |
| **Médio/Pior** | Busca binária completa (grafo esparso ou denso) | **O(log L × (n + m) log n)** |

Com os limites do problema (n ≤ 1000, m ≤ 10 000, L ≤ 10⁹):
- Total de chamadas ao Dijkstra: 2 (viabilidade) + ⌈log₂ L⌉ ≈ 30 (busca binária) + 1 (final) = **~33 chamadas**.
- Cada Dijkstra: O(11 000 × log 1000) ≈ O(11 000 × 10) = 110 000 operações.
- **Total: ~3,6 × 10⁶ operações** — dentro do limite de 4 segundos.

### Memória

O(n + m) para lista de adjacência, vetor de distâncias e heap.

---

## Evidência de Accepted

![Accepted no Codeforces](evidencias/accepted.png)
