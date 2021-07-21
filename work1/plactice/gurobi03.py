# coding: utf-8

from gurobipy import *

model = Model("turukametako")
x = model.addVar(lb=0,vtype="I", name="x")
y = model.addVar(lb=0,vtype="I", name="y")
z = model.addVar(lb=0,vtype="I", name="z")
model.update()
model.addConstr(x + y + z  == 32)
model.addConstr(2*x + 4*y + 8*z == 80)
model.setObjective(y + z , GRB.MINIMIZE)
model.optimize()
print("Opt.Value=", model.ObjVal)
print("(x,y,z)=", (x.X, y.X, z.X))
