from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("shekar")
except PackageNotFoundError:
    __version__ = "unknown"

from .base import BaseTextTransform, BaseTransform
from .classification import (
    InformalLanguageClassifier,
    OffensiveLanguageClassifier,
    SentimentClassifier,
)
from .dep_parsing import DependencyParser
from .embeddings import ContextualEmbedder, WordEmbedder
from .hub import Hub
from .keyword_extraction import KeywordExtractor
from .morphology import Conjugator, Inflector, Lemmatizer, Stemmer
from .ner import NER
from .normalizer import Normalizer
from .pipeline import Pipeline
from .pos import POSTagger
from .spelling import SpellChecker
from .tokenization import SentenceTokenizer, Tokenizer, WordTokenizer
from .transforms import (
    KeyboardNoise,
    NumberToWords,
    OCRNoise,
    Persianizer,
    WhitespaceNoise,
)
from .transliteration import FarsiToTajik, TajikToFarsi

__all__ = [
    "NER",
    "BaseTextTransform",
    "BaseTransform",
    "Conjugator",
    "ContextualEmbedder",
    "DependencyParser",
    "FarsiToTajik",
    "Hub",
    "Inflector",
    "InformalLanguageClassifier",
    "KeyboardNoise",
    "KeywordExtractor",
    "Lemmatizer",
    "Normalizer",
    "NumberToWords",
    "OCRNoise",
    "OffensiveLanguageClassifier",
    "POSTagger",
    "Persianizer",
    "Pipeline",
    "SentenceTokenizer",
    "SentimentClassifier",
    "SpellChecker",
    "Stemmer",
    "TajikToFarsi",
    "Tokenizer",
    "WhitespaceNoise",
    "WordEmbedder",
    "WordTokenizer",
    "__version__",
]
