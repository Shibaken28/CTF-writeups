# CakeCTF2021 discrete_log

## 概要
[問題リンク](https://github.com/theoremoon/cakectf-2021-public/tree/master/crypto/discrete-log/distfiles)

フラグの文字列の$i$文字目の文字コードを$m_i$として
$$
c_i \equiv g^{rm_i} \mod p
$$
の各$c_i$が与えられる．なお，素数$p$と正の整数$g$は与えられている．正の整数$r$は与えられない．
## 解法
$g^r$の値がわかれば，$m_i$を全探索(多くて256通り)すればいい．
フラグ形式より，$m_0$が`ord("C")`であることがわかるので，$d\equiv m_0^{-1}\mod \phi(p)$として
$(g^{rm_0})^d \equiv g^r \mod p$と計算することで$g^r$が求める．

```python
from Crypto.Util.number import *

def GCD(a,b):
    if a%b==0:
        return b
    return GCD(b,a%b)

def LCM(a,b):
    return a//GCD(a,b)*b

def extGCD(a, b):
    if b:
        d, y, x = extGCD(b, a % b)
        y -= (a // b)*x
        return d, x, y
    return a, 1, 0

p = # 長いので省略
q = 
cs = 

d = inverse(ord("C"),p-1)
gr = pow(cs[0],d,p)
flag = ""
for c in cs:
    for i in range(1<<8):
        if c==pow(gr,i,p):
            flag += chr(i)
print(flag)
```
```none
CakeCTF{ba37a0f409ef3ec23a6cffbc474a1cef}
```

## コメント
1文字ずつ暗号化するのは危険
