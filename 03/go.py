digits = re.compile('[0-9]+')

def go(input):
    lines = parse.lines(input)
    partsum = 0 # sum of all part numbers adjacent to a symbol
    stars = {} # (x,y) -> list of part numbers adjacent to a '*' there
    for j, l in enumerate(lines):
        for m in digits.finditer(l):
            n = int(m.group(0))
            found_symbol = False
            # apply this to all the spots adjacent to our number
            def check(x,y):
                nonlocal found_symbol
                if x < 0 or x >= len(l) or y < 0 or y >= len(lines):
                    return
                c = lines[y][x]
                if c == '.' or c.isdigit():
                    return
                found_symbol = True
                if c == '*':
                    stars[(x,y)] = stars.get((x,y),[]) + [n]

            check(m.start()-1, j)
            check(m.end(), j)
            for dy in (-1,1):
                for x in range(m.start()-1,m.end()+1):
                    check(x, j+dy)

            if found_symbol:
                partsum += n
    print(f"part 1, sum of attached parts: {partsum}")

    gearsum = sum(nums[0]*nums[1] for p,nums in stars.items() if len(nums) == 2)
    print(f"part 2, sum of gear ratios: {gearsum}")
