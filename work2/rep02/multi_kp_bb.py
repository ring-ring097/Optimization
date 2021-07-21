# レポート02  201911419 Tosa Rinto
import time
import sys
import fileinput
from pathlib import Path
from def_multi_kp_bb import *

# ナップサック問題を分枝限定法で解く関数
def MultiKnapsackProblemSolve(caps, items, costs, subs):
    from collections import deque
    queue = deque()
    # 元の問題を解く

    # print("入力")
    # print("caps : ", caps)
    # print("items : ", items)
    # print("costs : ", costs)
    # print("subs : ", subs)

    root = MultiKnapsackProblem("KP", caps = caps, items = items, costs = costs, subs = subs, zeros = set(), ones = set())

    # print("1回目")
    # print("関数内出力---------------------------------")
    root.getbounds()
    # 暫定の最適値と最適解を保存
    best = root
    # print("結果---------------------------------")
    # print("caps : ", best.caps)
    # print("items : ", best.items)
    # print("costs : ", best.costs)
    # print("subs : ", best.subs)
    # print("zeros : ", best.zeros.union({best.bi}))
    # print("ones : ", best.ones.union({best.bi}))
    # print("下界の最適解", best.xlb)
    # print("上界の最適解", best.xub)
    # print("下界値", best.lb)
    # print("上界値", best.ub)
    # print("分数値", best.bi)
    # print("-------------------------------------")
    # 解くべき問題のキューを作成
    queue.append(root)
    n = 0
    while queue != deque([]):
        # キューから問題を一つ選ぶ
        p = queue.popleft()
        # Pの上下界の計算
        n += 1
        # print("%d回目"%n)
        # print("関数内出力---------------------------------")
        p.getbounds()
        # print("---------------------------------------")
        # print("best: ", best.lb)
        # print("new_lb: ", p.lb)
        # print("new_ub: ", p.ub)
        # print("---------------------------------------")
        # print("結果---------------------------------")
        # print("caps : ", p.caps)
        # print("items : ", p.items)
        # print("costs : ", p.costs)
        # print("subs : ", p.subs)
        # print("zeros : ", p.zeros.union({p.bi}))
        # print("ones : ", p.ones.union({p.bi}))
        # print("zeros : ", p.zeros)
        # print("ones : ", p.ones)
        # print("下界の最適解", p.xlb)
        # print("下界値", p.lb)
        # print("上界の最適解" ,p.xub)
        # print("上界値", p.ub)
        # print("分数値", p.bi)
        # print("-------------------------------------")
        # もしPの上界が暫定の最適値を超えるなら計算を続行（超えなければそれが最適解）超えなければそれが最適解
        if p.ub > best.lb:
            # もしPの下界が暫定の最適値を上回るなら暫定の最適値を更新
            if p.lb > best.lb:
                best = p
            # もしPの上界がPの下界を上回るなら子問題を作って分枝(上界と下界が一致すれば終了)  
            if p.ub > p.lb:
                k = p.bi
                p1 = MultiKnapsackProblem(p.name + '+' + str(k),
                                     caps = p.caps, 
                                     items = p.items, 
                                     costs = p.costs, subs = p.subs, 
                                     zeros = p.zeros, ones = p.ones.union({k}))
                queue.append(p1)
                p2 = MultiKnapsackProblem(p.name + '-' + str(k),
                                     caps = p.caps, 
                                     items = p.items, 
                                     costs = p.costs, subs = p.subs, 
                                     zeros = p.zeros.union({k}), ones = p.ones)
                queue.append(p2)

    print("分枝回数%d回"%n)
    return 'Optimal', best.lb, best.xlb

# 時間計測
t1 = time.perf_counter()

# 問題設定
# 標準入力ファイルを数値リストに変換
if len(sys.argv) == 1:
    print('問題ファイルを指定してください')
elif len(sys.argv) > 2:
    print('指定できる問題ファイルは1つです')
elif Path(sys.argv[1]).exists():
    ARGV = []
    for line in fileinput.input():
        argv = list(map(float,line.split()))
        ARGV.append(argv)

    print(ARGV)
else:
    print("error")

# 数値リストを仕分け
print("入力--------------------------------------------------")
items = set()
j = 0
while j != ARGV[0][0]:
    j += 1
    items.add(j)
print("items : ", items)

subjects = set()
s = 0
while s != ARGV[0][1]:
    s += 1
    subjects.add(s)
print("subjects : ", subjects)

opt = ARGV[0][2]

costs = {}
for j in items:
    costs[j] = ARGV[1][j-1]
print("costs : ", costs)

subs = {}
for s in subjects:
    sub = {}
    for j in items:
        sub[j] = ARGV[s+1][j-1]
    subs[s] = sub
print("subs : ", subs)

caps = {}
for s in subjects:
    caps[s] = ARGV[len(subjects)+2][s-1]
print("caps : ", caps)

print("求める最適値 : ", opt)
print("実行--------------------------------------------------")
res = MultiKnapsackProblemSolve(caps = caps, items = items, costs = costs, subs = subs)

# 実行時間
t2 = time.perf_counter()
elapsed_time = t2 - t1
print("実行時間：", elapsed_time)

print('Optimal value = ', res[1])
print('Optimal solution = ', res[2])

