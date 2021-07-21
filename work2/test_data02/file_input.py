import sys
import fileinput
from pathlib import Path

# 標準入力ファイルを数値リストに変換
if len(sys.argv) == 1:
    print('問題ファイルを指定してください')
elif len(sys.argv) > 2:
    print('指定できる問題ファイルは1つです')
elif Path(sys.argv[1]).exists():
    ARGV = []
    for line in fileinput.input():
        argv = list(map(int, line.split()))
        ARGV.append(argv)

    print(ARGV)
else:
    print("error")

# 数値リストを仕分け
items = set()
j = 0
while j != ARGV[0][0]:
    j += 1
    items.add(j)
print("items : ", items)

subjects = set()
s = 0
while s != ARGV[0][1]:
    s += 1
    subjects.add(s)
print("subjects : ", subjects)

opt = ARGV[0][2]

costs = {}
for j in items:
    costs[j] = ARGV[1][j-1]
print("costs : ", costs)

subs = {}
for s in subjects:
    sub = {}
    for j in items:
        sub[j] = ARGV[s+1][j-1]
    subs[s] = sub
print("subs : ", subs)

caps = {}
for s in subjects:
    caps[s] = ARGV[len(subjects)+2][s-1]
print("caps : ", caps)

print("opt : ", opt)


