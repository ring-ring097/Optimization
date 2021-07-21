import networkx as nx
import matplotlib.pyplot as plt

# # # 無向グラフ
# G = nx.Graph()
# # # 有向グラフ
# # DG = nx.DiGraph()
# vlist = [1,2,3,4,5,6]
# elist = [(1,1), (1,2), (1,3), (2,4), (4,5), (5,6), (3,6)]
# G.add_nodes_from(vlist)
# G.add_edges_from(elist)
# nx.draw_networkx(G, node_color='lightgray', node_size=400)
# plt.axis('off')
# plt.show()

# print('Gの頂点のリスト:', G.nodes())
# print('Gの頂点の数:', G.number_of_nodes())
# print('Gの頂点1に隣接する頂点のリスト:', [v for v in nx.all_neighbors(G,1)])
#
# print('Gの枝のリスト', G.edges())
# print('Gの枝の数', G.number_of_edges())

# 無向グラフの隣接行列，接続行列
# G = nx.MultiGraph()
# G.add_edges_from([(1,2), (1,3), (3,1), (2,3), (2,2)])
# A = nx.adjacency_matrix(G)
# M = nx.incidence_matrix(G)
# print('A = ', A.toarray())
# print('M = ', M.toarray())
#
# 有向グラフの隣接行列，接続行列
# G2 = nx.MultiDiGraph()
# G2.add_edges_from([(1,2), (1,3), (3,1), (2,3), (2,2)])
# A2 = nx.adjacency_matrix(G2)
# M2 = nx.incidence_matrix(G2, oriented=True)
# print('A = ', A2.toarray())
# print('M = ', M2.toarray())
#
# 完全グラフの描画
# G = nx.complete_graph(5)
# p = nx.spring_layout(G, iterations=100)
# nx.draw_networkx(G, pos=p, node_color='lightgray', node_size=300)
# plt.axis('off')
# plt.show()

# 2部グラフ
# m = 3
# n = 4
# G = nx.complete_bipartite_graph(m,n)
# p = {}
# for i in range(m):
#     p[i] = (0,i)
# for j in range(n):
#     p[m+j] = (1,j)
# nx.draw_networkx(G, pos=p, node_color='lightgray', node_size=500)
# plt.axis('off')
# plt.show()

# 同型性のチェック
# G1 = nx.Graph()
# G1.add_edges_from([(1,4), (1,5), (1,6), (2,4), (2,5), (2,6), (3,4), (3,5), (4,6)])
#
# G2 = nx.Graph()
# G2.add_edges_from([('a','b'), ('a','d'), ('a','f'), ('b','c'), ('a','e'), ('c','d'), ('c','f'), ('d','e'), ('e','f')])
#
# G3 = nx.Graph()
# G3.add_edges_from([('x','z'), ('x','y'), ('y','z'), ('x','u'), ('y','v'), ('z','w'), ('u','v'), ('v','w'), ('w','u')])
#
# print(nx.is_isomorphic(G1,G2))
# print(nx.is_isomorphic(G1,G3))

# 連結性のチェック
G = nx.path_graph(4)
nx.add_path(G, [10, 11, 12])
print(nx.is_connected(G))
for c in nx.connected_components(G):
    print(c)
