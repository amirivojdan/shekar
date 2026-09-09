from collections.abc import Iterable
from functools import wraps
from inspect import signature

from .base import BaseTextTransform, BaseTransform


class Pipeline(BaseTransform):
    """
    A class for creating a pipeline of transformations using a sequence of BaseTransformer steps.
    The Pipeline class allows chaining multiple transformation steps, where each step is an instance
    of a class that inherits from BaseTransformer. The pipeline can be used to fit, transform, and
    fit-transform data sequentially through the defined steps.

    Args:
        steps (list[tuple[str, BaseTransformer]]): A list of tuples where each tuple contains a
            string (name of the step) and an instance of a BaseTransformer.

    Methods:
        fit(X, y=None):
            Fits each step in the pipeline sequentially using the input data X and optional target y.
        transform(X):
            Transforms the input data X sequentially through each step in the pipeline.
        fit_transform(X, y=None):
            Fits and transforms the input data X sequentially through each step in the pipeline.
            Supports both single string input and a list of strings.
        __call__(X):
            Allows the pipeline to be called as a function, fitting and transforming the input data X.

    Attributes:
        steps (list[tuple[str, BaseTransformer]]) or list[BaseTransformer]:
            A list of tuples where each tuple contains a string (name of the step) and an instance
            of a BaseTransformer. If only BaseTransformer instances are provided, they are wrapped
            in tuples with their class names as the step names.
    Example:

        >>> pipeline = Pipeline([
                    ("AlphaNumericUnifier", AlphabetNormalizer()),
                    ("ArabicUnicodeNormalizer", ArabicUnicodeNormalizer()),
                    ("NumericNormalizer", NumericNormalizer()),
                    ("PunctuationUnifier", PunctuationNormalizer()),
                    ("EmailMasker", EmailMasker(mask="")),
                    ("URLMasker", URLMasker(mask="")),
                    ("EmojiRemover", EmojiRemover()),
                    ("HTMLTagRemover", HTMLTagRemover()),
                    ("DiacriticsRemover", DiacriticsRemover()),
                    ("RedundantCharacterRemover", RedundantCharacterRemover()),
                    ("NonPersianRemover", NonPersianRemover()),
                    ("SpacingStandardizer", SpacingStandardizer()),
        ])
        >>> result = pipeline("🌹 باز هم مرغ سحر🐔 بر سر منبر گل ")
        >>> print(result)
        باز هم مرغ سحر بر سر منبر گل
    """

    supports_batching = True

    def __init__(
        self,
        steps: Iterable[tuple[str, BaseTransform]] | Iterable[BaseTransform],
        *,
        batch_size=None,
    ):
        self._batch_size_override = (
            None if batch_size is None else self._validate_batch_size(batch_size)
        )
        if not isinstance(steps, Iterable):
            raise TypeError(
                "steps must be a list of tuples (name, transformer) or a list of transformers."
            )
        steps = list(steps)

        if all(isinstance(step, BaseTransform) for step in steps):
            self.steps = [(step.__class__.__name__, step) for step in steps]

        elif all(
            isinstance(step, tuple)
            and len(step) == 2
            and isinstance(step[1], BaseTransform)
            and isinstance(step[0], str)
            for step in steps
        ):
            self.steps = steps

        else:
            raise TypeError(
                "steps must be a list of tuples (name, transformer) or a list of transformers."
            )

        self.batch_size = self._batch_size_override or max(
            (getattr(step, "batch_size", 1) for _, step in self.steps), default=32
        )

    def fit(self, X, y=None):
        for name, step in self.steps[:-1]:
            X = step.fit_transform(X, y)
        if self.steps:
            self.steps[-1][1].fit(X, y)
        return self

    def transform(self, X):
        if self._uses_batching() and not isinstance(X, str) and isinstance(X, Iterable):
            return self._iter_batches(X, fit=False)
        for name, step in self.steps:
            X = step.transform(X)
        return X

    def fit_transform(self, X, y=None):
        if isinstance(X, str):
            for name, step in self.steps:
                X = step.fit_transform(X, y)
            return X
        elif isinstance(X, Iterable):
            return self._iter_batches(X, fit=True, y=y)

        else:
            raise TypeError("Input must be a string or a list of strings.")

    def _uses_batching(self):
        return any(
            step._uses_batching()
            if isinstance(step, Pipeline)
            else getattr(step, "supports_batching", False) is True
            for _, step in self.steps
        )

    def _iter_batches(self, texts, *, fit, y=None):
        for batch in self._text_batches(texts, self.batch_size):
            for _, step in self.steps:
                # Recurse only through the standard Pipeline implementation;
                # bypassing a subclass override would discard its custom behavior.
                if (
                    isinstance(step, Pipeline)
                    and type(step).fit_transform is Pipeline.fit_transform
                    and type(step).transform is Pipeline.transform
                ):
                    batch = list(step._iter_batches(batch, fit=fit, y=y))
                elif getattr(step, "supports_batching", False) is True and (
                    not fit
                    or type(step).fit in (BaseTransform.fit, BaseTextTransform.fit)
                ):
                    batch = step.transform_batch(batch)
                else:
                    # Preserve custom/stateful transformers' per-item fitting semantics.
                    batch = [
                        step.fit_transform(item, y) if fit else step.transform(item)
                        for item in batch
                    ]
            yield from batch

    def _transform_batch(self, texts, batch_size):
        batch = texts
        for _, step in self.steps:
            if getattr(step, "supports_batching", False) is True:
                batch = step.transform_batch(batch, batch_size=batch_size)
            else:
                batch = [step.transform(item) for item in batch]
        return batch

    def __call__(self, X):
        return self.fit_transform(X)

    def __or__(self, other):
        if isinstance(other, Pipeline):
            return Pipeline(
                self.steps + other.steps,
                batch_size=self._batch_size_override
                if self._batch_size_override is not None
                else other._batch_size_override,
            )
        elif isinstance(other, BaseTransform):
            return Pipeline(
                self.steps + [(other.__class__.__name__, other)],
                batch_size=self._batch_size_override,
            )
        else:
            raise TypeError(
                f"Unsupported type for pipeline concatenation: {type(other)}"
            )

    def __ror__(self, other):
        if isinstance(other, Pipeline):
            return Pipeline(
                other.steps + self.steps,
                batch_size=other._batch_size_override
                if other._batch_size_override is not None
                else self._batch_size_override,
            )
        elif isinstance(other, BaseTransform):
            return Pipeline(
                [(other.__class__.__name__, other)] + self.steps,
                batch_size=self._batch_size_override,
            )
        else:
            raise TypeError(
                f"Unsupported type for pipeline concatenation: {type(other)}"
            )

    def __str__(self):
        return repr(self)

    def __repr__(self):
        steps_repr = ", ".join(f"({name!r}, {step!r})" for name, step in self.steps)
        return f"Pipeline(steps=[{steps_repr}])"

    def on_args(self, param_names):
        """
        Returns a decorator that applies this pipeline to one or more function arguments.

        Args:
            param_names (str or Iterable[str]): The name(s) of the function parameter(s) to be transformed.
                If a string is provided, it will be treated as a single parameter name.
                If an iterable is provided, each item will be treated as a separate parameter name.
        Returns:
            function: A decorator that applies the pipeline to the specified function arguments.

        Raises:
            TypeError: If param_names is not a string or an iterable of strings.
            ValueError: If a specified parameter name is not found in the function arguments.

        Example:
            @normalizer.on_args("text")
            def process_text(text):
                # text will be normalized before being passed to this function
                print(text)

            @normalizer.on_args(["text", "description"])
            def process_text_and_description(text, description):
                # both text and description will be normalized before being passed to this function
                print(text, description)
        """
        if isinstance(param_names, str):
            param_names = [param_names]
        elif not isinstance(param_names, Iterable) or not all(
            isinstance(p, str) for p in param_names
        ):
            raise TypeError("param_names must be a string or an iterable of strings")

        pipeline_instance = self

        def decorator(func):
            sig = signature(func)

            @wraps(func)
            def wrapper(*args, **kwargs):
                bound = sig.bind(*args, **kwargs)
                bound.apply_defaults()

                for name in param_names:
                    if name in bound.arguments:
                        bound.arguments[name] = pipeline_instance(bound.arguments[name])
                    else:
                        raise ValueError(
                            f"Parameter '{name}' not found in function arguments."
                        )

                return func(*bound.args, **bound.kwargs)

            return wrapper

        return decorator
