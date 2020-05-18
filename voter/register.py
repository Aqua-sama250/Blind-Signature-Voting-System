import sys
import os
import json
from RSA.crypt import *

pubPath = '../publickey/'

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

def blinder(target,blindKey):
  N2 = blindKey[0]
  a = blindKey[1]
  # random r, gcd(r,N) == 1
  while True:
    r = int.from_bytes(os.urandom(128),byteorder="big")
    if gcd(r,N2) == 1:
      break
  rinv = modinv(r,N2)
  # m' = (m * r ^ a) % N2 = (m % N2 ) * (r^a % N2) % N2
  N1prime = ((target[0] % N2) * pow(r,a,N2)) % N2
  eprime = ((target[1] % N2) * pow(r,a,N2)) % N2
  targetPrime = [N1prime,eprime]
  return targetPrime,r,rinv


def main():
  #command: python register.py [voterID] [organizorID]
  # voterId = 'voter#123'
  # organizorId = 'organizor#000'
  voterId = sys.argv[1]
  organizorId = sys.argv[2]
  f = open(pubPath + voterId + ".pub","r")
  output = f.read()
  p = json.loads(output)
  f.close()
  f = open(pubPath + organizorId + ".pub","r")
  output = f.read()
  p2 = json.loads(output)
  f.close()
  #pPrime = p * r ^ a % N2
  pPrime,random,randominv = blinder(p,p2)
  #assume voter passed changllenge question about his ID
  print("p' = ")
  print(pPrime)
  print("[r,r^-1] = ")
  print([random,randominv])
  f = open("../transfer/ballot.msg","w")
  #encrypt pPrime
  cipher = encrypt("../publickey/" + organizorId + ".pub",json.dumps(pPrime))
  f.write(cipher)
  f.close()
  f = open("./random.ran","w")
  f.write(json.dumps([random,randominv]))
  f.close()

if __name__ == "__main__":
    main()