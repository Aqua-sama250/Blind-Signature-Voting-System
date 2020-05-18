import sys
import os
import json
from RSA.crypt import *

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

def main():
  #command: python vote.py [voterID] [organizerId] [message]
  voterId = sys.argv[1]
  organizorId = sys.argv[2]
  message = sys.argv[3]
  # organizorId = 'organizor#000'
  #receive signatured ballot
  f = open("../transfer/ballot.msg","r")
  ballotPrime = json.loads(f.read())
  f.close()
  f = open("./random.ran","r")
  random = json.loads(f.read())
  r = random[0]
  rinv = random[1]
  f.close()
  f = open("../publickey/" + organizorId + ".pub","r")
  p2 = json.loads(f.read())
  f.close()
  N2 = p2[0]

  #ballot = ballotPrime * r^-1 mod N2 = p^b % N2
  sigN1 = (ballotPrime[0] * (rinv % N2)) % N2
  sige = (ballotPrime[1] * (rinv % N2)) % N2
  ballot = [sigN1,sige]
  print("ballot = ")
  print(ballot)

  f = open("../publickey/" + voterId + ".pub","r")
  p = json.loads(f.read())
  f.close()
  messageWithBallot = [ballot,p,message]
  print("messageWithBallot = ")
  print(messageWithBallot)

  #decrypt messageWithBallot using p2
  cipher = encrypt("../publickey/" + organizorId + ".pub",json.dumps(messageWithBallot))

  f = open("../transfer/voteMessage.msg","w")
  f.write(cipher)
  f.close()

if __name__ == "__main__":
    main()