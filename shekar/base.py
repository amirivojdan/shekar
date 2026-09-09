import re
import warnings
from abc import ABC, abstractmethod
from collections.abc import Iterable, Mapping
from itertools import islice
from numbers import Integral


class BaseTransform(ABC):
    supports_batching = False

    @staticmethod
    def _validate_batch_size(batch_size):
        if (
            isinstance(batch_size, bool)
            or not isinstance(batch_size, Integral)
            or batch_size < 1
        ):
            raise ValueError("batch_size must be a positive integer.")
        return int(batch_size)

    @classmethod
    def _text_batches(cls, texts, batch_size):
        size = cls._validate_batch_size(batch_size)
        if isinstance(texts, (str, bytes, Mapping)) or not isinstance(texts, Iterable):
            raise TypeError("Expected an iterable of strings.")
        iterator = iter(texts)
        while batch := list(islice(iterator, size)):
            if not all(isinstance(text, str) for text in batch):
                raise TypeError("Every batch item must be a string.")
            yield batch

    @classmethod
    def _session_batch_size(cls, session, requested):
        """Respect legacy custom models with a fixed batch dimension of one."""
        size = cls._validate_batch_size(requested)
        # These adapters own these batch-bearing inputs. Auxiliary inputs may
        # have static leading dimensions unrelated to the number of documents.
        input_names = {
            "input_ids",
            "attention_mask",
            "token_type_ids",
            "word_to_first_subtoken",
            "input_text",
        }
        if "_shekar_batch_limit" not in vars(session):
            fixed = set()
            for item in session.get_inputs():
                if item.name not in input_names:
                    continue
                shape = item.shape
                if shape and isinstance(shape[0], int) and shape[0] > 0:
                    fixed.add(shape[0])
            if fixed - {1}:
                raise ValueError(
                    "Only dynamic batch dimensions or a fixed batch of 1 are supported."
                )
            session._shekar_batch_limit = 1 if fixed else None
            session._shekar_batch_warned = False
        if session._shekar_batch_limit == 1:
            if size > 1 and not session._shekar_batch_warned:
                warnings.warn(
                    "This ONNX model has a fixed batch size of 1; inference will run "
                    "one sequence at a time. Use a model exported with dynamic batching.",
                    RuntimeWarning,
                    stacklevel=2,
                )
                session._shekar_batch_warned = True
            return 1
        return size

    def transform_batch(self, texts, *, batch_size=None):
        """Transform bounded groups of texts, preserving input order.

        Subclasses implement ``_transform_batch`` and opt into pipeline batching
        with ``supports_batching = True``. Other transforms retain a per-item
        fallback and their existing pipeline behavior.
        """
        size = self._validate_batch_size(
            getattr(self, "batch_size", 32) if batch_size is None else batch_size
        )
        return [
            result
            for batch in self._text_batches(texts, size)
            for result in self._transform_batch(batch, size)
        ]

    def _transform_batch(self, texts, batch_size):
        return [self.transform(text) for text in texts]

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
            return Pipeline(
                steps=[(self.__class__.__name__, self)] + value.steps,
                batch_size=value._batch_size_override,
            )
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
            return Pipeline(
                steps=value.steps + [(self.__class__.__name__, self)],
                batch_size=value._batch_size_override,
            )
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
            raise TypeError("Input must be a string or a Iterable of strings.")

    def fit(self, X: Iterable[str] | str, y=None):
        return self

    def fit_transform(self, X: Iterable[str] | str, y=None):
        return self.transform(X)

    @classmethod
    def _compile_patterns(
        cls, mappings: Iterable[tuple[str, str]], flags: int = re.UNICODE
    ) -> list[tuple[re.Pattern, str]]:
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
