import eval7

def evaluate_hand(cards):
    """
    7枚のeval7カードオブジェクトを受け取り、強さを返す
    """
    return eval7.evaluate(cards)

def generate_deck():
    """
    52枚のデッキを生成（"As", "Kd", ... 形式）
    """
    ranks = '23456789TJQKA'
    suits = 'cdhs'
    return [r + s for r in ranks for s in suits]

def remove_known_cards(deck, known_cards):
    """
    デッキから既に使われているカードを除外
    """
    return [card for card in deck if card not in known_cards]

def generate_possible_hands(deck, n=2):
    """
    デッキからn枚のカード組み合わせを全通り生成（デフォルトは2枚＝ハンド）
    """
    from itertools import combinations
    return list(combinations(deck, n))

def convert_str_to_eval7(cards):
    """
    文字列カード（例: "As"）を eval7.Card オブジェクトに変換
    """
    return [eval7.Card(c) for c in cards]
