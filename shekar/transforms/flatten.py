from shekar.base import BaseTransform
from typing import Iterable


class Flatten(BaseTransform):
    """
    A transformer that flattens a nested iterable of strings into a generator of strings.
    """

    def transform(self, X: Iterable) -> Iterable[str]:
        """
        Flattens a nested iterable structure into a generator of strings.

        Args:
            X: An iterable that may contain nested iterables of strings

        Returns:
            Iterable[str]: A generator yielding all string items
        """

        def _flatten(items):
            for item in items:
                if isinstance(item, str):
                    yield item
                elif isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
                    yield from _flatten(item)

        return _flatten(X)
