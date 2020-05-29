from itertools import combinations, permutations
from random import sample, choice
from math import factorial
from numpy import unique, where, asarray, ndarray, mean
from json import dump, load

class Cribbage():
    permu = lambda n, r:factorial(n) / factorial(n - r) #calculate number of permutations
    combi = lambda n, r:factorial(n) / (factorial(n - r) * factorial(r)) #calculate number of combinations

    def __init__(self, deck, verbose = False):
        """Initializes game with simple trackers"""
        self.deck = deck
        self.winning_score = 121

        # player 1 is the starting dealer
        self.hand_count = 1
        self.winner = False

        self.player_1_score = 0
        self.player_2_score = 0

        #for average calculations and sanity checks
        self.hand_scores = list()
        self.crib_scores = list()

    def pegging():
        """In development"""
        pass

    def count_points(self, hand1, hand2, crib, flip, verbose = False,
                    show_movements = False):
        """Counts both player's points and adds them to the scores
        Parameters:
            hand1: Player 1's hand (tuple or list)
            hand2: Player 2's hand (tuple or list)
            crib: Player 1 and 2's discards (tuple or list)
            flip: card flipped up (str) ex "4-C"
        """
        # the non-dealer's hand is counted first
        p1 = 0
        p2 = 0
        if self.hand_count % 2 != 0: # dealer is player 2 if even hand count
            #print("Player 1 deals")
            p2 = Cribbage.score_hand(hand2, flip, verbose)
            self.player_2_score += p2
            if self.player_2_score >= 131:
                self.winner = 2

            p1 = Cribbage.score_hand(hand1, flip, verbose)
            c = Cribbage.score_hand(crib, flip, verbose)
            self.player_1_score += p1 + c
            if self.player_1_score >= 131:
                self.winner = 1
        else:
            #print("Player 2 deals")
            p1 = Cribbage.score_hand(hand1, flip, verbose)
            self.player_1_score += p1
            if self.player_1_score >= 131:
                self.winner = 1

            p2 = Cribbage.score_hand(hand2, flip, verbose)
            c = Cribbage.score_hand(crib, flip, verbose)
            self.player_2_score += p2 + c
            if self.player_2_score >= 131:
                self.winner = 2
        self.hand_scores.extend([p1, p2])
        self.crib_scores.append(c)
        if show_movements:
            print((p1, p2))

    def deal(self):
        """Deals each player 6 cards and stores the flipped card."""
        hands = sample(self.deck, 13) #random sample so no need to shuffle
        hand1, hand2, flip = hands[:6], hands[6:-1], hands[-1]
        return hand1, hand2, flip

    def get_unique_runs(runs):
        """Helper function for score_hand to eliminate subruns
            ex: 4,5,6 in 4,5,6,7
        Parameters:
            runs: list of runs in hand
        returns: all non sub-runs
        """
        subs = list()
        runs_test = sorted([(len(run), run) for run in runs], key=lambda x:x[0], reverse=True)
        for l, run in runs_test:
            is_subrun = False
            for l2, subrun in [subrun for subrun in runs_test if subrun[0]<l]:
                if subrun in permutations(run,l2):
                    subs.append(subrun)
        return set(runs) - set(subs)

    def score_hand(hand, flip, verbose):
        """Calculates the points in a given hand.
        In cribbage, you can get, pairs, fifteens, runs, flushes, and nobs.
        Paramerers
            hand: 4 card hand (tuple or list)
            flip: flipped card (str)
            verbose: True/False
        Returns: total points  (int)
        """
        if type(hand) == tuple:
            hand = list(hand)
        hand = hand + [flip]
        nums = [int(c.split('-')[0]) for c in hand]
        suits = [c.split('-')[1] for c in hand]

        # nobs
        jack = 0
        if 11 in nums:
            flip_suit = flip.split('-')[1]
            for card in hand:
                if card.split('-') == ['11', flip_suit]:
                    jack = 1

        # pairs
        pairs = {i:nums.count(i) for i in nums}
        pair_score = sum([Cribbage.permu(n, 2) for n in pairs.values() if n>1])

        # flush
        if len(unique(suits[:4])) == 1:
            if flip.split('-')[1] == suits[0]:
                flush_score = 5
            else:
                flush_score = 4
        else:
            flush_score = 0

        #fifteens and runs
        fifteens = list()
        runs_raw=list()

        for comb in [combinations(hand, i) for i in list(range(6,1, -1))]:
            for c in (list(comb)):
                #fifteen
                c_adj =  [10 if int(n.split('-')[0])>10 else int(n.split('-')[0]) for n in c] # deals with face cards
                if c not in fifteens and sum(c_adj) == 15:
                    fifteens.append(c)

                # runs
                nums_a = [int(c_.split('-')[0]) for c_ in c]
                l = len(c_adj)
                c_sorted = sorted(c)
                if  l>= 3 and len(unique(nums_a)) == l and (max(nums_a) - min(nums_a)) == (l-1):
                    runs_raw.append(tuple(c_sorted))

        runs = [list(x) for x in Cribbage.get_unique_runs(runs_raw)] # helps in counting points

        fifteen_score = len(fifteens) * 2
        runs_score = len(ndarray.flatten(asarray(runs)))

        if verbose:
            pair_explain = ["{} {}s".format(v, k) for k,v in pairs.items() if v>1]
            s = """Jack: {}\npairs({}): {}\nfifteens({}): {}\nruns({}): {}\nflush: {}"""
            print(s.format(jack, pair_score, pair_explain, fifteen_score,fifteens,
                           runs_score, runs, flush_score))

        return int(jack + pair_score + flush_score + fifteen_score + runs_score)

    def expected_score(hand, deck, verbose=False):
        """Claculates expected score of a hand by averaging possible flips and averaging them."""
        remaining = list(set(deck) - set(hand))
        Ex_scores = []
        for flip in remaining:
            Ex_scores.append(Cribbage.score_hand(hand, flip, verbose))

        return mean(Ex_scores)

    def choose_hand(hand, deck):
        """Selects 4 card hand from hand of 6 based on greatest expected score."""
        possible = list()
        for c in combinations(hand, 4):
            possible.append([Cribbage.expected_score(list(c), deck), c])
        best = max(possible, key = lambda i : i[0])
        discard = list(set(hand) - set(best[1]))
        return best[1], discard
