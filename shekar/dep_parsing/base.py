from shekar.base import BaseTransform
from .albert_dep_parser import AlbertDepParser

DEP_PARSER_REGISTRY = {
    "albert": AlbertDepParser,
}


class DependencyParser(BaseTransform):
    def __init__(self, model: str = "albert", model_path=None):
        model = model.lower()
        if model not in DEP_PARSER_REGISTRY:
            raise ValueError(
                f"Unknown dependency parser model '{model}'. Available: {list(DEP_PARSER_REGISTRY.keys())}"
            )
        self.model = DEP_PARSER_REGISTRY[model](model_path=model_path)

    def transform(self, X: str) -> list:
        return self.model.transform(X)

    def print_tree(self, results: list[tuple[str, int, str]]):
        """Print a dependency parse result as a tree to stdout."""
        if not results:
            return

        n = len(results)
        children: dict[int, list[int]] = {i: [] for i in range(n + 1)}
        for i, (_, head, _) in enumerate(results):
            children[head].append(i + 1)

        def _print_node(node_idx: int, prefix: str, is_last: bool):
            connector = "└── " if is_last else "├── "
            if node_idx == 0:
                print("ROOT")
            else:
                word, _, deprel = results[node_idx - 1]
                print(f"{prefix}{connector}[{deprel}] {word}")

            child_prefix = prefix + ("    " if is_last else "│   ")
            kids = children[node_idx]
            for j, child in enumerate(kids):
                _print_node(child, child_prefix, j == len(kids) - 1)

        _print_node(0, "", True)
