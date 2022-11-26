# Miller–Rabin primality test
素数判定アルゴリズム．

```python
import random

def MillerRabinPrimalityTest(n, k=20):
    s = 0
    d = n-1
    if n == 2:
        return True
    if n == 1 or n % 2 == 0:
        return False
    # 奇数dと整数sでn-1=d*2^sを満たすようにする
    while d % 2 == 0:
        s += 1
        d //= 2
    # k回の試行を行う
    for _ in range(k):
        a = random.randint(1, n-1)
        x = pow(a, d, n)
        # x = 1 or -1
        if x != 1: 
            composite = True
            y = d
            for _ in range(s):
                x = pow(a, y, n)
                y *= 2
                if x == n-1:
                    composite = False
                    break
            if composite:
                return False
    return True
```
