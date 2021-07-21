import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from itertools import combinations
import sys
import fileinput
from pathlib import Path


# 問題のグラフ生成と表示
def MakeGraph(ARGV):
    if len(ARGV) < 1:
        print('グリッドのサイズを正しく入力してください')
        sys.exit()
    elif len(ARGV) == 2:
        print('重みをランダムで設定します')
        G = nx.grid_2d_graph(int(ARGV[0]), int(ARGV[1]))
        for (u,v) in G.edges():
            G[u][v]['weight'] = np.random.randint(1,6)
    else:
        G = nx.grid_2d_graph(int(ARGV[0]), int(ARGV[1]))
        n = 2
        for (u,v) in G.edges():
            G[u][v]['weight'] = ARGV[n]
            n += 1

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
    return G

# 全ての奇点間の最短路の長さを計算
def MakeOddGraph(G):
    # 奇点の点集合作成
    Vodd = [v for v in G.nodes() if G.degree(v)%2 == 1]
    if len(Vodd) == 0:
        return 0
    else:
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
        return K

# 重み最小の完全マッチングを求める（偶数個の頂点からなる完全グラフは必ず最適解を持つ）
# 重みを汎化して重み最大マッチングを求めることで重み最小マッチングを得る
def WeightMatching(K):
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
    return mm

# マッチング（最短路）に沿って，枝を重複させてオイラー閉路を求める
def EulerGraph(G, mm):
    CG = G.copy()
    for (u,v) in mm:
        dp = nx.dijkstra_path(G, u, v)
        # NetWorkXのGraphでは多重辺を扱えないので中間点を作成する
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
    return CG

# できたグラフからオイラー閉路を作成
def EulerCircuit(CG):
    ec = nx.eulerian_circuit(CG)
    for (i,j) in ec:
        print(i, end='->')
    print('end')
    return 0

# 入力からグラフを作成
# 標準入力ファイルを数値リストに変換
if len(sys.argv) == 1:
    print('問題ファイルを指定してください')
    sys.exit()
elif len(sys.argv) > 2:
    print('指定できる問題ファイルは1つです')
    sys.exit()
elif Path(sys.argv[1]).exists():
    ARGV = []
    for line in fileinput.input():
        argv = list(map(float,line.split()))
        ARGV.extend(argv)

    print(ARGV)
else:
    print("error")
    sys.exit()


G = MakeGraph(ARGV)
K = MakeOddGraph(G)
if K == 0:
    EulerCircuit(G)
else:
    mm = WeightMatching(K)
    CG = EulerGraph(G, mm)
    EulerCircuit(CG)

