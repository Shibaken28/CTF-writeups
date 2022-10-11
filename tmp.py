from Crypto.Util.number import long_to_bytes,inverse,getPrime
from math import *

def GCD(a,b):
    while b:
        a,b = b,a%b
    return a

a = 10
b = a**10000
print('{:.10000g}'.format(b))

x = 10000000000000000000000000000000000
a = x*x
b = sqrt(a)
print('{:.10000g}'.format(b))


