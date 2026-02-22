from shekar.transforms import (
    Flatten,
)


def test_flatten():
    flatten = Flatten()
    input_text = [
        ["سلام", "دوست"],
        ["خوبی؟", "چطوری؟"],
    ]
    expected_output = ["سلام", "دوست", "خوبی؟", "چطوری؟"]
    assert list(flatten(input_text)) == expected_output

    input_text = [
        ["سلام", "دوست"],
        ["خوبی؟", "چطوری؟"],
        ["من خوبم", "شما چطورید؟"],
    ]
    expected_output = ["سلام", "دوست", "خوبی؟", "چطوری؟", "من خوبم", "شما چطورید؟"]
    assert list(flatten(input_text)) == expected_output
