# ImaginaryCTF October 2022 Luggage


## 問題
ランダムにフラグのビット数と同じ長さの`pub`がランダム生成され，フラグの`i`番目のビットが`1`だったところに対応する`pub[i]`が足し算されて`c`となる．`c`と`pub`が与えられる．要するに[ナップザック問題](https://ja.wikipedia.org/wiki/%E3%83%8A%E3%83%83%E3%83%97%E3%82%B5%E3%83%83%E3%82%AF%E5%95%8F%E9%A1%8C)．

```python
from Crypto.Util.number import bytes_to_long, getPrime
from Crypto.Random.random import getrandbits

flag = b"ictf{xxxxxxxxxxxxxxxxxxxxxxx}"
flag = bytes_to_long(flag)

p = getPrime(512)
k = [getrandbits(n*2+3) for n in range(flag.bit_length())]
assert all(n < p for n in k)

e = getrandbits(1024)
pub = [(m * e) % p for m in k]
print(pub)

c = []
for n in range(flag.bit_length()):
  c.append((flag % 2) * pub[n])
  flag //= 2

print(f"{pub}")
print(f"{sum(c)}")
```

## 解法
ナップザック問題を解くにはLLLを使う．

<details>
<summary>LLLの簡単な説明</summary>

格子の作り方は次の通り．

$$
\begin{pmatrix}
1 & 0 & 0 & \cdots & 0 & 0 & 0 & p_1\\\\
0 & 1 & 0 & \cdots & 0 & 0 & 0 & p_2 \\\\
0 & 0 & 1 & \cdots & 0 & 0 & 0 & p_3 \\\\
\vdots & \vdots & \vdots & \ddots & \vdots & \vdots & \vdots \\\\
0 & 0 & 0 & \cdots & 1 & 0 & 0 & p_{n-2} \\\\
0 & 0 & 0 & \cdots & 0 & 1 & 0 & p_{n-1}\\\\
0 & 0 & 0 & \cdots & 0 & 0 & 1 & p_{n}\\\\
0 & 0 & 0 & \cdots & 0 & 0 & 0 & -c\\\\
\end{pmatrix}
$$

例えば，$p=(102,103,104)$からいくつか選んで$c=206$を作る組み合わせを知りたい場合，

$$
\begin{pmatrix}
1 & 0 & 0 & 102 \\\\
0 & 1 & 0 & 103 \\\\
0 & 0 & 1 & 104 \\\\
0 & 0 & 0 & -206 \\\\
\end{pmatrix}
$$

をLLLにかける．

```
sage: X = Matrix(ZZ,4,4)                 
sage: X[0,0]=1                           
sage: X[1,1]=1                           
sage: X[2,2]=1                           
sage: X[0,3]=102                         
sage: X[1,3]=103                         
sage: X[1,3]=104                         
sage: X[3,3]=-206 
sage: X
[   1    0    0  102]
[   0    1    0  103]
[   0    0    1  104]
[   0    0    0 -206]
sage: X.LLL()
[  1   0   1   0]
[ -1   1   0   1]
[  0  -1   1   1]
[ 35   0 -34  34]
```
LLLは各行をそれぞれベクトルと見たとき，それらのベクトルの適当な整数倍したものがゼロベクトルに近いように計算してくれる．
LLLにかける前の行列で，一番右の列以外の$1,0$は，どのベクトルがいくつ足し算されたかを表すために用意されている．
この場合，結果の$1$行目がもとの行列の$1,3,4$行目のベクトルを足し算したものになっている．すなわち，$102+104-206=0$であることがわかる．

</details>

`c`が計算されるときに`flag`の下位ビットから処理されていることに注意して実装する．なお，出力されたベクトルの最終列は無視するべきだが，$0$であるはずなので反転したときに結局関係なくなる(桁の先頭に$0$が入るだけ)ので問題ない．

```python
from Crypto.Util.number import *

n = len(pub)
X = Matrix(ZZ, n+1, n+1)

for i,p in enumerate(pub):
    X[i,i] = 1
    X[i,n] = p

X[n,n] = -c

out = Matrix(X).LLL()

for row in out:
    if all(n in [0, 1] for n in row):
        print(row)
        flag = int("".join(str(n) for n in list(row[::-1])), 2)
        print(long_to_bytes(flag)) #b'ictf{sUpeRinCrEasIng_wH4T???}'
```





