# ImaginaryCTF October 2022 RSA-ECB
## 問題
フラグの各1文字ずつ，文字コードがRSAで暗号化されている．パラメータは$n,e$のみ既知．
```python
#!/usr/bin/env python3

from Crypto.Util.number import *

p = getPrime(512)
q = getPrime(512)
n = p*q
e = 65537

m = open("flag.txt", 'rb').read()

out = open('output', 'wb')

out.write(long_to_bytes(n))

for c in m:
    out.write(long_to_bytes(pow(c, e, n)))
```

## 解法
考えられる候補の少ないところをブルートフォースするタイプの問題．
各1文字は8ビットなので簡単に全探索できる．今回の場合は$n$と各$c_i$がバイナリデータとしてつなげて出力されているので，適切なビット数を区切って取得する必要がある．
```python
from Crypto.Util.number import *

f = open("./output", "rb").read()

l = 1024//8
n = bytes_to_long(f[:l])
cs = []
for i in range(l,len(f),l):
    cs.append(bytes_to_long(f[i:i+l]))

flag = ""
e = 0x10001
print(f"n = {n}")

for c in cs:
    for m in range(1<<8):
        if pow(m,e,n) == c:
            flag += chr(m)
            break

print(flag)

# ictf{dont_mind_me_I'm_just_brute_forcing_rsa}
```

## コメント
よくある一文字ずつブルートフォースするタイプの問題かと思ったら，バイナリに連結されて出力されたので各パラメータのビット数をちゃんと考える必要があった．

