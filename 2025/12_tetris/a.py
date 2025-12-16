#!/bin/env python3
import sys, re

# comment on my data set
# - tiles are all 3x3
# - no tiles have empty borders
# - 1000 regions

total = 0

file = sys.argv[1]

tiles = []
regions = []

current_tile = None
tile_lines = []

def append_tile(tile):
    c = 0
    n, s, w, e = 0, 0, 0, 0
    nf, sf, wf, ef = 0, 0, 0, 0

    if tile[0][0] == '#':
        n += 4
        nf+= 1
        w += 1
        wf+= 4
        c += 1
    if tile[0][1] == '#':
        n += 2
        nf+= 2
        c += 1
    if tile[0][2] == '#':
        n += 1
        nf+= 4
        e += 4
        ef+= 1
        c += 1
    if tile[1][0] == '#':
        w += 2
        wf+= 2
        c += 1
    if tile[1][1] == '#':
        c += 1
    if tile[1][2] == '#':
        e += 2
        ef+= 2
        c += 1
    if tile[2][0] == '#':
        s += 1
        sf+= 4
        w += 4
        wf+= 1
        c += 1
    if tile[2][1] == '#':
        s += 2
        sf+= 2
        c += 1
    if tile[2][2] == '#':
        s += 4
        sf+= 1
        e += 1
        ef+= 4
        c += 1

    masks = [ [ n, e, s, w ] ]
    for m in [ e, s, w, n ], [ s, w, n, e ], [ w, n, e, s], [ nf, wf, sf, ef ], [ wf, sf, ef, nf ], [ sf, ef, nf, wf ], [ ef, nf, wf, sf ]:
        if m not in masks:
            masks.append(m)
    
    tiles.append({
        'tile': tile,
        'count': c,
        'masks': masks
    })


def solve(w, h, target):
    return 0

for i, line in enumerate(open(file)):
    line = line.strip('\n')
    # print("read " + line)
    if (m := re.match(r'^(\d+):$', line)) is not None:
        # start of tile
        if current_tile is not None:
            # print(f"store {current_tile} {tile_lines}")
            append_tile(tile_lines)
            tile_lines = []
        current_tile = int(m.group(1))
        # print(f"reading tile {current_tile}")

    elif (m := re.match(r'^[#.]+$', line)) is not None:
        tile_lines.append(line)
        # print(f"shape → {tile_lines}")
    
    elif (m := re.match(r'^(\d+)x(\d+): (.+)$', line)) is not None:
        target = list(map(int, m.group(3).split(' ')))
        regions.append({
            'width': int(m.group(1)),
            'height': int(m.group(2)),
            'target': target
        })
        # print(f"added {regions[-1]}")

append_tile(tile_lines)

for i, tile in enumerate(tiles):
    print(f"{i}: {tile['tile']} → {tile['count']} / {tile['masks']}")

# out = open("data_reduced.txt", "w")

easy = 0
impossible = 0
todo = 0

for region in regions:
    count = 0
    n = 0
    for i, t in enumerate(region['target']):
        n += t
        count += t * tiles[i]['count']
    print(f"have to place {n} tiles of {count} bricks (for {n*9} slots) in {region['width'] * region['height']} slots ({(region['width']//3) * (region['height']//3)})")
    if n <= (region['width']//3) * (region['height']//3):
        easy += 1
        print(" ⇒ easy")
    elif count > region['width'] * region['height']:
        impossible += 1
        print(" ⇒ impossible")
    else:
        todo += 1
        total += solve(region['width'], region['height'], region['target'])
        # print(f"{region['width']}x{region['height']}: {' '.join(map(str, region['target']))}", file=out)

print(f"easy:{easy}, impossible:{impossible}, todo:{todo}")
