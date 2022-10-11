# 合同式基本
## 合同式
割り算における剰余，すなわち割ったあまりについての演算である．
例えば，$9$を$5$で割ったあまりは$4$である．また，$14$を$5$で割ったあまりも$4$である．このことを合同式で表すと次のようにかける．
$$
9 \equiv 14 \pmod 5
$$
記号として$\equiv$を使っている．図形の合同を表すときと同じ記号である．$=$ではない．
読み方はいろいろあり，次のように読む．
- $9$と$14$は$5$を法として合同
- $9$合同$14$モッド$5$

$\textrm{mod}$を「モッド」と読んだり「モジュロ」(modはmoduloの略)と読んだり，「モッド」の小さいツが省略されて「モド」になったり，様々である．

## 性質

次の条件が成り立つとき，
$$
a\equiv c \pmod m \\\\
b\equiv d \pmod m
$$
次の式が成立する．
$$
a + b \equiv c + d \pmod m \\\\
a - b \equiv c - d \pmod m \\\\
ab \equiv cd \pmod m
$$

整数$k,l$を使って$a,b$は$a=km+c,b=lm+d$と表して，各値を計算すると証明ができる．
$$
a + b = (km+c) + (lm+d) = (k+l)m + (c+d) \\\\
a - b = (km+c) - (lm+d) = (k-l)m + (c-d) \\\\
ab = (km+c)(lm+d) = klm^2 + kmd + lcm + cd = m(klm+kd+lc) + cd
$$

また，$ab \equiv cd \pmod m$で，$a=b,c=d$とすると，$a^2 \equiv c^2 \pmod m$が成り立つ．さらにこれを繰り返すと次が成り立つ．
$$
xを正の整数とすると，a^x \equiv c^x \pmod m 
$$


## 例
- $3 \equiv 8 \pmod 5$
- $19 \equiv 13 \pmod 6$
- $-3 \equiv 2 \pmod 5$
- $21 + 11 \equiv 1 + 1 \equiv 2 \equiv 0 \pmod 2$
- $13 \times 9 \equiv 0 \times 9 \equiv 0 \pmod{13}$
- $3^{100} \equiv 1^{100 }\equiv 1\pmod 2$

