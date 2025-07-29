from .diacritic_filter import DiacriticFilter
from .emoji_filter import EmojiFilter
from .non_persian_letter_filter import NonPersianLetterFilter
from .punctuation_filter import PunctuationFilter
from .stopword_filter import StopWordFilter
from .hashtag_filter import HashtagFilter
from .mention_filter import MentionFilter
from .digit_filter import DigitFilter
from .repeated_letter_filter import RepeatedLetterFilter
from .html_tag_filter import HTMLTagFilter

# aliases
DiacriticRemover = DiacriticFilter
EmojiRemover = EmojiFilter
NonPersianRemover = NonPersianLetterFilter
PunctuationRemover = PunctuationFilter
StopWordRemover = StopWordFilter
HashtagRemover = HashtagFilter
MentionRemover = MentionFilter
DigitRemover = DigitFilter
RepeatedLetterRemover = RepeatedLetterFilter
HTMLRemover = HTMLTagFilter

# action-based aliases
RemoveDiacritics = DiacriticFilter
RemoveEmojis = EmojiFilter
RemoveNonPersianLetters = NonPersianLetterFilter
RemovePunctuations = PunctuationFilter
RemoveStopWords = StopWordFilter
RemoveHashtags = HashtagFilter
RemoveMentions = MentionFilter
RemoveDigits = DigitFilter
RemoveRepeatedLetters = RepeatedLetterFilter
RemoveHTMLTags = HTMLTagFilter


__all__ = [
    "DiacriticFilter",
    "EmojiFilter",
    "NonPersianLetterFilter",
    "PunctuationFilter",
    "StopWordFilter",
    "HashtagFilter",
    "MentionFilter",
    "DigitFilter",
    "RepeatedLetterFilter",
    "HTMLTagFilter",
    # aliases
    "DiacriticRemover",
    "EmojiRemover",
    "NonPersianRemover",
    "PunctuationRemover",
    "StopWordRemover",
    "HashtagRemover",
    "MentionRemover",
    "DigitRemover",
    "RepeatedLetterRemover",
    "HTMLRemover"
    # action-based aliases
    "RemoveDiacritics",
    "RemoveEmojis",
    "RemoveNonPersianLetters",
    "RemovePunctuations",
    "RemoveStopWords",
    "RemoveHashtags",
    "RemoveMentions",
    "RemoveDigits",
    "RemoveRepeatedLetters",
    "RemoveHTMLTags",
]
