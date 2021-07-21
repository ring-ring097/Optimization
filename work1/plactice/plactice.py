# coding: utf-8
from gurobipy import *

model = Model("sample")
x = model.addVar(lb=0, ub=3, vtype="C")
y = model.addVar(lb=0, ub=5, vtype="C")
model.update()
model.addConstr(x + y <= 4)
model.addConstr(x + 2*y <= 6)
model.setObjective(2*x + y, GRB.MAXMIZE)
model.optimize()

# 解を求める計算
print("↓点線の間に、Gurobi Optimizerからログが出力")
print("-" * 40)

model_1.optimize()

print("-" * 40)
print()


# 最適解が得られた場合、結果を出力
if model.Status == GRB.OPTIMAL:
    # 解の値
    x_opt = x.X
    y_opt = y.X
    # 目的関数の値
    val_opt = model_1.ObjVal
    print(f"最適解は x = {x_opt}, y = {y_opt}")
    print(f"最適値は {val_opt}")
