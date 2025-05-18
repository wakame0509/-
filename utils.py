def classify_hand(group):
    """
    グループ名を渡すと、そのグループに属するスターティングハンド一覧を返す。
    """
    groups = {
        "High Pair": ["AA", "KK", "QQ", "JJ"],
        "Mid Pair": ["TT", "99", "88"],
        "Low Pair": ["77", "66", "55", "44", "33", "22"],
        "Broadway": [
            "AKs", "AQs", "AJs", "ATs", "KQs", "KJs", "QJs", "JTs",
            "AKo", "AQo", "AJo", "KQo"
        ],
        "Suited Connectors": ["T9s", "98s", "87s", "76s", "65s", "54s", "43s"],
        "Offsuit Connectors": ["T9o", "98o", "87o", "76o", "65o", "54o", "43o"],
        "Suited Gappers": ["J9s", "97s", "86s", "75s", "64s", "53s"],
        "Offsuit Gappers": ["J9o", "97o", "86o", "75o", "64o", "53o"],
        "Suited Non-Connectors": ["Q9s", "T8s", "94s", "93s"],
        "Offsuit Non-Connectors": ["Q9o", "T8o", "94o", "93o"],
        "Ace-X Suited": ["A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s"],
        "Junk Hands": [
            "32o", "42o", "52o", "62o", "72o", "82o", "92o",
            "T2o", "J2o", "Q2o", "K2o", "32s", "42s"
        ]
    }
    return groups.get(group, [])

def generate_deck():
    """
    52枚のカードデッキを "As", "Kd" の形式で返す
    """
    ranks = '23456789TJQKA'
    suits = 'cdhs'
    return [r + s for r in ranks for s in suits]

def remove_known_cards(deck, known_cards):
    """
    指定されたカードをデッキから除外する
    """
    return [card for card in deck if card not in known_cards]
