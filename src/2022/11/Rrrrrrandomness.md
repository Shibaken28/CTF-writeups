# ImaginaryCTF October 2022 Rrrrrrandomness

## 問題
線形合同法によって乱数列が生成される．
生成に使われるパラメータの$a,b,m$の和を求める問題．
ただし，線形合同法とは，次の漸化式と$x_0$によって計算される値である．

$$
x_{i+1} = ax_i + b \pmod m
$$

ただし，`rand`関数にはちょっと小細工が仕込まれていて，$x_i$の次に$x_{i+1}$が生成されるとは限らずに，ランダムに$1$個から$256$個の値がスキップされることがある．

```python
from Crypto.Util.number import getPrime
from secrets import randbelow
from hashlib import sha256

m = getPrime(20)
a = randbelow(m)
b = randbelow(m)
x = randbelow(m)

def rand():
    def rand():
        global a, b, m, x
        x = (a*x + b) % m
        return x
    while 1:
        for _ in range(rand() & 0xFF):
            rand()
        for _ in range(rand() & 0x8):
            yield rand()

def xor(x, y):
    return bytes(a ^ b for a, b in zip(x, y))

rand = rand()
rand = [next(rand) for _ in range(20)]
print('rand =', rand)

print('ct =', xor(b'ictf{REDACTED}', sha256((m + a + b).to_bytes(6, 'big')).digest()))
```

## 解説
線形合同法は，連続した乱数列から各パラメータを求めることができる．
次のような連続した乱数列が与えられたとする．
$$
\begin{align}
x_1 &= ax_0 + b \pmod m \\\\
x_2 &= ax_1 + b \pmod m \\\\
x_3 &= ax_2 + b \pmod m \\\\
x_4 &= ax_3 + b \pmod m \\\\
x_5 &= ax_4 + b \pmod m \\\\
x_6 &= ax_5 + b \pmod m
\end{align}
$$
$b$のみがわからない場合は，次のようにして求めることができる．
$$
\begin{align}
x_1 &= ax_0 + b \pmod m \\\\
b &= x_1 - ax_0 \pmod m
\end{align}
$$
$a,b$がわからない場合は，次のように逆数を用いてまず$a$を求めることができる(残りの$b$を求める方法はしました)．
$$
\begin{align}
x_2 - x_1 &= ax_1 - ax_0 \pmod m \\\\
x_2 - x_1 &= a(x_1 - x_0) \pmod m \\\\
a &= (x_2 - x_1)(x_1 - x_0)^{-1} \pmod m
\end{align}
$$

$a,b,m$全てわからない場合，次のような$T_0,T_1,T_2,\cdots$を用意する．

$$
\begin{align}
T_0 &= x_1 - x_0 \\\\
T_1 &= x_2 - x_1 = A(x_1-x_0) = A T_0 \pmod m \\\\
T_2 &= x_3 - x_2 = A(x_2-x_1) = A T_1 \pmod m \\\\
T_0T_2 - T_1^2 &= A^2T_0^2 - A^2T_0^2 = 0  \pmod m \\\\
\end{align}
$$

ここで，$T_0T_2 - T_1^2 = 0 \pmod m$であることから，添字をずらすと次が成り立つ．

$$
\begin{align}
T_1T_3 - T_2^2 &= 0  \pmod m \\\\
T_2T_4 - T_3^2 &= 0  \pmod m \\\\
T_3T_5 - T_4^2 &= 0  \pmod m \\\\
\vdots \\\\
T_{n-1}T_{n+2} - T_n^2 &= 0  \pmod m
\end{align}
$$
こられの数は全て$m$で割ったあまりが$0$であるため，これらの数の最大公約数を求めることができれば，それが$m$である可能性[^1]がある．

[^1]:あくまで可能性であり，いずれも同じ数になってしまうことや，$m$の倍数になってしまうことがある．最大公約数を取るときに使う数が多いければ多いほど$m$が求められる確率が高くなる．


以上のことにより，次のスクリプトによって$a,b,m$を求めることができる．

```python
from Crypto.Util.number import *
from hashlib import sha256

def linear_random_crack(rands):
    t = [rands[i+1]-rands[i]  for i in range(len(rands)-1) ]
    s = [(t[i+2]*t[i]-t[i+1]*t[i+1]) for i in range(len(t)-2) ]
    m = 0
    for a in s:
        m = GCD(m,a)
    a = ((t[2]-t[1]) * inverse(t[1]-t[0],m))%m
    b = (rands[1] - a*rands[0])%m
    return a,b,m

def xor(x, y):
    return bytes(a ^ b for a, b in zip(x, y))


ct = b'\x1b\xc3\xc1O\x7f]q\xb98\x8d\xb8\xf5\xec\x82\x8cg\xd0\xed\xbb\t<G\xe6\xde\xf7\xb3\x81\xe05'
r = [830740, 252348, 146586, 407799, 782171, 349709, 751088, 904092, 390201, 909918, 347514, 89924, 7112, 751221, 26415, 299902, 438982, 787802, 1081, 814607]
l = 8 # 必要に応じて小さくする
for i in range(len(r)-l):
    a,b,m = linear_random_crack(r[i:i+l])
    print(a,b,m)
    print(xor(ct,sha256((a+b+m).to_bytes(6, 'big')).digest()))
```

出力は次のようになる．
```none
963459 253883 977407
b'ictf{n07_50_r4nd0m_4ft3r_4ll}'
0 0 1
b'\x03\xa2\xe9\xf0\xf5\x10\x11Rs\xdc\xa8\xdf\x0e G\r\xdbm\xba\x10K\x1f\xc2^\xce\xe9\xc4\xa4a'
0 0 1
b'\x03\xa2\xe9\xf0\xf5\x10\x11Rs\xdc\xa8\xdf\x0e G\r\xdbm\xba\x10K\x1f\xc2^\xce\xe9\xc4\xa4a'
0 0 1
b'\x03\xa2\xe9\xf0\xf5\x10\x11Rs\xdc\xa8\xdf\x0e G\r\xdbm\xba\x10K\x1f\xc2^\xce\xe9\xc4\xa4a'
0 0 1
b'\x03\xa2\xe9\xf0\xf5\x10\x11Rs\xdc\xa8\xdf\x0e G\r\xdbm\xba\x10K\x1f\xc2^\xce\xe9\xc4\xa4a'
0 0 1
b'\x03\xa2\xe9\xf0\xf5\x10\x11Rs\xdc\xa8\xdf\x0e G\r\xdbm\xba\x10K\x1f\xc2^\xce\xe9\xc4\xa4a'
0 0 1
b'\x03\xa2\xe9\xf0\xf5\x10\x11Rs\xdc\xa8\xdf\x0e G\r\xdbm\xba\x10K\x1f\xc2^\xce\xe9\xc4\xa4a'
0 0 1
b'\x03\xa2\xe9\xf0\xf5\x10\x11Rs\xdc\xa8\xdf\x0e G\r\xdbm\xba\x10K\x1f\xc2^\xce\xe9\xc4\xa4a'
963459 253883 977407
b'ictf{n07_50_r4nd0m_4ft3r_4ll}'
0 0 1
b'\x03\xa2\xe9\xf0\xf5\x10\x11Rs\xdc\xa8\xdf\x0e G\r\xdbm\xba\x10K\x1f\xc2^\xce\xe9\xc4\xa4a'
0 0 1
b'\x03\xa2\xe9\xf0\xf5\x10\x11Rs\xdc\xa8\xdf\x0e G\r\xdbm\xba\x10K\x1f\xc2^\xce\xe9\xc4\xa4a'
0 0 1
b'\x03\xa2\xe9\xf0\xf5\x10\x11Rs\xdc\xa8\xdf\x0e G\r\xdbm\xba\x10K\x1f\xc2^\xce\xe9\xc4\xa4a'
```

# コメント
`yield`を知らなかった．

