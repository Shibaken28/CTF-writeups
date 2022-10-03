# CakeCTF2022 brand new crypto
## 問題
[問題リンク](https://github.com/theoremoon/cakectf2022-public/tree/master/crypto/brand_new_crypto/distfiles)

素数$p,q$があり，$n=pq$．$\phi=(p-1)(q-1)$として$0$以上$\phi$以下の整数$a,s$があり，

$$
\begin{align}
\phi &= (p-1)(q-1) \\\\
b &= \phi + 1 -a \\\\
t &= -sa b^{-1} \pmod \phi
\end{align}
$$

$b$と$\phi$は互いに素であることが保証される．
$0$以上$n$以下の整数$r$を使って次のように暗号化される
$$
c_1 \equiv mr^s \pmod n\\\\
c_2 \equiv mr^t \pmod n
$$
復元は次のようにできる
$$
m = c_1 ^a c_2^b \pmod n
$$

その他色々な条件があるが，この暗号が破綻しないために例外を考えなくていいということなんだろう．

そして，各フラグの$i$文字目の文字コード$m_i$についてこの暗号化をした値$c_1,c_2$が与えられる．また，全体で$a,b,s,t,p,q$の値は固定．$r$だけランダム．
与えられる値は，各暗号化された値と$s,t,n$．

## 考えたこと
なんかよくわからないのでまず復元で何が起こっているかを見ておく．
確かに，
$$
m\equiv  c_1 ^a c_2 ^b \equiv (mr^s)^a (mr^t)^b \equiv m^a r^{sa} m^b r^{-sab^{-1}b} \equiv m^{ab}r^{sa-sa} \equiv m^{ab} \equiv m^{\phi+1} \equiv m \pmod n
$$
と成り立っている．
なんとなく，$t$が$a,b$にから計算されているので，これをうまく使うんじゃないかと思う．
あと，$m_i$がせいぜい256通りなので，それっぽい値がわかれば全探索が可能．

4時間後，次の方法が思いついた．

$$
(mr^s)^t (mr^t)^{-s} \equiv m^{t-s} r^{st-st} \equiv m^{t-s} \pmod n
$$

これで，$m$を全探索して$m^{t-s}\pmod n$と一致するものを見つければ良い．
$s$と$t$が具体的にどんな方法で出された値であるかを考える必要はなかったのだ．

```python
from Crypto.Util.number import inverse , long_to_bytes

s,t,n = 長いので省略
cs = 

flag = ""
for c1,c2 in cs:
    mst = (pow(c1,t,n)*pow(pow(c2,s,n)%n,-1,n))%n
    print(mst)
    for m in range(256):
        if pow(m,t-s,n)==mst:
            print(chr(m))
            flag += chr(m)
print(flag)

```
```none
CakeCTF{s0_anyway_tak3_car3_0f_0n3_byt3_p1aint3xt}
```

## 感想
悩んだ割に結構解法がシンプルでした．$m$が同じで$e$が異なるRSAへの攻撃手法を思い出しました．
同じ数の異なる冪数があるときはこの道の解法を考えると良さそう．
