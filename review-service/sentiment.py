"""
Lightweight sentiment helpers (keyword-based) for demo purposes.
polarity_scores(text) -> {'pos','neg','neu'} in [0,1]
stars(text) -> 1..5
"""
import re
from collections import Counter

_POS_WORDS = {
    "good","great","excellent","amazing","love","loved","like","liked","awesome",
    "fantastic","perfect","happy","satisfied","smooth","quick","friendly","helpful",
    "fast","efficient","fair","easy","recommend","recommended","best","wonderful"
}
_NEG_WORDS = {
    "bad","terrible","awful","hate","hated","poor","slow","unfriendly","rude",
    "worst","disappointing","disappointed","hard","difficult","confusing",
    "broken","buggy","expensive","overpriced","delay","delayed","problem","issues"
}

def _tokenize(text: str):
    return re.findall(r"[a-z']+", (text or "").lower())

def polarity_scores(text: str) -> dict:
    toks = _tokenize(text)
    counts = Counter(toks)
    pos = sum(counts[w] for w in _POS_WORDS)
    neg = sum(counts[w] for w in _NEG_WORDS)
    total = pos + neg
    if total == 0:
        return {"pos": 0.33, "neg": 0.33, "neu": 0.34}
    pos_score = pos / total
    neg_score = neg / total
    neu_score = max(0.0, 1.0 - (pos_score + neg_score))
    s = pos_score + neg_score + neu_score
    return {"pos": pos_score/s, "neg": neg_score/s, "neu": neu_score/s}

def stars(text: str) -> int:
    s = polarity_scores(text)
    pos, neg = s["pos"], s["neg"]
    if pos >= 0.75 and neg <= 0.1:
        return 5
    if pos >= 0.55 and neg <= 0.2:
        return 4
    if neg >= 0.55 and pos <= 0.2:
        return 1
    if neg >= 0.40 and pos <= 0.35:
        return 2
    return 3