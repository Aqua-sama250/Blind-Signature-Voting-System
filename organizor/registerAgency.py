import os
import sys
import json
from RSA.crypt import *

prvPath = './privatekey/'

def main():
  #command: python registerAgency.py [voterId] [organizorID]
  #assume voter passed changllenge question about his ID
  #organizor knows (voterId, p1')

  voterId = sys.argv[1]
  organizorId = sys.argv[2]
  # organizorId = 'organizor#000'

  if os.path.exists("./registeredID.msg"):
    f = open("./registeredID.msg","r")
    output = f.read()
    ids = json.loads(output)
    print(ids)
    f.close()
    if voterId in ids:
      print("voter has registered")
      return -1
    else:
      ids.append(voterId)
      f = open("./registeredID.msg","w")
      f.write(json.dumps(ids))
      f.close()
  else:
    f = open("./registeredID.msg","w")
    f.write(json.dumps([voterId]))
    f.close()

  f = open(prvPath + organizorId + ".prv","r")
  output = f.read()
  s2 = json.loads(output)
  f.close()
  f = open("../transfer/ballot.msg","r")
  #decrypt cipher
  message = decrypt("./privatekey/" + organizorId + ".prv",f.read())
  pPrime = json.loads(message)
  f.close()
  print(pPrime)
  # ballot = [N1',e']
  # organizorSK = [N2,b]
  #signature: sig(p1') = (p1') ^ b = [N1'^b, e'^b]
  sigN1 = pow(pPrime[0],s2[1],s2[0])
  sige = pow(pPrime[1],s2[1],s2[0])
  ballotPrime = [sigN1,sige]
  print("ballot' = ")
  print(ballotPrime)
  f = open("../transfer/ballot.msg","w")
  f.write(json.dumps(ballotPrime))
  f.close()

if __name__ == "__main__":
    main()