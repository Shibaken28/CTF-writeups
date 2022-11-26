# getPrime
ミラーラビン素数判定を用いて、指定されたビット数の素数を生成する。

## depends
- [Miller–Rabin primality test](./Miller-Rabin.md)


```python
def getPrime(n):
    while True:
        p = random.randint(2<<(n-2), 2<<(n-1))
        if MillerRabinPrimalityTest(p):
            return p
```
