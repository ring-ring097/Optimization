import matplotlib.pyplot as plt
import networkx as nx

# 3*3のグリッドを作成
GR = nx.grid_2d_graph(3,3)
#奇点を二つ追加
GR.add_edges_from([((0,1), (1,2))])
nx.draw_networkx(GR, 
                 pos={v:v for v in GR.nodes()}, 
                 node_color='lightgray', 
                 node_size=1200, 
                 with_labels=True)
plt.axis('off')
plt.show()
print(nx.is_eulerian(GR))

#奇点をさらに二つ追加
GR.add_edges_from([((1,0), (2,1))])
nx.draw_networkx(GR, 
                 pos={v:v for v in GR.nodes()}, 
                 node_color='lightgray', 
                 node_size=1200, 
                 with_labels=True)
plt.axis('off')
plt.show()
print(nx.is_eulerian(GR))

# オイラー閉路を構築する関数
ee = nx.eulerian_circuit(GR)
for (i,j) in ee:
    print(i, end='=>')
print("")
