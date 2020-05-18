from RSA.genkeys import *
import sys

pubPath = '../publickey/'
prvPath = './privatekey/'

def main():
  id = sys.argv[1]
  pk = generatekeys(pubPath,prvPath,id);
  # N = pk[0]
  # e = pk[1]
  # print(N)
  # print(e)

if __name__ == "__main__":
    main()