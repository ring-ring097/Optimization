# coding: utf-8
from gurobipy import *

model = Model("fraction")

x = model.addVar(lb=0,vtype="C",name="x\'")
y = model.addVar(lb=0,vtype="C",name="y\'")
z = model.addVar(lb=0,vtype="C",name="z\'")
t = model.addVar(lb=0,vtype="C",name="t\'")

model.addConstr(2*x + 4*y == 1)
model.addConstr(x + y + z == 32*t)
model.addConstr(2*x + 4*y + 8*z == 80*t)

model.update()

model.setObjective(x+y, GRB.MINIMIZE)

model.Params.TimeLimit = 10
model.optimize()

if model.Status == GRB.OPTIMAL:
    print("succeed")
    print("Opt.Val. = ", model.ObjVal)
    print("t = ", t.X)
    print("(x,y,z) = ", x.X/t.X, y.X/t.X, z.X/t.X)
elif model.Status == GRB.TIME_LIMIT:
    print("Time Over")
else:
    print("error")

