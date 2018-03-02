#!/usr/bin/python3

import sys
from Npuzzle import Npuzzle

if __name__ == "__main__":
	npuzzle = Npuzzle(int(sys.argv[1]))
	npuzzle.resolve()
