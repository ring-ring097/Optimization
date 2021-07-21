# 多制約0-1ナップサック問題の下界を求める

items = {1,2,3,4}
c = {1:16, 2:19, 3:23, 4:28}
w1 = {1:2, 2:3, 3:4, 4:5}
w2 = {1:3000, 2:3500, 3:5100, 4:7200}
subs = {1:w1, 2:w2}
capacity1 = 7
capacity2 = 10000
caps = {1:capacity1, 2:capacity2}

ratio = {}
for i in subs.keys():
    w = subs[i]
    for j in items:
        ratio[(i,j)] = c[j] / w[j]

sItems = {}
sItems.update(sorted(ratio.items(), key=lambda x:x[1], reverse=True))

# 実行
# 品物とそれを入れるか入れないかの情報を持つ辞書
x = {}
for j in items:
    x[j] = 0

# すでに入れたものの情報を保持するリスト
List = []
for k,v in sItems.items():
    # K = str(k)
    # V1 = str(subs[1][k[1]]) 
    # V2 = str(subs[2][k[1]])
    # print("%s,%s,%s"%(K,V1,V2))
    if k[1] not in List:
        # print("キャパ1", caps[1])
        # print("キャパ2", caps[2])
        if subs[1][k[1]] <= caps[1] and subs[2][k[1]] <= caps[2]:
            caps[1] -= subs[1][k[1]]
            caps[2] -= subs[2][k[1]]
            # print("%dを追加"%k[1])
            # print("残りキャパ1", caps[1])
            # print("残りキャパ2", caps[2])
            x[k[1]] = 1
            List.append(k[1])
        else:
            # print("%dは追加できない"%k[1])
    else:
    #     print("%dはすでに追加済み"%k[1])
    # print("~~~~~~~~~~~~~~~~~~")
        
print("品物とそれを入れるか入れないかの情報")
print(x)

print("下界：", sum(c[j]*x[j] for j in items))

