from shekar.classification.informal_rule_based import RuleBasedInformalClassifier


def test_informal_sentence():
    classifier = RuleBasedInformalClassifier()
    assert classifier.is_informal("نون بگیر بیار داری میای خونه") is True


def test_threshold():
    classifier = RuleBasedInformalClassifier(occurrence_threshold=5)
    assert classifier.is_informal("نون بگیر بیار داری میای خونه") is False


def test_formal_sentence():
    classifier = RuleBasedInformalClassifier()
    assert classifier.is_informal("من به خانه می‌آیم") is False
