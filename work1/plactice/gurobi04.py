# coding: utf-8
# Gurobiをインポート
from gurobipy import *

# 定数の定義
I,d = multidict({1:80, 2:270, 3:250, 4:160, 5:180})
J,M = multidict({1:500, 2:500, 3:500})
c = {(1,1):4,(2,1):5,(3,1):6,(4,1):8,(5,1):10,
    (1,2):6,(2,2):4,(3,2):3,(4,2):5,(5,2):8,
    (1,3):9,(2,3):7,(3,3):4,(4,3):3,(5,3):4,
    }

# モデルの定義
model = Model("transportation")

# 変数の定義
x = {}
for i in I:
    for j in J:
        x[i,j] = model.addVar(vtype="C",name="x(%s,%s)"%(i,j))

# モデルのアップデート
model.update()

# 制約式
for i in I:
    model.addConstr(quicksum(x[i,j] for j in J if (i,j) in x) == d[i], name="Demand(%s)"%i)
for j in J:
    model.addConstr(quicksum(x[i,j] for i in I if (i,j) in x) <= M[j], name="Capacity(%s)"%j)

# 目的関数
model.setObjective(quicksum(c[i,j]*x[i,j] for (i,j) in x), GRB.MINIMIZE)

# 最適化
model.optimize()

# 解の出力
print("Optimal calue:", model.ObjVal)
EPS = 1.e-6
for (i,j) in x:
    if x[i,j].X > EPS:
        print("sending quantity %10s from factory %3s to customer %3s"%(x[i,j].X, j, i))
