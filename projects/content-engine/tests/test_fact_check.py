from content_engine.fact_check import check_brief_texts, sensitive_mentions, unsupported_numbers

FACTS = "30 kg weighted vest. Day 3: 5 summits. Movember funds men's mental health and suicide prevention."


def test_numbers_from_the_facts_pass():
    assert unsupported_numbers("30kg on my back, 5 summits", FACTS) == []


def test_invented_numbers_are_flagged():
    assert unsupported_numbers("I'm 15 kg off the mark, 75 men lost this year", FACTS) == ["15", "75"]


def test_numbers_inside_links_and_placeholders_are_ignored():
    assert unsupported_numbers("movember.com/m/15440871 and [fight date 4 Dec]", FACTS) == []


def test_family_and_loss_are_flagged_unless_given_in_the_facts():
    found = sensitive_mentions("I'm doing this for my brother, for the men we lost to suicide", FACTS)
    assert "brother" in found and "lost" in found
    assert "suicide" not in found  # it's in the campaign facts


def test_placeholder_mentions_are_fine():
    assert sensitive_mentions("For [someone close to me]", FACTS) == []


def test_check_brief_texts_quotes_the_sentence_for_each_problem():
    flags = check_brief_texts({"brief-10-voiceover": "Short intro. I'm doing this for my brother. Thanks."}, FACTS)
    assert len(flags) == 1
    assert flags[0].item == "brief-10-voiceover"
    assert flags[0].excerpt == "I'm doing this for my brother."
    assert "brother" in flags[0].message
