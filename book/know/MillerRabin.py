from Crypto.Util.number import bytes_to_long, long_to_bytes
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

def getPrime(n):
    while True:
        p = random.randint(2<<(n-2), 2<<(n-1))
        if MillerRabinPrimalityTest(p):
            return p


def gen_key():
    p = getPrime(512)
    q = getPrime(512)
    n = p*q
    phi = (p-1)*(q-1)
    e = 65537
    d = pow(e,-1,phi)
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
