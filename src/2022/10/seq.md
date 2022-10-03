# picoCTF2022 Sequences
## 概要
$$
\begin{align}
a_0 &= 1 \\\\
a_1 &= 2 \\\\
a_2 &= 3 \\\\
a_3 &= 4 \\\\
a_i &= 21a\_{i-1} + 301a\_{i-2} - 9549\_{i-3} + 55692 a\_{i-4} \quad (i>4)
\end{align}
$$
で定義される数列で，$a\_{20000000}$を$10^{10000}$で割った余りを求める．

## 解法
数列は，$4$項間の線形漸化式である．線形漸化式の$n$項目は高速に求められる([参考](https://shibaken28.github.io/my-library-for-competitive-programming/famous/fibo.html))．
次のように行列で表し，ダブリングによって累乗を高速に計算する．
$$
\\begin{pmatrix}
21 & 301 & -9549 & 55692 \\\\
1 &0&0&0\\\\
0&1&0&0\\\\
0&0&1&0\\\\
\\end{pmatrix}
^{n-3}
\\begin{pmatrix}
a\_3\\\\
a\_2\\\\
a\_1\\\\
a\_0
\\end{pmatrix}
\=
\\begin{pmatrix}
a\_n\\\\
a\_{n-1}\\\\
a\_{n-2}\\\\
a\_{n-3}
\\end{pmatrix}
$$


```python
import math
import hashlib
import sys
from tqdm import tqdm
import functools

ITERS = int(2e7)
VERIF_KEY = "96cc5f3b460732b442814fd33cf8537c"
ENCRYPTED_FLAG = bytes.fromhex("42cbbce1487b443de1acf4834baed794f4bbd0dfe08b5f3b248ef7c32b")

def mat_mul(a, b) :
    I, J, K = len(a), len(b[0]), len(b)
    c = [[0] * J for _ in range(I)]
    for i in range(I) :
        for j in range(J) :
            for k in range(K) :
                c[i][j] += a[i][k] * b[k][j]
            c[i][j] %= 10**10000
    return c


def mat_pow(x, n):
    y = [[0] * len(x) for _ in range(len(x))]

    for i in range(len(x)):
        y[i][i] = 1

    while n > 0:
        if n & 1:
            y = mat_mul(x, y)
        x = mat_mul(x, x)
        n >>= 1

    return y


d0 = 0
ret = [[4], [3], [2],[1]]
mat = [[21,301,-9549,55692], [1, 0, 0, 0], [0, 1, 0, 0],[0,0,1,0]]
#ret = mat_mul(mat_pow(mat, ITERS), ret)
#ret = [[1],[1]]
#mat = [[1,1], [1,0]]
ret = mat_mul(mat_pow(mat, ITRES), ret)
print(ret)


# Decrypt the flag
def decrypt_flag(sol):
    sol = sol % (10**10000)
    sol = str(sol)
    sol_md5 = hashlib.md5(sol.encode()).hexdigest()

    if sol_md5 != VERIF_KEY:
        print("Incorrect solution")
        sys.exit(1)

    key = hashlib.sha256(sol.encode()).digest()
    flag = bytearray([char ^ key[i] for i, char in enumerate(ENCRYPTED_FLAG)]).decode()

    print(flag)

if __name__ == "__main__":
    sol = A
    decrypt_flag(sol)
```

## コメント
競プロだと基本ですね
