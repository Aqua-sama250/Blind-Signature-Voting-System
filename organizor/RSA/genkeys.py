import sys
import os
from .PrimeGenerator import *

def gcd(a,b):
    # a < b
    if a == 0:
        return b
    else:
        return gcd(b % a, a)

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return -1
    else:
        return x % m

def generatekeys(pubPath,prvPath,fileName):
    # p = int.from_bytes(os.urandom(32),byteorder='big')#128bytes
    # q = int.from_bytes(os.urandom(32),byteorder='big')
    p = generate_prime_number()
    q = generate_prime_number()
    print("p = " + str(p))
    print("q = " + str(q))
    N = p * q
    print("N = " + str(N))
    phi = (p - 1) * (q - 1)
    print("phi = " + str(phi))
    while True:
        e = int.from_bytes(os.urandom(128),byteorder="big") % phi
        d = modinv(e,phi)
        if d > 0:
            break
    print("e = " + str(e))
    print("d = " + str(d))

    # output_file
    filename = pubPath + fileName + ".pub"
    f = open(filename,"w")
    publicKey = [N,e]
    f.write(str(publicKey))
    f.close()
    filename = prvPath + fileName + ".prv"
    f = open(filename,"w")
    privateKey = [N,d]
    f.write(str(privateKey))
    f.close()
    return publicKey
