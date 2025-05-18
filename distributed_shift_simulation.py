import os
import pandas as pd
import eval7
import random
from itertools import combinations

# --- ハンド分類（12分類例） ---
def classify_hand(card1, card2):
    ranks = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8,
             '9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}
    r1, r2 = card1[0], card2[0]
    s1, s2 = card1[1], card2[1]
    if r1 == r2:
        if r1 in 'A K Q J'.split():
            return 'High Pair'
        elif r1 in 'T 9 8 7'.split():
            return 'Mid Pair'
        else:
            return 'Low Pair'
    elif abs(ranks[r1] - ranks[r2]) == 1:
        return 'Suited Connectors' if s1 == s2 else 'Offsuit Connectors'
    elif ranks[r1] + ranks[r2] >= 24:
        return 'Broadway'
    elif s1 == s2:
        return 'Suited Non-Connectors'
    else:
        return 'Offsuit Non-Connectors'

# --- 評価 ---
def evaluate(cards):
    return eval7.evaluate([eval7.Card(c) for c in cards])

# --- モンテカルロ勝率計算 ---
def monte_carlo(hand, board, trials):
    wins = ties = 0
    deck = [r + s for r in '23456789TJQKA' for s in 'cdhs']
    for card in hand + board:
        deck.remove(card)

    for _ in range(trials):
        random.shuffle(deck)
        opp = deck[:2]
        remain = deck[2:7 - len(board)]
        full_board = board + remain
        p1 = hand + full_board
        p2 = opp + full_board
        score1 = evaluate(p1)
        score2 = evaluate(p2)
        if score1 > score2:
            wins += 1
        elif score1 == score2:
            ties += 1
    return round((wins + ties / 2) / trials * 100, 2)

# --- フロップ→ターン→リバー勝率変動記録 ---
def simulate_shift(card1, card2, flop_list, turn_list, river_list, trials=10000):
    results = []
    base_hand = [card1, card2]
    for flop in flop_list:
        flop_cards = flop.split()
        base_deck = [r + s for r in '23456789TJQKA' for s in 'cdhs']
        known = set(base_hand + flop_cards)
        deck = [c for c in base_deck if c not in known]

        pre = monte_carlo(base_hand, [], trials)
        post_flop = monte_carlo(base_hand, flop_cards, trials)

        for turn in turn_list:
            if turn in known: continue
            turn_board = flop_cards + [turn]
            for river in river_list:
                if river in known or river == turn: continue
                full_board = flop_cards + [turn, river]
                post_turn = monte_carlo(base_hand, turn_board, trials)
                post_river = monte_carlo(base_hand, full_board, trials)
                results.append({
                    "Hand": f"{card1} {card2}",
                    "Group": classify_hand(card1, card2),
                    "Flop": ' '.join(flop_cards),
                    "Turn": turn,
                    "River": river,
                    "Preflop": pre,
                    "FlopWinrate": post_flop,
                    "TurnWinrate": post_turn,
                    "RiverWinrate": post_river,
                    "ShiftFlop": post_flop - pre,
                    "ShiftTurn": post_turn - post_flop,
                    "ShiftRiver": post_river - post_turn
                })
    return results

# --- 分担実行 ---
def run_distributed_simulation(target_groups, flop_file="flop30.csv", output="results.csv", trials=10000):
    flop_df = pd.read_csv(flop_file)
    flop_list = flop_df["Flop"].tolist()
    all_turns = [r + s for r in '23456789TJQKA' for s in 'cdhs']
    all_rivers = all_turns.copy()
    deck = [r + s for r in '23456789TJQKA' for s in 'cdhs']
    all_hands = list(combinations(deck, 2))
    filtered_hands = [h for h in all_hands if classify_hand(h[0], h[1]) in target_groups]

    all_results = []
    for h1, h2 in filtered_hands:
        all_results.extend(simulate_shift(h1, h2, flop_list, all_turns, all_rivers, trials=trials))

    pd.DataFrame(all_results).to_csv(output, index=False)
    print(f"保存完了: {output}")
