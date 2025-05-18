def classify_hand(card1, card2):
    """
    2枚のカード文字列（例："As", "Ah"）からグループを分類して返す
    """
    rank_order = "23456789TJQKA"
    r1, s1 = card1[0], card1[1]
    r2, s2 = card2[0], card2[1]

    if r1 == r2:
        if rank_order.index(r1) >= rank_order.index('T'):
            return "High Pair"
        elif rank_order.index(r1) >= rank_order.index('6'):
            return "Mid Pair"
        else:
            return "Low Pair"
    elif abs(rank_order.index(r1) - rank_order.index(r2)) == 1:
        if s1 == s2:
            return "Suited Connectors"
        else:
            return "Offsuit Connectors"
    elif abs(rank_order.index(r1) - rank_order.index(r2)) == 2:
        if s1 == s2:
            return "Suited Gappers"
        else:
            return "Offsuit Gappers"
    elif r1 == 'A' or r2 == 'A':
        if s1 == s2:
            return "Ace-X Suited"
        else:
            return "Offsuit Non-Connectors"
    else:
        if s1 == s2:
            return "Suited Non-Connectors"
        else:
            return "Junk Hands"

def generate_deck():
    ranks = '23456789TJQKA'
    suits = 'cdhs'
    return [r + s for r in ranks for s in suits]

def remove_known_cards(deck, known_cards):
    return [card for card in deck if card not in known_cards]
