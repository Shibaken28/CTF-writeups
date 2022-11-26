# RSA
## 必要な知識
- モジュロ演算
- Fermatの小定理，オイラーの$\varphi$関数
- 拡張ユークリッドの互除法

## 概要
素数$p$と$q$を用いて，$n=pq$とする．
$e$を公開鍵として，$d$を秘密鍵とする．
$e$と$d$は，以下の式を満たす必要がある．
$$ed\equiv 1\pmod{\varphi(n)}$$
$e$と$\phi(n)$は互いに素である必要がある．
ここで，$\varphi(n)$はオイラー関数である．この値は$n$が異なる素数$p$と$q$の積である場合，次のように求められる．
$$\varphi(n)=(p-1)(q-1)$$
公開鍵$(e,n)$と秘密鍵$(d,n)$を用いて，暗号化と復号化を行う．
ここで，$m$は平文，$c$は暗号文である．
暗号化は，以下の式で行う．
$$c\equiv m^e\pmod{n}$$
復号化は，以下の式で行う．
$$m\equiv c^d\pmod{n}$$

## 成り立つ理由
オイラーの$\varphi$関数は，$x$と互いに素な$n$について，次の性質がある．
$$x^{\varphi(n)} \equiv 1 \pmod n$$
$ed\equiv 1 \pmod{\varphi(n)}$であるため，次のように復元できることがわかる．
$$
c^d\equiv (m^e)^d\equiv m^{ed}\equiv m^{k\varphi(n)+1} \equiv m^{k\varphi(n)}m\equiv (m^{\varphi(n)})^k m \equiv 1^km\equiv m\pmod{n}
$$

なお，$k$は$ed=k\varphi(n)+1$が成り立つ整数である．

## 一般化(Multi-prime RSA)
$n=p_1^{e_1}p_2^{e_2}\cdots p_k^{e_k}$とする．オイラーの$\varphi$関数は，次のように計算できる．
$$\varphi(n)=\prod_{i=1}^k(p_i-1)p_i^{e_i-1}$$

## プログラム上での求め方
### $p,q$
ミラー–ラビン素数判定法を使うことで巨大な素数が生成できる．
### $e$
$e=65537$などの素数を用いることが多い．
### $d$
$ed\equiv 1\pmod{\varphi(n)}$を満たすような$d$を求める．
これは，拡張ユークリッドの互除法を用いて求めることができる．
### $c,m$
$c\equiv m^e\pmod{n}$や$m\equiv c^d\pmod{n}$を計算する．
このとき，$m^e$や$c^d$は巨大な数になるため，Naiveな計算では間に合わない．
繰り返し二乗法(バイナリ法，ダブリングなど)を用いることで，$O(\log e),O(\log d)$で計算できる．

## 実装例
```python
from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes

def gen_key():
    p = getPrime(1024)
    q = getPrime(1024)
    n = p*q
    phi = (p-1)*(q-1)
    e = 65537
    d = inverse(e,phi)
    return (e,n),(d,n)

def encrypt(m,e,n):
    return pow(m,e,n)

def decrypt(c,d,n):
    return pow(c,d,n)

if __name__ == "__main__":
    (e,n),(d,n) = gen_key()
    m = bytes_to_long(b"Hello World")
    c = encrypt(m,e,n)
    print(long_to_bytes(decrypt(c,d,n)))
```

