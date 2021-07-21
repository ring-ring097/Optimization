import numpy as np
import scipy.linalg as linalg
MEPS = 1.0e-10

# 線形緩和(シンプレックス法を用いる)
def lp_RevisedSimplex(c,A,b,zeros,ones):
    # 0-1固定されたアイテムを考慮する
    np.seterr(divide='ignore')
    # m行n列の行列を定義
    (m,n) = A.shape 
    # aの後ろに単位行列をくっつける（スラック変数を入れるため）
    AI = np.hstack((A, np.identity(m)))
    # 目的関数の係数ベクトル
    c0 = np.r_[c, np.zeros(m)]
    # 基底変数の添字群
    basis = [n+i for i in range(m)]
    # 非基底変数の添字群
    nonbasis = [j for j in range(n)]
    xub = {}

    while True:
        # Step1
        # 双対変数yについて解く
        y = linalg.solve(AI[:, basis].T, c0[basis])
        # 被約費用ベクトルの計算
        cc = c0[nonbasis] - np.dot(y, AI[:, nonbasis])

        # 最適性判定
        # 被約費用ベクトルが0以下（十分に小さいとき）(x_B,x_N)=(A^{-1}_Bb,0)が最適基底解
        if np.all(cc <= MEPS):
            x = np.zeros(n+m)
            x[basis] = linalg.solve(AI[:,basis], b)
            print('Optimal value = ', np.dot(c0[basis], x[basis]))
            for j in items:
                if j in zeros:
                    xub[j] = 0.0
                elif j in ones:
                    xub[j] = 1.0
                else:
                    xub[j] = x[j-1]
            print(xub)
            break
        # そうでないとき，入る変数(s)を選ぶ
        else:
            # s = np.argmax(cc)
            # 候補の中で最も添字が小さいものを選ぶ
            s = -100
            ns = 0
            for ss in cc:
                if ss > 0:
                    s = ns
                    break
                else:
                    pass
                ns += 1
            if s == -100:
                print("入る変数の候補がありません")
            

        # Step2
        # A_Bd = A_sをdについて解く
        d = linalg.solve(AI[:,basis], AI[:,nonbasis[s]])

        # 非有界性の判定
        # もしd<=0ならば問題は非有界で終了
        if np.all(d <= MEPS):
            print('Unbounded')
            break
        # そうでないならば，A_Bb- = bをb-について解き，
        else:
            bb = linalg.solve(AI[:,basis], b)
            ratio = bb/d
            ratio[ratio<-MEPS] = np.inf 

            # 出る変数（r）を選ぶ
            r = np.argmin(ratio)

            # Step3
            # 基底と非基底の入れ替え(ピボット演算)
            nonbasis[s], basis[r] = basis[r], nonbasis[s]



# 問題を決定する
items = {1,2,3,4}
costs = {1:16, 2:19, 3:23, 4:28}
subs = {1:{1:2, 2:3, 3:4, 4:5}, 2:{1:3000, 2:3500, 3:5100, 4:7200}}
caps = {1:7, 2:10000}

print("入力-----------------------------")
print("items :", items)
print("costs : ", costs)
print("subs : ", subs )
print("caps : ", caps)
# items = {1,2,3,4,5,6}
# costs = {1:100, 2:600, 3:1200, 4:2400, 5:500, 6:2000}
# subs = {1:{1:8, 2:12, 3:13, 4:64, 5:22, 6:41}, 2:{1:8, 2:12, 3:13, 4:75, 5:22, 6:41}, 3:{1:3, 2:6, 3:4, 4:18, 5:6, 6:4}, 4:{1:5, 2:10, 3:8, 4:32, 5:6, 6:12}, 5:{1:5, 2:13, 3:8, 4:42, 5:6, 6:20}, 6:{1:5, 2:13, 3:8, 4:48, 5:6, 6:20}, 7:{1:0, 2:0, 3:0, 4:0, 5:8, 6:0}, 8:{1:3, 2:0, 3:4, 4:0, 5:8, 6:0}, 9:{1:3, 2:2, 3:4, 4:0, 5:8, 6:4}, 10:{1:3, 2:2, 3:4, 4:8, 5:8, 6:4}}
# caps = {1:80, 2:96, 3:20, 4:36, 5:44, 6:48, 7:10, 8:18, 9:22, 10:24}

# 0-1固定されたアイテムを考慮する
zeros = {}
ones = {}
zeros_dic = {}
ones_dic = {}
for j in items:
    if j in zeros:
        zeros_dic[j] = 1
    else:
        zeros_dic[j] = 0
    if j in ones:
        ones_dic[j] = 1
    else:
        ones_dic[j] = 0

print("zeros : ", zeros_dic)
print("ones : ", ones_dic)

# 係数行列
a = []
cost = []
b = []
for i in subs.keys():
    a1 = []
    print("i = %d"%i)
    Cap = caps[i]
    print("cap = %d"%caps[i])
    for j in subs[i].keys():
        if zeros_dic[j] == 1 or ones_dic[j] == 1:
            if ones_dic[j] == 1:
                Cap -= subs[i][j]
        else:
            a1.append(subs[i][j])
    a.append(a1)
    b.append(Cap)
print("b : ", b)

for j in items:
    if zeros_dic[j] == 1 or ones_dic[j] == 1:
        pass
    else:
        cost.append(costs[j])
        b.append(1.0)
        a2 = []
        for jj in items:
            if jj in zeros or jj in ones:
                pass
            elif j == jj:
                a2.append(1.0)
            else:
                a2.append(0.0)
        a.append(a2)

A = np.array(a)
# コストベクトル
Cost = np.array(cost)
# 右側ベクトルを定義
B = np.array(b)
print("実際に解く問題-----------------------------")
print("A:",A)
print("Cost:",Cost)
print("B:",B)
print("実行-----------------------------")
lp_RevisedSimplex(Cost, A, B, zeros, ones)


