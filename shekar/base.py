from abc import ABC, abstractmethod
from typing import Iterable, List
import re


class BaseTransform(ABC):
    @abstractmethod
    def transform(self, X):
        raise NotImplementedError("Subclasses must implement transform()")

    def fit(self, X, y=None):
        """
        Fit the transform to the data. This method can be overridden by subclasses
        if they need to perform any fitting operation.
        """
        return self

    def fit_transform(self, X, y=None):
        self.fit(X, y)
        return self.transform(X)

    def __call__(self, *args, **kwds):
        return self.fit_transform(*args, **kwds)

    def __or__(self, value):
        from shekar.pipeline import Pipeline

        if isinstance(value, Pipeline):
            return Pipeline(steps=[(self.__class__.__name__, self)] + value.steps)
        elif isinstance(value, BaseTransform):
            return Pipeline(
                steps=[
                    self,
                    value,
                ]
            )
        else:
            raise TypeError(
                f"Unsupported type for pipeline concatenation: {type(value)}"
            )

    def __ror__(self, value):
        from shekar.pipeline import Pipeline

        if isinstance(value, Pipeline):
            return Pipeline(steps=value.steps + [(self.__class__.__name__, self)])
        elif isinstance(value, BaseTransform):
            return Pipeline(
                steps=[
                    value,
                    self,
                ]
            )
        else:
            raise TypeError(
                f"Unsupported type for pipeline concatenation: {type(value)}"
            )

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class BaseTextTransform(BaseTransform):
    @abstractmethod
    def _function(self, X: str, y=None) -> Iterable[str] | str:
        raise NotImplementedError("Subclasses must implement _function()")

    def transform(self, X: Iterable[str] | str) -> Iterable[str] | str:
        if isinstance(X, str):
            return self._function(X)
        elif isinstance(X, Iterable):
            return (self._function(x) for x in X)
        else:
            raise ValueError("Input must be a string or a Iterable of strings.")

    def fit(self, X: Iterable[str] | str, y=None):
        return self

    def fit_transform(self, X: Iterable[str] | str, y=None):
        return self.transform(X)

    @classmethod
    def _compile_patterns(
        cls, mappings: Iterable[tuple[str, str]], flags: int = re.UNICODE
    ) -> List[tuple[re.Pattern, str]]:
        """
        Compiles a list of regex patterns and their corresponding replacement strings.
        This method takes an iterable of tuples, where each tuple contains a regex pattern
        string and a replacement string. It compiles the regex patterns into `re.Pattern`
        objects and pairs them with their respective replacement strings.
        Args:
            cls: The class on which this method is called.
            mappings (Iterable[tuple[str, str]]): An iterable of tuples, where each tuple
                consists of a regex pattern string and a replacement string.
        Returns:
            List[tuple[re.Pattern, str]]: A list of tuples, where each tuple contains a
            compiled regex pattern (`re.Pattern`) and its corresponding replacement string.
        """
        compiled_patterns = [
            (re.compile(pattern, flags=flags), replacement)
            for pattern, replacement in mappings
        ]
        return compiled_patterns

    @classmethod
    def _map_patterns(
        cls, text: str, patterns: Iterable[tuple[re.Pattern, str]]
    ) -> str:
        for pattern, replacement in patterns:
            text = pattern.sub(replacement, text)
        return text

    @classmethod
    def _create_translation_table(
        cls, mappings: Iterable[tuple[str, str]]
    ) -> dict[int, str | None]:
        trans: dict[int, str | None] = {}
        for chars, repl in mappings:
            for ch in chars:
                trans[ord(ch)] = repl
        return trans
