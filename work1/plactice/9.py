# coding: utf-8
from gurobipy import *

LB = 0.0
UB = 1.0
EPS = 0.01

while 1:
    theta = (UB + LB)/2
    model = Model("fractional_2")
    x = model.addVar(vtype="I")
    y = model.addVar(vtype="I")
    z = model.addVar(vtype="I")
    model.update()
    model.addConstr(x + y + z == 32)
    model.addConstr(2*x + 4*y + 8*z == 80)
    model.addConstr((2*theta - 1)*x - (4*theta - 1)*y >= 0)
    model.setObjective(x + y + z, GRB.MINIMIZE)
    print("-" * 40)
    model.optimize()
    print("-" * 40)
    if model.Status == GRB.OPTIMAL:
        UB = theta
        if UB - LB <= EPS:
            break
    else:
        LB = theta

print("theta : ", theta)
print("(x,y,z) = ", x.X, y.X, z.X)

