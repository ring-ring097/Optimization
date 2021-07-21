import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from itertools import combinations

# 問題のグラフ生成と表示
np.random.seed(1000)

G = nx.grid_2d_graph(4,3)
for (u,v) in G.edges():
    G[u][v]['weight'] = np.random.randint(1,6)

nx.draw_networkx(G,
                 pos={v:v for v in G.nodes()},
                 node_color='lightgray',
                 node_size=1500,
                 width=1)
nx.draw_networkx_edge_labels(G,
                             edge_labels={(u,v):G[u][v]['weight'] for (u,v) in G.edges()},
                             pos={v:v for v in G.nodes()},)
plt.axis('off')
plt.show()

# 全ての奇点間の最短路の長さを計算
# 奇点の点集合作成
Vodd = [v for v in G.nodes() if G.degree(v)%2 == 1]
#dist[vodd1][vodd2]に計算結果を格納
dist = dict(nx.all_pairs_dijkstra_path_length(G))

# 頂点がVoddの完全グラフを作成（重みは最短路長）
K = nx.Graph()
K.add_weighted_edges_from([(u,v,dist[u][v])
                           for (u,v) in combinations(Vodd, 2)])
nx.draw_networkx(K,
                 pos={v:v for v in K.nodes()},
                 node_color='lightgray',
                 node_size=1500,
                 width=1)
nx.draw_networkx_edge_labels(K,
                             pos={v:v for v in K.nodes()},
                             edge_labels={(u,v):K[u][v]['weight'] for (u,v) in K.edges()})
plt.axis('off')
plt.show()

# 重み最小の完全マッチングを求める（偶数個の頂点からなる完全グラフは必ず最適解を持つ）
# 重みを汎化して重み最大マッチングを求めることで重み最小マッチングを得る
CK = K.copy()
wm = max(CK[u][v]['weight'] for (u,v) in CK.edges())
for (u,v) in K.edges():
    CK[u][v]['weight'] = wm - CK[u][v]['weight'] + 1

m = nx.max_weight_matching(CK, maxcardinality=True)
md = dict(m)
mm = []
for (u,v) in md.items():
    if (u,v) not in mm and (v,u) not in mm:
        mm.append((u,v))

nx.draw_networkx(CK,
                 pos={v:v for v in CK.nodes()},
                 node_color='lightgray',
                 node_size=1500,
                 width=1)
nx.draw_networkx_edge_labels(CK,
                             pos={v:v for v in CK.nodes()},
                             edge_labels={(u,v):CK[u][v]['weight'] for (u,v) in CK.edges()})
nx.draw_networkx_edges(CK,
                       pos={v:v for v in CK.nodes()},
                       edgelist=mm,
                       width=5)
plt.axis('off')
plt.show()

# マッチング（最短路）に沿って，枝を重複させてオイラー閉路を求める
CG = G.copy()
for (u,v) in mm:
    dp = nx.dijkstra_path(G, u, v)
    for i in range(len(dp)-1):
        (ux, uy) = dp[i]
        (vx, vy) = dp[i+1]
        if ux == vx:
            wx = ux + 0.3
            wy = (uy + vy) / 2.0
        else:
            wx = (ux + vx) / 2.0
            wy = uy + 0.3
        CG.add_edges_from([((ux,uy), (wx,wy)), ((wx,wy), (vx,vy))])

nx.draw_networkx(CG, 
                 pos={v:v for v in CG.nodes()},
                 node_color='lightgray',
                 node_size=1500,
                 width=1)
plt.axis('off')
plt.show()

# できたグラフからオイラー閉路を作成
ec = nx.eulerian_circuit(CG)
for (i,j) in ec:
    print(i, end='->')
print('end')
