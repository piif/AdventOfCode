#!/bin/env python3
import sys

total = 0

if len(sys.argv) > 1:
    input = open(sys.argv[1])
else:
    input = sys.stdin


def enumerate_combinations(value, splits):
    if splits == 1:
        yield [ value ]
        return
    for i in range(0, value+1):
        for j in enumerate_combinations(i, splits-1):
            yield [ value - i ] + j


# in my data file, 3 hard cases
# - 171 lines
# - biggest joltage is 300
# - all button seems to have sorted positions
# - longest joltage list has 10 items
# - longest button list has 12 buttons
# - longest button has 8 items

def solve(joltage, buttons, indent=''):
    # find less present joltage in buttons
    nb_j = [ 1000 if j == 0 else 0 for i, j in enumerate(joltage) ]
    for b in buttons:
        for j in b:
            nb_j[j] += 1
    # print(f"{indent}button joltages {nb_j}")

    bmin = min(*nb_j)
    if bmin <= 3:
        imin = nb_j.index(bmin)
        jmin = joltage[imin]
    else:
        # find smaller joltage
        imin=-1
        jmin=1000
        for i, j in enumerate(joltage):
            if j > 0 and j < jmin:
                jmin = j
                imin = i

    # find buttons containing this position
    buttons_to_try = []
    buttons_left = []
    for b in buttons:
        if imin in b:
            buttons_to_try.append(b)
        else:
            # used buttons can be removed from list to try with remaining joltage since they will imply to set current joltage < 0
            buttons_left.append(b)

    nb_buttons_to_try = len(buttons_to_try)
    if nb_buttons_to_try == 0:
        return None

    # sort them from longer (will have bigger impact on all joltages)
    buttons_to_try.sort(reverse=True, key=lambda x: len(x))
    # print(f"{indent}trying on {joltage} j[{imin}]={jmin} with {nb_buttons_to_try} buttons: {buttons_to_try}")

    found = None

    # for each buttons combination which keep other ones >= 0:
    for presses in enumerate_combinations(jmin, nb_buttons_to_try):
        # deduce new joltage
        new_joltage = press_button(joltage, buttons_to_try, presses)
        if new_joltage is None:
            continue

        if sum(new_joltage) == 0:
            # this is a solution
            return jmin

        if len(buttons_left) == 0:
            # wont find solution thru this path
            continue

        # recurse with remaining joltage
        subfound = solve(new_joltage, buttons_left, indent+'  ')
        if subfound is not None:
            # # for the moment, stop at first solution
            # return jmin + subfound
            if found is None:
                found = jmin + subfound
            else:
                found = min(jmin + subfound, found)

    return found


def press_button(joltage, buttons, presses):
    new_joltage = joltage.copy()
    for i in range(len(buttons)):
        b = buttons[i]
        p = presses[i]
        for pos in b:
            if new_joltage[pos] < p:
                return None
            new_joltage[pos] -= p
    return new_joltage

count = 0
for i, line in enumerate(input):
    line = line.strip('\n').split(' ')
    firsts = list(map(int, line[0][1:-1].split(',')))
    buttons = [ list(map(int, l[1:-1].split(','))) for l in line[1:-1] ]
    joltage = list(map(int, line[-1][1:-1].split(',')))
    
    nb_buttons = [ 0 ] * len(joltage)
    for button in buttons:
        display = [ '    ' ] * len(joltage)
        for j in button:
            display[j] = '  # '
            nb_buttons[j] += 1
        print(''.join(display))
    print(''.join([ f"{n:4}" for n in nb_buttons ]))
    print(''.join([ f"{j:4}" for j in joltage ]))

    min_joltage = min(*joltage)
    first_nb = min_joltage // len(firsts)
    first_presses = [ first_nb ] * len(firsts)
    first_buttons = [ buttons[b] for b in firsts ]
    joltage = press_button(joltage, first_buttons, first_presses)
    print(f"press {first_nb} times buttons {firsts}")
    print(''.join([ f"{j:4}" for j in joltage ]))

    found = (first_nb * len(firsts))
    print(found, '+')
    s= solve(joltage, buttons) or 0
    found += s
    print(found)
    total += found
    print()

print(f"⇒ {total}")
# ⇒ 9283 for 121 tests < 500 , in 11s

# 8: ??
# 44: ??
# 131: 275

# 0: 155
# 4: 324
# 14:241
# 15:110
# 16:250
# 17:171
# 18:178
# 30:200
# 36:285
# 37:149

# 49: 106
# 51: 101
# 54: 229
# 62: 241
# 63: 208
# 70: 212
# 72: 261
# 79: 257
# 84: 126
# 86: 255

# 90: 126
# 99: 272
# 100: 269
# 102: 186
# 103: 220
# 104: 110
# 105: 136
# 106: 226
# 112: 143
# 119: 233
# 122: 178
# 124: 255
# 129: 155
# 130: 193
