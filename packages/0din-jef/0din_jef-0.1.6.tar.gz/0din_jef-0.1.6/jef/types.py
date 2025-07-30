from typing import TypedDict, List, NotRequired, Dict

class ScoreType(TypedDict):
    score: float
    percentage: float
    total_possible_score: NotRequired[int]
    missing: NotRequired[List[str]]
    matches: NotRequired[List[str]]


class CopyrightScoreType(ScoreType):
    ngram_scores: NotRequired[float]
    sentence_scores: NotRequired[float]
    last_analysis_scores: NotRequired[Dict[str, any]]