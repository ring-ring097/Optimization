# 多制約0-1ナップサック問題を解くclass定義
import numpy as np
import scipy.linalg as linalg
MEPS = 1.0e-10

class MultiKnapsackProblem(object):
    def __init__(self, name, caps, items, costs, subs, zeros=set(), ones=set()):
        self.name = name                      #問題の名前，文字列
        self.caps = caps                      #i番目の制約におけるナップサックの容量の辞書
        self.items = items                    #品物の集合
        self.costs = costs                            #品物jの価格,品物をキーとする辞書
        self.subs = subs                      #i種類の制約における品物jの重さ,品物をキーとする辞書を要素とする辞書
        self.zeros = zeros                    #ナップサックに入れない品物の集合
        self.ones = ones                      #ナップサックに入れない品物の集合
        self.lb = -100.0                      #問題の下界
        self.ub = -100.0                      #問題の上界
        ratio = {}
        for i in self.subs.keys():
            w = self.subs[i]
            for j in self.items:
                if w[j] == 0:
                    ratio[(i,j)] = 0
                else:
                    ratio[(i,j)] = self.costs[j] / w[j]

        self.sItemList = {}
        self.sItemList.update(sorted(ratio.items(), key=lambda x:x[1], reverse=True))
                                              #品物の価格の重さに対する比の大きい順に並べたもの
        #下界lbを達成する解
        self.xlb = {}
        for k in self.items:
            self.xlb[k] = 0.0
        #上界ubを達成する解
        self.xub = {}
        for k in self.items:
            self.xub[k] = 0.0

        self.bi_tmp = 1.0
        self.bi = None                        #ubを達成する解で，値が分数であるもの

    # 上界と下界を計算する関数
    def getbounds(self):
        # 下界の計算
        # 0-1で固定するものをあらかじめ設定
        # print("0-1固定考慮")
        for j in self.zeros:
            self.xlb[j] = self.xub[j] = 0.0
        for j in self.ones:
            self.xlb[j] = self.xub[j] = 1.0
        # 現在のアイテム数で容量オーバーになっていなければ終了
        for i in self.caps.keys():
            if self.caps[i] < sum(self.subs[i][j] for j in self.ones):
                self.lb = self.ub = -100.0
                return 0

        # 0-1を固定していないもので考え直す
        ritems = self.items - self.zeros - self.ones
        sItems = {}
        for k,v in self.sItemList.items():
            if k[1] in ritems:
                sItems[k] = v
        # 残り容量
        cap = {}
        for i in self.caps.keys():
            cap[i] = self.caps[i] - sum(self.subs[i][j] for j in self.ones)

        # 貪欲算法での計算
        List = []
        for k,v in sItems.items():
            if k[1] not in List:
                flag = 0
                for i in self.subs.keys():
                    if self.subs[i][k[1]] <= cap[i]:
                        pass
                    else:
                        flag = 1
                if flag == 0: 
                    for i in self.subs.keys():
                        cap[i] -= self.subs[i][k[1]]
                    self.xlb[k[1]] = 1.0
                    List.append(k[1])
                else:
                    pass
            else:
                pass


        # 線形緩和(シンプレックス法を用いる)
        def lp_RevisedSimplex(c,A,b):
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
                    for j in self.items:
                        if j in self.zeros:
                            self.xub[j] = 0.0
                        elif j in self.ones:
                            self.xub[j] = 1.0
                        else:
                            self.xub[j] = x[j-1]
                            xj_tmp = x[j-1]
                            # 分数の場合，0.5に近い値を優先的にbiに選ぶ
                            if xj_tmp != 0.0 and xj_tmp != 1.0:
                                self.bi = j
                                print("bi_v : ", xj_tmp)
                                print("bi : ", j)
                                # if self.bi == None:
                                #     self.bi = j
                                # elif abs(0.5-xj_tmp) < self.bi_tmp:
                                #     self.bi_tmp = abs(0.5-xj_tmp)
                                #     self.bi = j

                    break
                # そうでないとき，入る変数(s)を選ぶ
                else:
                    # s = np.argmax(cc)
                    # 候補の中で最も添字が小さいものを選ぶ
                    s = -100
                    ns = 0
                    for ss in cc:
                        if ss > MEPS:
                            s = ns
                            break
                        else:
                            pass
                        ns += 1
                    if s == -100:
                        print("erorr")

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
                    ratio[d<MEPS] = np.inf

                    # 出る変数（r）を選ぶ
                    r = np.argmin(ratio)

                    # minratio = np.inf
                    # minindex = np.inf
                    # for i in range(m):
                    #     if ratio[i]-minratio < -MEPS or (abs(ratio[i]-minratio) <= MEPS and basis[i] < minindex):
                    #         r = i
                    #         minratio = ratio[r]
                    #         minindex = basis[r]

                    # Step3
                    # 基底と非基底の入れ替え(ピボット演算)
                    nonbasis[s], basis[r] = basis[r], nonbasis[s]

        # 問題を決定する
        # 0-1固定されたアイテムを考慮する
        zeros_dic = {}
        ones_dic = {}
        for j in self.items:
            if j in self.zeros:
                zeros_dic[j] = 1
            else:
                zeros_dic[j] = 0
            if j in self.ones:
                ones_dic[j] = 1
            else:
                ones_dic[j] = 0
        
        # 係数行列
        a = []
        cost = []
        b = []
        for i in self.subs.keys():
            a1 = []
            Cap = self.caps[i]
            for j in self.subs[i].keys():
                if zeros_dic[j] == 1 or ones_dic[j] == 1:
                    if ones_dic[j] == 1:
                        Cap -= self.subs[i][j]
                    pass
                else:
                    a1.append(self.subs[i][j])
            a.append(a1)

            b.append(Cap)
        for j in self.items:
            if zeros_dic[j] == 1 or ones_dic[j] == 1:
                pass
            else:
                cost.append(self.costs[j])
                b.append(1.0)
                a2 = []
                for jj in self.items:
                    if jj in self.zeros or jj in self.ones:
                        pass
                    elif j == jj:
                        a2.append(1.0)
                    else:
                        a2.append(0.0)
                a.append(a2)

        # 制約の係数行列
        A = np.array(a)
        # コストベクトル
        Cost = np.array(cost)
        # 右側ベクトルを定義
        B = np.array(b)
        # print("A:",A)
        # print("Cost:",Cost)
        # print("B:",B)
        # 最適化実行
        lp_RevisedSimplex(Cost, A, B)


        # 上界と下界を計算
        self.lb = sum(self.costs[j]*self.xlb[j] for j in self.items)
        self.ub = sum(self.costs[j]*self.xub[j] for j in self.items)
