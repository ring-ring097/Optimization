from def_kp_bb import *

# ナップサック問題を分枝限定法で解く関数
def KnapsackProblemSolve(capacity, items, costs, weights):
    from collections import deque
    queue = deque()
    # 元の問題を解く
    root = KnapsackProblem('KP', 
                           capacity = capacity, 
                           items = items, 
                           costs = costs, weights = weights, 
                           zeros= set(), ones = set()
                           )
    root.getbounds()
    # 暫定の最適値と最適解を保存
    best = root
    # 解くべき問題のキューを作成
    queue.append(root)
    while queue != deque([]):
        # キューから問題を一つ選ぶ
        p = queue.popleft()
        # Pの上下界の計算
        p.getbounds()
        # もしPの上界が暫定の最適値を超えるなら計算を続行（超えなければそれが最適解）超えなければそれが最適解
        if p.ub > best.lb:
            # もしPの下界が暫定の最適値を上回るなら暫定の最適値を更新
            if p.lb > best.lb:
                best = p
            # もしPの上界がPの下界を上回るなら子問題を作って分枝(上界と下界が一致すれば終了)  
            if p.ub > p.lb:
                k = p.bi
                print(k)
                p1 = KnapsackProblem(p.name + '+' + str(k),
                                     capacity = p.capacity, 
                                     items = p.items, 
                                     costs = p.costs, weights = p.weights, 
                                     zeros= p.zeros, ones = p.ones.union({k})
                                    )
                queue.append(p1)
                p2 = KnapsackProblem(p.name + '-' + str(k),
                                     capacity = p.capacity, 
                                     items = p.items, 
                                     costs = p.costs, weights = p.weights, 
                                     zeros= p.zeros.union({k}), ones = p.ones
                                    )
                queue.append(p2)
    return 'Optimal', best.lb, best.xlb

# 問題の定義
capacity = 15
items = {1, 2, 3, 4, 5}
c = {1:50, 2:40, 3:10, 4:70, 5:55}
w = {1:7, 2:5, 3:1, 4:9, 5:6}

res = KnapsackProblemSolve(capacity = capacity, items = items, costs = c, weights = w)
print('Optimal value = ', res[1])
print('Optimal solution = ', res[2])
