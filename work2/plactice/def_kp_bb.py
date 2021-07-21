# ナップサック問題を解くてためのクラス
class KnapsackProblem(object):
    def __init__(self, name, capacity, items, costs, weights, zeros=set(), ones=set()):
        self.name = name                      #問題の名前，文字列
        self.capacity = capacity              #ナップサックの容量
        self.items = items                    #品物の集合
        self.costs = costs                    #品物jの価格,品物をキーとする辞書
        self.weights = weights                #品物jの重さ,品物をキーとする辞書
        self.zeros = zeros                    #ナップサックに入れない品物の集合
        self.ones = ones                      #ナップサックに入れない品物の集合
        self.lb = -100                        #問題の下界
        self.ub = -100                        #問題の上界
        ratio = {j:costs[j]/weights[j] for j in items}
        self.sitemList = [k for k, v in sorted(ratio.items(), key=lambda x:x[1], reverse=True)]
                                              #品物の価格の重さに対する比の大きい順に並べたもの
        self.xlb = {j:0 for j in self.items}  #下界lbを達成する解
        self.xub = {j:0 for j in self.items}  #上界ubを達成する解
        self.bi = None                        #ubを達成する解で，値が分数であるもの

    # 上界と下界を計算する関数
    def getbounds(self):
        # ナップサックに入れない品物は解の集合において0の値を取る
        for j in self.zeros:
            self.xlb[j] = self.xub[j] = 0
        # ナップサックに入れる品物は解の集合において1の値を取る
        for j in self.ones:
            self.xlb[j] = self.xub[j] = 1
        # 現在のアイテム数で容量オーバーになっていれば終了
        if self.capacity < sum(self.weights[j] for j in self.ones):
            self.lb = self.ub = -100
            return 0

        # 入れるか入れないか決まっていない残りの品物をsitemsに格納
        ritems = self.items - self.zeros - self.ones
        sitems = [j for j in self.sitemList if j in ritems]
        # 残り容量
        cap = self.capacity - sum(self.weights[j] for j in self.ones)
        # 線形緩和
        for j in sitems:
            # もし残りアイテムの一つがまだ入るなる（容量オーバーにならないなら）入れる
            if self.weights[j] <= cap:
                cap -= self.weights[j]
                self.xlb[j] = self.xub[j] = 1
            # そうでなければ入るだけ分数にして入れる
            else:
                self.xub[j] = cap/self.weights[j]
                self.bi = j
                break
        # 上界と下界を計算
        self.lb = sum(self.costs[j]*self.xlb[j] for j in self.items)
        self.ub = sum(self.costs[j]*self.xub[j] for j in self.items)

    # ナップサック問題の情報を出力する関数
    def __str__(self):
        return('Name = ' + self.name + ',\n' + 
               'capacity = ' + str(self.capacity) + ',\n' + 
               'items = ' + str(self.items) + ',\n' +
               'costs = ' + str(self.costs) + ',\n' +
               'weights = ' + str(self.weights) + ',\n' +
               'zeros = ' + str(self.zeros) + ',\n' +
               'ones = ' + str(self.ones) + ',\n' +
               'lb = ' + str(self.lb) + ',\n' +
               'ub = ' + str(self.ub) + ',\n' +
               'bi = ' + str(self.bi) + ',\n')

