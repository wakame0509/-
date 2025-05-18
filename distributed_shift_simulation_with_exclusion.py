import pandas as pd
import eval7
import random
from calculate_winrate import run_winrate_evolution
from utils import classify_hand, generate_deck, remove_known_cards

def run_distributed_simulation(
    target_groups,
    flop_file="flop30.csv",
    output="results.csv",
    trials=10000,
    range_list=None,
    exclude_4players=True
):
    df_results = []

    deck_master = generate_deck()
    flop_df = pd.read_csv(flop_file)
    flops = [row['Flop'].split() for _, row in flop_df.iterrows()]

    for group in target_groups:
        print(f"Running group: {group}")
        hands = classify_hand(group)

        for hand in hands:
            card1, card2 = hand[0:2], hand[2:4]

            for flop in flops:
                board = flop.copy()

                for _ in range(trials):
                    deck = deck_master.copy()
                    known = [card1, card2] + board
                    deck = remove_known_cards(deck, known)

                    # ランダムに4人分（8枚）を除外
                    if exclude_4players:
                        random.shuffle(deck)
                        excluded = deck[:8]
                        deck = deck[8:]
                    else:
                        excluded = []

                    result = run_winrate_evolution(
                        p1_card1=card1,
                        p1_card2=card2,
                        board=board,
                        selected_range=range_list,
                        extra_excluded=excluded,
                        num_simulations=1
                    )

                    df_results.append({
                        "Hand": hand,
                        "Flop": " ".join(flop),
                        "Preflop": result["Preflop"],
                        "FlopWinrate": result["FlopWinrate"],
                        "TurnWinrate": result["TurnWinrate"],
                        "RiverWinrate": result["RiverWinrate"],
                        "ShiftFlop": result["ShiftFlop"],
                        "ShiftTurn": result["ShiftTurn"],
                        "ShiftRiver": result["ShiftRiver"],
                        "Group": group
                    })

    pd.DataFrame(df_results).to_csv(output, index=False)
    print(f"Saved: {output}")
