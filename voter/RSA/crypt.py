import sys
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib
import json

def gcd(a,b):
    # a < b
    if a == 0:
        return b
    else:
        return gcd(b % a, a)

def encrypt(key,src):
    #read file pk
    f = open(key,"r")
    output = json.loads(f.read())
    f.close()
    N = output[0]
    e = output[1]
    #select random x
    x = 0
    while True:
        x = int.from_bytes(os.urandom(8),byteorder="big")
        if x >= 2 and gcd(x,N) == 1:
            break
    #encrypt x using RSA; y = x^e in Zn
    y = pow(x,e,N)
    #encrypt message with AES
    root = hashlib.md5()
    root.update(str(x).encode('utf-8'))
    k = root.hexdigest()
    #AES m: str -> bytes -> AES -> bytes -> hex
    nonce = get_random_bytes(11)
    cipher = AES.new(bytes(k,'utf-8'), AES.MODE_CCM, nonce)
    # cipher.encrypt => bytes
    root = hashlib.sha256()
    root.update(str(src).encode('utf-8'))
    mac = root.hexdigest()
    msgToEncrypt = json.dumps([src,mac])
    msg = cipher.encrypt(bytes(msgToEncrypt,'utf-8'))
    msg = msg.hex()
    # output file
    nonce = nonce.hex()
    cipherMessage = [y,msg,nonce]
    return json.dumps(cipherMessage)

def decrypt(key,src):
    # f = open(src, "r")
    output = json.loads(src)
    y = output[0]
    c = output[1]
    c = bytes.fromhex(c)
    nonce = output[2]
    nonce = bytes.fromhex(nonce)

    f = open(key,"r")
    output = json.loads(f.read())
    f.close()
    N = output[0]
    d = output[1]
    #x = RSA^-1(y) = y^d mod N = (x^e mod N)^d mod N
    x = pow(y,d,N)
    # print(x)
    #k = H(x)
    root = hashlib.md5()
    root.update(str(x).encode('utf-8'))
    k = root.hexdigest()
    #m = D(k,c) c: bytes -> AES -> bytes -> str
    cipher = AES.new(bytes(k,'utf-8'), AES.MODE_CCM, nonce)
    msgDecripted = json.loads(cipher.decrypt(c).decode('utf-8'))
    msg = msgDecripted[0]
    mac = msgDecripted[1]
    root = hashlib.sha256()
    root.update(str(msg).encode('utf-8'))
    mac2 = root.hexdigest()
    if mac == mac2:
      return msg
    else:
      err = "MAC not match"
      print(err)
      return err