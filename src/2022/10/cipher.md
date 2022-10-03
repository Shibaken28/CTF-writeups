# InterKosenCTF2020 ciphertexts
## 問題
平文$m$，素数$p,q,r$があって，$n_1=pq$，$n_2=pqr$，素数$e_1$とその次に大きい素数$e_2$を用意．
$$
\begin{align}
c_1 &= m^{e_1} \pmod {pq} \\\\
c_2 &= m^{e_2} \pmod  {pqr}
\end{align}
$$
$p,q,r$以外は与えられる．
## 解法
```python
r = n2//n1
d=pow(e1,-1,r-1)
m=pow(c1,d,r)
print(long_to_bytes(m))
```
$r$がバレているので$\mod r$の世界で考えれば行けるんじゃないかと思ったがだめだった．
では，$\mod pq$の世界ではどうだろうか．$c_2$を$\pmod {pq}$で考えて，$e_1x+e_2y=1$となるような$x,y$を見つけてくれば良い．
$$
c_1^x c_2^y \equiv (m^{e_1})^x(m^{e_2})^y  \equiv m^{e_1x+e_2y} \equiv m \pmod {pq}
$$
```python
x = -74571
y = 74570
print(e1*x+e2*y) # 1
m = (pow(c1,x,n1)*pow(c2,y,n1))%n1
print(long_to_bytes(m))
```
```python
1
b'KosenCTF{HALDYN_D0M3}'
```
出てきた．
## コメント
warmup問題として出たらしい．
