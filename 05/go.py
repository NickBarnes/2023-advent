# I brute-forced part 2 in C (see part2.c) and then wrote a much more
# pleasant version with interval arithmetic.

class Map:
    def __init__(self, lines):
        d1,d2 = lines[0].split()
        assert d2 == 'map:'
        self.source,t,self.dest = d1.split('-')
        assert t == 'to'
        self.ranges = [(interval.Interval(l[1], l[1] + l[2]),
                        l[0]-l[1])
                       for line in lines[1:]
                       if (l := [int(x) for x in line.split()])]

    def apply(self, v):
        for (src, delta) in self.ranges:
            if v in src:
                return v + delta
        return v

    # ooh look at the shiny shiny
    def apply_intervals(self, inter):
        hits = []
        ints = inter.ints
        for (src, delta) in self.ranges:
            hits += [hit.offset(delta) for i in ints if (hit := i & src)]
            ints = sum([list(i - src) for i in ints], [])
        return interval.Intervals([(x.base, x.limit) for x in hits + ints])

# Seed intervals for part 2
def seed_intervals(seeds):
    return interval.Intervals([(int(base), int(base)+int(length))
                               for base, length in
                               zip(seeds[::2],seeds[1::2])])

# Minimum location for part 1
def min_location_1(seeds, maps):
    return min(functools.reduce(lambda v,m: m.apply(v), maps, s)
               for s in seeds)

# Minimum location for part 2 (interval arithmetic)
def min_location_2(seeds, maps):
    return (functools.reduce(lambda i,m: m.apply_intervals(i), maps, seeds)
            .ints[0].base)

def go(input):
    sections = parse.sections(input)
    seeds = sections[0]
    assert len(seeds) == 1
    seeds = seeds[0].split()
    assert seeds[0] == 'seeds:'
    seeds = seeds[1:]

    maps = [Map(s) for s in sections[1:]]
    print("part 1, minimum location: "
          f"{min_location_1([int(x) for x in seeds], maps)}")
    print("part 2, minimum location: "
          f"{min_location_2(seed_intervals(seeds), maps)}")
