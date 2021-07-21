テストデータは case1 ~ case7 の7ケース

・解く問題

    Maximize
        sum{j=1,,,n} p(j)x(j)
    s.t.   
        sum{j=1,,,n} r(i,j)x(j) <= b(i)   i=1,,,,,m
        x(j) = 0 or 1

・入力フォーマット

    品物の数 n, 制約の数 m, 最適値 opt
    p(1),,,p(n)
    r(1,1),,,r(1,n)
    ...
    r(m,1),,,r(m,n)
    b(1),,,b(m)


case_all は case1 ~ case7 を縦に並べたもの