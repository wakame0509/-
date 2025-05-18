import eval7
from itertools import combinations

def evaluate_hand(cards):
    return eval7.evaluate(cards)

def generate_deck():
    ranks = '23456789TJQKA'
    suits = 'cdhs'
    return [r + s for r in ranks for s in suits]

def remove_known_cards(deck, known_cards):
    return [card for card in deck if card not in known_cards]

def generate_possible_hands(deck, n=2):
    return list(combinations(deck, n))

def convert_str_to_eval7(cards):
    return [eval7.Card(c) for c in cards]

def run_winrate_evolution(hero_hand, board, opp_range, num_trials=10000, exclude_4players=False):
    wins = 0
    ties = 0
    total = 0

    hero_eval = convert_str_to_eval7(hero_hand)
    board_eval = convert_str_to_eval7(board)
    known = set(hero_hand + board)

    full_deck = generate_deck()
    deck = remove_known_cards(full_deck, known)

    if exclude_4players:
        # 4人分（8枚）を除外
        all_exclusions = list(combinations(deck, 8))
        deck = deck.copy()  # copy is safer
        for excl_cards in all_exclusions[:1]:  # 簡易的に最初の1通り
            excluded = set(excl_cards)
            sim_deck = [c for c in deck if c not in excluded]
            result = _simulate_trials(hero_eval, board_eval, sim_deck, opp_range, num_trials)
            wins += result[0]
            ties += result[1]
            total += result[2]
    else:
        result = _simulate_trials(hero_eval, board_eval, deck, opp_range, num_trials)
        wins += result[0]
        ties += result[1]
        total += result[2]

    return (wins + ties / 2) / total * 100 if total > 0 else 0.0

def _simulate_trials(hero_eval, board_eval, deck, opp_range, num_trials):
    import random
    wins = 0
    ties = 0
    total = 0

    for _ in range(num_trials):
        sim_deck = deck.copy()
        random.shuffle(sim_deck)

        if opp_range:
            opp_hand = random.choice(opp_range)
        else:
            opp_hand = [sim_deck.pop(), sim_deck.pop()]

        opp_eval = convert_str_to_eval7(opp_hand)
        missing = 5 - len(board_eval)
        rem_board = convert_str_to_eval7([sim_deck.pop() for _ in range(missing)])
        full_board = board_eval + rem_board

        p1 = hero_eval + full_board
        p2 = opp_eval + full_board

        s1 = evaluate_hand(p1)
        s2 = evaluate_hand(p2)

        if s1 > s2:
            wins += 1
        elif s1 == s2:
            ties += 1
        total += 1

    return wins, ties, total
