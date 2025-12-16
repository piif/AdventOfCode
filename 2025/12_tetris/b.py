#!/bin/env python3
import sys

total = 0

file = sys.argv[1]

for i, line in enumerate(open(file)):
    line = line.strip('\n')
    print("read " + line)

print(total)