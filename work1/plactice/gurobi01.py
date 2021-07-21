# coding: utf-8
# gurobiをインポート
from gurobipy import *

# モデルの定義
model = Model("lo1")

# 変数の定義
x1 = model.addVar(vtype="C", name="x1")
x2 = model.addVar(vtype="C", name="x2")
x3 = model.addVar(lb=0, ub=30, vtype="C", name="x2")

# モデルのアップデート
model.update()

# 制約式
model.addConstr(2*x1 + x2 + x3 <= 60)
model.addConstr(x1 + 2*x2 + x3 <= 60)

# 目的関数
model.setObjective(15*x1 + 18*x2 + 30*x3, GRB.MAXIMIZE)

# 最適化問題を解く
model.optimize()

# 解の出力
print ("Opt. Value=", model.ObjVal)
for v in model.getVars():
    print (v.VarName, v.X)

