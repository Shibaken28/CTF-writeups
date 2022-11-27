# ImaginaryCTF October 2022 RSA-CBC

## 問題
$2048$ビットの$n$を使って，フラグの一文字ずつ$m_i$として次を実行する．$vi$の初期値は256ビットのランダムな値．
1. $c_i=(vi+m_i)^e$を計算する．
2. $vi$に$c_i$を代入する．

各$c_i$の値の値と$vi$の初期値が与えられるので，フラグを復元する．

```python
from Crypto.Util.number import getPrime
from secrets import randbelow


class RSACBC:
    def __init__(self, size):
        self.blk = 1
        self.len = size // 8
        self.n = getPrime(size // 2) * getPrime(size // 2)
        self.e = 65537

    def encrypt(self, msg: bytes) -> bytes:
        iv = randbelow(self.n)
        iv0 = iv
        ct = b""
        for i in range(0, len(msg), self.blk):
            m = int.from_bytes(msg[i : i + self.blk], "big")
            c = pow(iv + m, self.e, self.n)
            ct += c.to_bytes(self.len, "big")
            iv = c
        return iv0.to_bytes(self.len, "big"), ct


flag = open("flag.txt", "rb").read().strip()
assert flag.startswith(b"ictf{")
assert flag.endswith(b"}")
flag = flag[5:-1]
cipher = RSACBC(2048)
print(f"n = {cipher.n}")

iv, ct = cipher.encrypt(flag)
print(f"{iv = }")
print(f"{ct = }")
```



## 解法
$1$文字ずつ$c_i$をブルートフォースするタイプの問題．
```python
from Crypto.Util.number import *

flag = ""
iv = bytes_to_long(iv)
d = 2048 // 8
for i in range(0,len(ct),d):
    c = bytes_to_long(ct[i:i+d])
    e = 65537
    for m in range(256):
        if pow(iv+m,e,n) == c:
            iv = c
            flag += chr(m)
            break
    
print(flag)

```

## コメント
ecbモードの問題とほぼ同じ解法．RSAはあんまり関係ない．
