import sys
import os
import json
from RSA.crypt import *

def main():
  # organizorId = 'organizor#000'
  organizorId = sys.argv[1]

  f = open("../transfer/voteMessage.msg","r")
  cipher = f.read()
  f.close()
  #decrypt msg using s2
  message = decrypt("./privatekey/" + organizorId + ".prv",cipher)
  print("voteMessage = ")
  print(message)
  [ballot,p,msg] = json.loads(message)
  #check signature using p2
  f = open("../publickey/" + organizorId + ".pub","r")
  p2 = json.loads(f.read())
  f.close()
  checkN = pow(ballot[0],p2[1],p2[0])
  checke = pow(ballot[1],p2[1],p2[0])
  if checkN == p[0] and checke == p[1]:
    print("signature check success")
    #write voting message into box
    if os.path.exists("./box.msg"):
      f = open("./box.msg","r")
      cipher = f.read()
      f.close()
      pair = json.loads(decrypt("../publickey/" + organizorId + ".pub",cipher))
      if json.dumps(p) not in pair:
        pair[json.dumps(p)] = msg
        f = open("./box.msg","w")
        print("saving pair:")
        print(pair)
        result = encrypt("./privatekey/" + organizorId + ".prv",json.dumps(pair))
        f.write(result)
        f.close()
    else:
      pair = {}
      pair[json.dumps(p)] = msg
      f = open("./box.msg","w")
      print("saving pair:")
      print(pair)
      result = encrypt("./privatekey/" + organizorId + ".prv",json.dumps(pair))
      f.write(result)
      f.close()
  else:
    print("signature check failed")


if __name__ == "__main__":
    main()