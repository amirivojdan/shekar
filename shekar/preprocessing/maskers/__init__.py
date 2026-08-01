from .diacritic_masker import DiacriticMasker
from .digit_masker import DigitMasker
from .email_masker import EmailMasker
from .emoji_masker import EmojiMasker
from .hashtag_masker import HashtagMasker
from .html_tag_masker import HTMLTagMasker
from .mention_masker import MentionMasker
from .non_persian_letter_masker import NonPersianLetterMasker
from .offensive_word_masker import OffensiveWordMasker
from .punctuation_masker import PunctuationMasker
from .stopword_masker import StopWordMasker
from .url_masker import URLMasker

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
    "DiacriticRemover",
    "DigitMasker",
    "DigitRemover",
    "EmailMasker",
    "EmailRemover",
    "EmojiMasker",
    "EmojiRemover",
    "HTMLTagMasker",
    "HTMLTagRemover",
    "HashtagMasker",
    "HashtagRemover",
    "MaskDiacritics",
    "MaskDigits",
    # Maskers
    "MaskEmails",
    "MaskEmojis",
    "MaskHTMLTags",
    "MaskHashtags",
    "MaskMentions",
    "MaskNonPersianLetters",
    "MaskOffensiveWords",
    "MaskPunctuations",
    "MaskStopWords",
    "MaskURLs",
    "MentionMasker",
    "MentionRemover",
    "NonPersianLetterMasker",
    "NonPersianRemover",
    "OffensiveWordMasker",
    "OffensiveWordRemover",
    "PunctuationMasker",
    "PunctuationRemover",
    # action-based aliases
    "RemoveDiacritics",
    "RemoveDigits",
    "RemoveEmails",
    "RemoveEmojis",
    "RemoveHTMLTags",
    "RemoveHashtags",
    "RemoveMentions",
    "RemoveNonPersianLetters",
    "RemoveOffensiveWords",
    "RemovePunctuations",
    "RemoveStopWords",
    "RemoveURLs",
    "RepeatedLetterMasker",
    "StopWordMasker",
    "StopWordRemover",
    "URLMasker",
    "URLRemover",
]
