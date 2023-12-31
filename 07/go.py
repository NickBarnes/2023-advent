ranks = {c:i for i,c in enumerate('23456789TJQKA')}
j_ranks = {c:i for i,c in enumerate('J23456789TQKA')}

@functools.total_ordering
class Hand:
    def __init__(self, hand, jokers):
        self.hand = hand
        self.ranks = [(j_ranks if jokers else ranks)[c] for c in hand]
        c = Counter(hand)
        if jokers:
            self.jokers = c['J']
            del c['J']
        else:
            self.jokers = 0
        # fundamental hand type ('kind') is the size of the maximum set
        self.kind = max(c.values(), default=0) + self.jokers
        # two exceptions, which we can represent with intermediate values
        if self.kind == 3 and len(c) == 2: # only two card types
            self.kind = 3.5 # full house
        elif self.kind == 2 and len(c) == 3: # only three card types
            self.kind = 2.5 # two pair

    def __eq__(self, other):
        return self.hand == other.hand

    def __gt__(self, other):
        return ((self.kind, self.ranks) >
                (other.kind, other.ranks))
    
    def __repr__(self):
        return f"<{self.hand}, {self.kind}({self.jokers})>"

def winnings(lines, jokers = False):
    # pair all hands with their initial indices, and sort by hand
    ranked = sorted((Hand(h, jokers), i, int(b))
                    for i, (h, b) in enumerate(lines))
    # enumerate the ranking, multiply rank by the bid
    return sum((k+1) * b for k, (_, i ,b) in enumerate(ranked))

def go(input):
    lines = parse.words(input)
    print("part 1, winnings:", winnings(lines))
    print("part 2, winnings with jokers:", winnings(lines, jokers = True))
