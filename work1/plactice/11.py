# coding: utf-8
from gurobipy import *
F, c, d = multidict({"CQPounder":[360,{"Cal":556, "Carbo":39, "Protein":30, "VitA":147, "VitC": 10, "Calc":221, "Iron":2.4}],
                     "Big Mac":[320,{"Cal":556, "Carbo":46, "Protein":26, "VitA":97, "VitC": 9, "Calc":142, "Iron":2.4}],
                     "FFilet":[270,{"Cal":356, "Carbo":42, "Protein":14, "VitA":28, "VitC": 1, "Calc":76, "Iron":0.7}],
                     "Chiken":[290,{"Cal":431, "Carbo":45, "Protein":20, "VitA":9, "VitC": 2, "Calc":37, "Iron":0.9}],
                     "Fries":[190,{"Cal":249, "Carbo":30, "Protein":3, "VitA":0, "VitC": 5, "Calc":7, "Iron":0.6}],
                     "Milk":[170,{"Cal":138, "Carbo":10, "Protein":7, "VitA":80, "VitC": 2, "Calc":227, "Iron":0}],
                     "VegJuice":[360,{"Cal":69, "Carbo":17, "Protein":1, "VitA":750, "VitC": 2, "Calc":18, "Iron":0}]
                     })
N, a, b = multidict({"Cal":[2000, 3000],
                     "Carbo":[300, 375],
                     "Protein":[50, 60],
                     "VitA":[500, 750],
                     "VitC":[85, 100],
                     "Calc":[660, 900],
                     "Iron":[6.0, 7.5]
                     })

model = Model("modern diet")
x = {}
for j in F:
    x[j] = model.addVar(vtype="I", name="x(%s)"%j)

model.update()

for i in N:
    model.addConstr(quicksum(d[j][i]*x[j] for j in F) >= a[i], "NutrLB(%s)"%i)
    model.addConstr(quicksum(d[j][i]*x[j] for j in F) <= b[i], "NutrUB(%s)"%i)

model.setObjective(quicksum(c[j]*x[j] for j in F), GRB.MINIMIZE)

print("-"*40)
model.optimize()
print("-"*40)

status = model.Status
if status == GRB.OPTIMAL:
    print("Optimal Value = ", model.ObjVal)
    for j in x:
        if x[j].X > 0:
            print(j,x[j].X)
if status == GRB.UNBOUNDED or status == GRB.INF_OR_UNBD:
    model.setObjective(0, GRB.MAXIMIZE)
    print("~"*40)
    model.optimize()
    print("~"*40)
    status == model.Status
    if status == GRB.OPTIMAL:
        print("Instance unbounded")
    elif status == GRB.INFEASIBLE:
        print("Infeasible")
    else:
        print("error")

model.computeIIS()
for c in model.getConstrs():
    if c.IISConstr:
        print(c.ConstrName)

model.feasRelaxS(1, True, False, True)
print("."*40)
model.optimize()
print("."*40)
status = model.Status
if status == GRB.Status.OPTIMAL:
    print("Opt.Value = ", model.ObjVal)
    for v in model.getVars():
        print(v.VarName, v.X)
