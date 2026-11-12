from content_engine.models import Idea, Score
from content_engine.scoring import clamp_score, rank, select_top


def idea(i: int) -> Idea:
    return Idea(id=i, title=f"Idea {i}", hook="h", format="reel", summary="s")


def test_clamp_score_keeps_scores_within_one_to_ten():
    assert clamp_score(0) == 1
    assert clamp_score(14) == 10
    assert clamp_score("7") == 7
    assert clamp_score("not a number") == 1


def test_total_is_mean_of_three_criteria():
    assert Score(1, 9, 6, 6, "").total == 7.0


def test_rank_orders_by_total_then_originality():
    ideas = [idea(1), idea(2), idea(3)]
    scores = {
        1: Score(1, 5, 5, 5, ""),
        2: Score(2, 6, 9, 9, ""),  # total 8.0, originality 6
        3: Score(3, 9, 8, 7, ""),  # total 8.0, originality 9 -> wins the tie
    }
    assert [i.id for i, _ in rank(ideas, scores)] == [3, 2, 1]


def test_unscored_idea_ranks_last_with_minimum_scores():
    ranked = rank([idea(1), idea(2)], {2: Score(2, 3, 3, 3, "")})
    assert [i.id for i, _ in ranked] == [2, 1]
    assert ranked[-1][1].total == 1.0


def test_select_top_returns_first_n():
    ranked = rank([idea(i) for i in range(1, 6)], {})
    assert len(select_top(ranked, 3)) == 3
    assert len(select_top(ranked, 10)) == 5
