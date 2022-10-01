# cakeCTF2021 together as one
## 問題概要
[問題リンクファイル](https://github.com/theoremoon/cakectf-2021-public/tree/master/crypto/together_as_one/distfiles)

素数$p,q,r$があり，$e=65537$，フラグを$m$とし，次の値が与えられる．
$$
n = pqr \\\\
c = m^e \\\\
x = (p+q)^r \mod n \\\\
y = (p+qr)^r \mod n
$$

## 解法
二項定理により，$x$の値について次の計算ができる．
$n=pqr$であり，$0<x<r$のとき${}_r\textrm{C}_x$が$r$の倍数であることを使っている．
$$
\begin{align}
x &= (p+q)^r \mod n \\\\
  &= {}_r\textrm{C}_0 p^rq^0 + {}_r\textrm{C}_1 p^{r-1}q^1 + {}_r \textrm{C}_2 p^{r-2}q^2 +   \cdots + {}_r\textrm{C}\_{r-1} p^1q^{r-1} + {}_r\textrm{C}\_{r} p^0q^{r-1} \mod n \\\\
  &= p^r + q^r \mod n
\end{align}
$$
$y$も同様に，展開をして$n$の倍数になる項を削除する．
$$
\begin{align}
y &= (p+qr)^r \mod n \\\\
  &= p^r + q^rr^r \mod n
\end{align}
$$
法$q$の世界で考える．すると，
$$
\begin{align}
x &= p^r \mod q\\\\
y &= p^r \mod q
\end{align}
$$
よって，整数$k$を用いると次が成り立つ
$$
\begin{align}
x &= y \mod q\\\\
x &= y + kq
x - y &= kq
\end{align}
$$

$x-y$は$q$の倍数であり，$n$も素因数$q$を持っているため，$q=\textrm{GCD}(x-y,n)$である．

次に，$x$と$y$を法$r$で考える．フェルマーの小定理により，$p^r \mod r=p$が成り立つ(他の変数も同様)．

$$
\begin{align}
x = p + q \mod r\\\\
y = p \mod r
\end{align}
$$
$q$が邪魔だが既知であるため，$r$について合同な式ができる．
$$
\begin{align}
x - q = y \mod r\\\\
\end{align}
$$
よって，$r=\textrm{GCD}(x-q-y,n/q)$である．
```python
from Crypto.Util.number import long_to_bytes,inverse

def GCD(a,b):
    if a%b==0:
        return b
    return GCD(b,a%b)

def LCM(a,b):
    return a//GCD(a,b)*b


n = # 長いので省略
c = 
x = 
y = 
e = 0x10001

q = GCD((x-y)%n,n)
r = GCD((x-y-q)%n,n)//q
p = n//r//q

print(f'{p = :#}')
print(f'{q = :#}')
print(f'{r = :#}')
assert p*q*r == n

phi = (p-1)*(q-1)*(r-1)
d = pow(e,-1,phi)
m = pow(c,d,n)
print(long_to_bytes(m))
```
```none
CakeCTF{This_chall_is_inspired_by_this_music__Check_out!__https://www.youtube.com/watch?v=vLadkYLi8YE_cf49dcb6a31f}
```

## 感想
$q$を見つけた後がわかりませんでした．
こういう式変形して最大公約数とって$p,q$あぶり出すタイプの問題，法を$p$とか$q$して合同な数を見つけようとすると見えやすくなるのかもしれない．
