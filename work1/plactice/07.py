# coding: utf-8
from gurobipy import *

a = []
I = 5

for i in range(0,I):
    a.append(i)

print(a)

#
# a = {(1,1):0.25,(1,2):0.15,(1,3):0.30,
#      (2,1):0.30,(2,2):0.30,(2,3):0.10,
#      (3,1):0.15,(3,2):0.65,(3,3):0.05,
#      (4,1):0.10,(4,2):0.05,(4,3):0.85
#      }
#
# I,p = multidict({1:5, 2:6, 3:8, 4:20})
# K,LB,UB = multidict({1:[.2,.2], 2:[.0,.35], 3:[.45,1.0]})
#
# model = Model("mix")
#
# x = {}
# for i in I:
#     x[i] = model.addVar(lb=0.00, ub=1.00, vtype="C", name="x[%s]"%i)
#
# model.update()
#
# model.addConstr(quicksum(x[i] for i in I) == 1)
#
# for k in K:
#     model.addConstr(quicksum(a[i,k]*x[i] for i in I) >= LB[k])
#     model.addConstr(quicksum(a[i,k]*x[i] for i in I) <= UB[k])
#
# model.setObjective(quicksum(p[i]*x[i] for i in I), GRB.MINIMIZE)
#
# model.Params.TimeLimit = 10
# model.optimize()
# if model.Status == GRB.OPTIMAL:
#     print("Optimal value:", model.Objval)
#     for i in I:
#         print("x[%s]:"%i, x[i].X)
# elif model.Status == GRB.TIME_LIMIT:
#     print("Time Over")
# else:
#     print("error!")

