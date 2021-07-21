# coding: utf-8
from gurobipy import *

def example():
    J,v = multidict({1:16, 2:19, 3:23, 4:28})
    a = {(1,1):2, (1,2):3, (1,3):4, (1,4):5,
         (2,1):3000, (2,2):3500, (2,3):5100, (2,4):7200
         }
    I,b = multidict({1:7, 2:10000})
    return I, J, v, a, b

def mkp(I, J, v, a, b):
    model = Model("mkp")
    x = {}
    for j in J:
        x[j] = model.addVar(vtype="B", name="x(%s)"%j)

    model.update()
    for i in I:
        model.addConstr(quicksum(a[i,j]*x[j] for j in J) <= b[i], "Capacity(%s)"%i)

    model.setObjective(quicksum(v[j]*x[j] for j in J), GRB.MAXIMIZE)

    model.update()
    return model

if __name__ == "__main__":
    I, J, v, a, b = example()
    model = mkp(I, J, v, a, b)

    model.update()
    #定式化が正しいかどうかのデバック
    model.write("mkp.lp")
    model.write('mkp.mps')

    model.Params.TimeLimit = 10
    print("-"*40)
    model.optimize()
    print("-"*40)
    print("Oprimal Value = ", model.ObjVal)

    if model.Status == GRB.OPTIMAL:
        EPS = 1.e-6
        for v in model.getVars():
            if v.X > EPS:
                print(v.VarName, v.X)
    elif model.Status == GRB.TIME_LIMIT:
        print("Time Over")
    else:
        print("Error")

