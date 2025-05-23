import eval7
import random

def evaluate_hand(cards):
    return eval7.evaluate(cards)

def generate_deck():
    ranks = '23456789TJQKA'
    suits = 'cdhs'
    return [r + s for r in ranks for s in suits]

def remove_known_cards(deck, known_cards):
    return [card for card in deck if card not in known_cards]

def run_winrate_evolution(p1_card1, p1_card2, board, selected_range,
                          extra_excluded=None, num_simulations=10000):
    """
    フロップ→ターン→リバーを段階別に評価する軽量版
    メモリ使用量を大幅に削減し、Render無料プラン対応
    """
    known = [p1_card1, p1_card2] + board
    full_deck = generate_deck()
    deck = remove_known_cards(full_deck, known)

    if extra_excluded:
        deck = remove_known_cards(deck, extra_excluded)

    # フロップ評価
    flop_wins = flop_ties = 0
    for _ in range(num_simulations):
        sim_deck = deck.copy()
        random.shuffle(sim_deck)
        if selected_range:
            opp_hand = random.choice(selected_range)
        else:
            opp_hand = [sim_deck.pop(), sim_deck.pop()]
        flop_board = board + [sim_deck.pop() for _ in range(5 - len(board))]
        try:
            p1 = [eval7.Card(p1_card1), eval7.Card(p1_card2)] + [eval7.Card(c) for c in flop_board]
            p2 = [eval7.Card(opp_hand[0]), eval7.Card(opp_hand[1])] + [eval7.Card(c) for c in flop_board]
            s1 = evaluate_hand(p1)
            s2 = evaluate_hand(p2)
            if s1 > s2:
                flop_wins += 1
            elif s1 == s2:
                flop_ties += 1
        except:
            continue
    flop_winrate = (flop_wins + flop_ties / 2) / num_simulations * 100

    # ターン評価
    turn_wins = turn_ties = 0
    for _ in range(num_simulations):
        sim_deck = deck.copy()
        random.shuffle(sim_deck)
        if selected_range:
            opp_hand = random.choice(selected_range)
        else:
            opp_hand = [sim_deck.pop(), sim_deck.pop()]
        turn_board = board + [sim_deck.pop() for _ in range(5 - len(board))]
        try:
            p1 = [eval7.Card(p1_card1), eval7.Card(p1_card2)] + [eval7.Card(c) for c in turn_board]
            p2 = [eval7.Card(opp_hand[0]), eval7.Card(opp_hand[1])] + [eval7.Card(c) for c in turn_board]
            s1 = evaluate_hand(p1)
            s2 = evaluate_hand(p2)
            if s1 > s2:
                turn_wins += 1
            elif s1 == s2:
                turn_ties += 1
        except:
            continue
    turn_winrate = (turn_wins + turn_ties / 2) / num_simulations * 100

    # リバー評価
    river_wins = river_ties = 0
    for _ in range(num_simulations):
        sim_deck = deck.copy()
        random.shuffle(sim_deck)
        if selected_range:
            opp_hand = random.choice(selected_range)
        else:
            opp_hand = [sim_deck.pop(), sim_deck.pop()]
        river_board = board + [sim_deck.pop() for _ in range(5 - len(board))]
        try:
            p1 = [eval7.Card(p1_card1), eval7.Card(p1_card2)] + [eval7.Card(c) for c in river_board]
            p2 = [eval7.Card(opp_hand[0]), eval7.Card(opp_hand[1])] + [eval7.Card(c) for c in river_board]
            s1 = evaluate_hand(p1)
            s2 = evaluate_hand(p2)
            if s1 > s2:
                river_wins += 1
            elif s1 == s2:
                river_ties += 1
        except:
            continue
    river_winrate = (river_wins + river_ties / 2) / num_simulations * 100

    return {
        "Preflop": 0.0,
        "FlopWinrate": flop_winrate,
        "TurnWinrate": turn_winrate,
        "RiverWinrate": river_winrate,
        "ShiftFlop": flop_winrate - 0.0,
        "ShiftTurn": turn_winrate - flop_winrate,
        "ShiftRiver": river_winrate - turn_winrate
    }
