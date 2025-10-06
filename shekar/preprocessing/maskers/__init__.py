from .email_masker import EmailMasker
from .url_masker import URLMasker
from .diacritic_masker import DiacriticMasker
from .non_persian_letter_masker import NonPersianLetterMasker
from .emoji_masker import EmojiMasker
from .punctuation_masker import PunctuationMasker
from .stopword_masker import StopWordMasker
from .hashtag_masker import HashtagMasker
from .mention_masker import MentionMasker
from .digit_masker import DigitMasker
from .html_tag_masker import HTMLTagMasker
from .offensive_word_masker import OffensiveWordMasker

# aliases
DiacriticRemover = DiacriticMasker
EmojiRemover = EmojiMasker
NonPersianRemover = NonPersianLetterMasker
PunctuationRemover = PunctuationMasker
StopWordRemover = StopWordMasker
HashtagRemover = HashtagMasker
MentionRemover = MentionMasker
DigitRemover = DigitMasker
HTMLTagRemover = HTMLTagMasker
EmailRemover = EmailMasker
URLRemover = URLMasker
OffensiveWordRemover = OffensiveWordMasker


# action-based remover aliases
RemoveDiacritics = DiacriticMasker
RemoveEmojis = EmojiMasker
RemoveNonPersianLetters = NonPersianLetterMasker
RemovePunctuations = PunctuationMasker
RemoveStopWords = StopWordMasker
RemoveHashtags = HashtagMasker
RemoveMentions = MentionMasker
RemoveDigits = DigitMasker
RemoveHTMLTags = HTMLTagMasker
RemoveEmails = EmailMasker
RemoveURLs = URLMasker
RemoveOffensiveWords = OffensiveWordMasker

# action-based Masker aliases
MaskEmails = EmailMasker
MaskURLs = URLMasker
MaskEmojis = EmojiMasker
MaskDigits = DigitMasker
MaskPunctuations = PunctuationMasker
MaskNonPersianLetters = NonPersianLetterMasker
MaskStopWords = StopWordMasker
MaskHashtags = HashtagMasker
MaskMentions = MentionMasker
MaskDiacritics = DiacriticMasker
MaskHTMLTags = HTMLTagMasker
MaskOffensiveWords = OffensiveWordMasker


__all__ = [
    "DiacriticMasker",
    "EmojiMasker",
    "NonPersianLetterMasker",
    "PunctuationMasker",
    "StopWordMasker",
    "HashtagMasker",
    "MentionMasker",
    "DigitMasker",
    "RepeatedLetterMasker",
    "HTMLTagMasker",
    "EmailMasker",
    "URLMasker",
    "OffensiveWordMasker",
    # aliases
    "DiacriticRemover",
    "EmojiRemover",
    "NonPersianRemover",
    "PunctuationRemover",
    "StopWordRemover",
    "HashtagRemover",
    "MentionRemover",
    "DigitRemover",
    "HTMLTagRemover",
    "EmailRemover",
    "URLRemover",
    "OffensiveWordRemover",
    # action-based aliases
    "RemoveDiacritics",
    "RemoveEmojis",
    "RemoveNonPersianLetters",
    "RemovePunctuations",
    "RemoveStopWords",
    "RemoveHashtags",
    "RemoveMentions",
    "RemoveDigits",
    "RemoveHTMLTags",
    "RemoveEmails",
    "RemoveURLs",
    "RemoveOffensiveWords",
    # Maskers
    "MaskEmails",
    "MaskURLs",
    "MaskEmojis",
    "MaskDigits",
    "MaskPunctuations",
    "MaskNonPersianLetters",
    "MaskStopWords",
    "MaskHashtags",
    "MaskMentions",
    "MaskDiacritics",
    "MaskHTMLTags",
    "MaskOffensiveWords",
]
