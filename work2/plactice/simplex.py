import numpy as np
import scipy.linalg as linalg
MEPS = 1.0e-10

items = {1,2,3,4}


def lp_RevisedSimplex(c,A,b):
    np.seterr(divide='ignore')
    # m行n列の行列を定義
    (m,n) = A.shape 
    # Aの後ろに単位行列をくっつける（スラック変数を入れるため）
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
            print('Optimal value = ', np.dot(c0[basis], x[basis]))
            for i in items:
                i -= 1
                print('x', i, '=', x[i])
            print("x:", x)
            break
        # そうでないとき，出る変数(s)を選ぶ
        else:
            s = np.argmax(cc)

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
# コストベクトル
c = np.array([16,19,23,28])
# 右側ベクトルを定義
b = np.array([7,10000,1,1,1,1])

print("入力-----------------------------")
print("A:",A)
print("Cost:",c)
print("B:",b)
# 係数行列
A = np.array([[2,2,-1],[2,-2,3],[0,2,-1]])
# コストベクトル
c = np.array([4, 3, 5])
# 右側ベクトル
b = np.array([6,8,4])


# 最適化実行
lp_RevisedSimplex(c, A, b)
