#!/usr/bin/python

import os
import sys
import filecmp

#class readfile():
infile1 = sys.argv[1]
infile2 = sys.argv[2]
def cmpfiles(infile1,infile2):
    f1 = open('infile1',r).readline()
    f2 = open('infile2',r).readline()
    different = [x for x in f1 if x not in f2]
    print different

def main():
    if len(sys.argv) != 2:
        return
    cmpfiles(infile1,infile2)
if __name__ == "__main__":
    main()
