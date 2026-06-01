import heapq
import sys


def solve():
    dados = sys.stdin.buffer.read().split()
    idx = 0
    n = int(dados[idx]); idx += 1
    m = int(dados[idx]); idx += 1
    L = int(dados[idx]); idx += 1
    s = int(dados[idx]); idx += 1
    t = int(dados[idx]); idx += 1

    arestas = []
    adj = [[] for _ in range(n)]
    for i in range(m):
        u = int(dados[idx]); idx += 1
        v = int(dados[idx]); idx += 1
        w = int(dados[idx]); idx += 1
        arestas.append((u, v, w))
        adj[u].append((v, i))
        adj[v].append((u, i))

    INF = float('inf')

    def dijkstra(val_zero):
        dist = [INF] * n
        dist[s] = 0
        anterior = [-1] * n
        aresta_anterior = [-1] * n
        fila = [(0, s)]
        while fila:
            d, u = heapq.heappop(fila)
            if d > dist[u]:
                continue
            for v, idx_aresta in adj[u]:
                w = arestas[idx_aresta][2] or val_zero
                nova_dist = d + w
                if nova_dist < dist[v]:
                    dist[v] = nova_dist
                    anterior[v] = u
                    aresta_anterior[v] = idx_aresta
                    heapq.heappush(fila, (nova_dist, v))
        return dist, anterior, aresta_anterior

    dist_min = dijkstra(1)[0][t]
    dist_max = dijkstra(L + 1)[0][t]

    if dist_min > L or dist_max < L:
        print("NO")
        return

    esq, dir = 1, L + 1
    while esq < dir:
        meio = (esq + dir) // 2
        if dijkstra(meio)[0][t] >= L:
            dir = meio
        else:
            esq = meio + 1
    x_otimo = esq

    dist, anterior, aresta_anterior = dijkstra(x_otimo)
    delta = dist[t] - L

    atribuidos = {}
    v = t
    while v != s:
        idx_aresta = aresta_anterior[v]
        if delta > 0 and arestas[idx_aresta][2] == 0:
            atribuidos[idx_aresta] = x_otimo - 1
            delta -= 1
        v = anterior[v]

    saida = ["YES"]
    for i, (u, v, w) in enumerate(arestas):
        saida.append(f"{u} {v} {atribuidos.get(i, x_otimo) if w == 0 else w}")
    print('\n'.join(saida))


solve()
