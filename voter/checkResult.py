import sys
import os
import json
from RSA.crypt import *

def main():
  # command: python checkResult.py [voterId] [organizerId]
  # voterId = "voter#123"
  # organizorId = "organizor#000"
  voterId = sys.argv[1]
  organizorId = sys.argv[2]
  f = open("../transfer/box.msg","r")
  cipher = f.read()
  f.close()
  print(cipher)
  msg = json.loads(decrypt("../publickey/" + organizorId + ".pub",cipher))
  print(msg)
  f = open("../publickey/" + voterId + ".pub","r")
  p = f.read()
  f.close()
  print("voted messge = ")
  print(msg[p])

if __name__ == "__main__":
    main()