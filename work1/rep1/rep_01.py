# codingk: utf-8
from gurobipy import *

# 定義 ---------------------------------------------------------------------------------------------
# 美術館全体
class Museum:
    def __init__(self, I, J):
        self.I = I
        self.J = J
        self.room = []
        for i in range(0,I):
            sublist = []
            for j in range(0,J):
                sublist.append(Area)
            self.room.append(sublist)

# 美術館の1エリア（1マス）
class Area(Museum):
    def __init__(self):
        self.label = "hallway"
        self.prop = None

# 問題を設定する関数
def addRequirements(i, j, num, museum):
    museum.room[i-1][j-1].label = "wall"
    museum.room[i-1][j-1].prop = num

# 壁に接するエリアのライトの数を調べる関数
def getAroundLights(i ,j, museum):
    n = []
    if i-1 >= 0 and museum.room[i-1][j].label == "hallway":
        n.append(museum.room[i-1][j].prop)
    if i+1 < museum.I and museum.room[i+1][j].label == "hallway":
        n.append(museum.room[i+1][j].prop)
    if j-1 >= 0 and museum.room[i][j-1].label == "hallway":
        n.append(museum.room[i][j-1].prop)
    if j+1 < museum.I and museum.room[i][j+1].label == "hallway":
        n.append(museum.room[i][j+1].prop)
    return quicksum(n)
    
# 行を見て壁までにあるライトを数える関数
def getVLightsIlluminated(i, j, museum):
    mV = []
    k1 = j
    k2 = j
    mV.append(museum.room[i][k1].prop)
    while k1 > 0:
        k1 -= 1
        if museum.room[i][k1].label == "hallway":
            mV.append(museum.room[i][k1].prop)
        else:
            break
    while k2 < museum.J - 1:
        k2 += 1
        if museum.room[i][k2].label == "hallway":
            mV.append(museum.room[i][k2].prop)
        else:
            break
    return mV

# 列を見て壁までにあるライトを数える関数
def getHLightsIlluminated(i, j, museum):
    mH = []
    k3 = i
    k4 = i
    mH.append(museum.room[k3][j].prop)
    while k3 > 0:
        k3 -= 1
        if museum.room[k3][j].label == "hallway":
            mH.append(museum.room[k3][j].prop)
        else:
            break
    while k4 < museum.I - 1:
        k4 += 1
        if museum.room[k4][j].label == "hallway":
            mH.append(museum.room[k4][j].prop)
        else:
            break
    return mH

# 最適化 ---------------------------------------------------------------------------------------------
model = Model("Museum Puzzle")

# museumのインスタンス化
museum = Museum(10, 10)

# roomの初期化
for i in range(0,museum.I):
    for j in range(0,museum.J):
        museum.room[i][j] = Area()

# 問題の定義
addRequirements(1,1,0,museum)
addRequirements(1,5,None,museum)
addRequirements(1,6,0,museum)
addRequirements(1,7,0,museum)
addRequirements(1,8,0,museum)
addRequirements(1,9,0,museum)
addRequirements(1,10,None,museum)
addRequirements(2,5,None,museum)
addRequirements(2,10,None,museum)
addRequirements(4,10,1,museum)
addRequirements(6,4,2,museum)
addRequirements(7,5,1,museum)
addRequirements(7,7,1,museum)
addRequirements(7,9,None,museum)
addRequirements(8,3,2,museum)
addRequirements(8,6,None,museum)
addRequirements(8,8,0,museum)
addRequirements(10,4,2,museum)

# 変数の作成
for i in range(0,museum.I):
    for j in range(0,museum.J):
        if museum.room[i][j].label == "hallway":
            museum.room[i][j].prop = model.addVar(vtype="B", name="x(%s,%s)"%(i+1,j+1))
        else:
            pass

model.update()


# 制約
for i in range(0,museum.I):
    for j in range(0,museum.J):

        # 壁の制約
        if museum.room[i][j].label == "wall":
            if museum.room[i][j].prop == None:
                pass
            else:
                # 壁に接するエリアには数字の数だけライトをおく
                model.addConstr(museum.room[i][j].prop == getAroundLights(i,j,museum), "wall(%s,%s)_constraint"%(i+1,j+1))

        # ライトの制約
        elif museum.room[i][j].label == "hallway":
            # ライトはライトで照らさない(行)
            model.addConstr(quicksum(getVLightsIlluminated(i,j,museum)) <= 1, "light(%s,%s)_constraint_1"%(i+1,j+1))
            # ライトはライトで照らさない(列)
            model.addConstr(quicksum(getHLightsIlluminated(i,j,museum)) <= 1, "light(%s,%s)_constraint_2"%(i+1,j+1))
            # 廊下の制約（どの廊下も照らされる）
            model.addConstr(
                quicksum(getVLightsIlluminated(i,j,museum)) + quicksum(getHLightsIlluminated(i,j,museum)) - museum.room[i][j].prop >= 1,
                "hallway(%s,%s)_constraint"%(i+1,j+1)
            )


# 目的関数：ライトの数を最小にする
model.setObjective(quicksum(model.getVars()), GRB.MINIMIZE)

model.update()
model.write("puzzle.lp")

# 処理時間は最長10秒
model.Params.TimeLimit == 10
print("-"*40)
model.optimize()
print("-"*40)

if model.Status == GRB.OPTIMAL:
    print("Optimal value:", model.Objval)
    for i in range(0,museum.I):
        for j in range(0,museum.J):
            if museum.room[i][j].label == "wall":
                if museum.room[i][j].prop == 0:
                    print("0️⃣ ", end=",")
                elif museum.room[i][j].prop == 1:
                    print("1️⃣ ", end=",")
                elif museum.room[i][j].prop == 2:
                    print("2️⃣ ", end=",")
                elif museum.room[i][j].prop == 3:
                    print("3️⃣ ", end=",")
                elif museum.room[i][j].prop == 4:
                    print("4️⃣ ", end=",")
                else:
                    print("◻️ ", end=",")
            elif museum.room[i][j].label == "hallway":
                if math.floor(museum.room[i][j].prop.X) == 0:
                    print("　", end=",")
                else:
                    print("⭕️", end=",")
        print("")
elif model.Status == GRB.TIME_LIMIT:
    print("Time Over")
elif model.Status == GRB.UNBOUNDED:
    print("Instance unbounded")
elif model.Status == GRB.INFEASIBLE:
    print("Infeasible")
else:
    print("error!")

