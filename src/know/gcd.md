# ユークリッドの互除法
計算量を$O(\log\min(a,b))$で最大公約数を求める．

```python
def GCD(a,b):
    while b:
        a,b = b,a%b
    return a
```

