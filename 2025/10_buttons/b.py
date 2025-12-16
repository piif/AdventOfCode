#!/bin/env python3
import sys

total = 0

file = sys.argv[1]

primes = [ 2, 3, 5, 7, 11, 13, 17, 23, 29, 31, 37, 41 ]

def conv_buttons(input):
    value = 1
    for b in input:
        value *= primes[int(b)]
    print(f"conv_buttons {input} → {value}")
    return value

def conv_joltage(input):
    value = 1
    for i, b in enumerate(input):
        value *= primes[i] ** int(b)
    print(f"conv_joltage {input} → {value}")
    return value


def solve_for_len(source, target, buttons, test_len):
    # print(f"solve_for_len({source}, {target}, {buttons}, {test_len})")
    for i, b in enumerate(buttons):
        value = source ^ b
        if test_len == 1:
            if value == target:
                return True
        else:
            if solve_for_len(value, target, buttons[i+1:], test_len-1):
                return True


def solve(target, buttons):
    remain = target
    all_presses = 0
    for button in buttons:
        if remain > button:
            presses = remain // button
            print(f"  try {presses} on {button}")
            remain -= presses * button
            all_presses += presses
        if remain == 0:
            return all_presses
    return None


for i, line in enumerate(open(file)):
    line = line.strip('\n').split(' ')
    buttons = [ l[1:-1].split(',') for l in line[1:-1] ]
    buttons.sort(key = lambda x:len(x))
    buttons = list(map(conv_buttons, buttons))
    joltage = conv_joltage(line[-1][1:-1].split(','))
    print(f"read {buttons} / {joltage}")
    # found = solve(joltage, buttons)
    # print(found)
    # total += found

print(total)
