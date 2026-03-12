# Dependency Parsing

The `DependencyParser` class provides syntactic dependency parsing for Persian text using a transformer-based model (default: **ALBERT**). It analyzes the grammatical structure of a sentence and returns, for each word, its syntactic head (1-indexed, where 0 means ROOT) and the dependency relation label following the **Universal Dependencies (UD)** standard.

**Features**

- **Transformer-based model** for high accuracy
- **Universal Dependencies** relation labels following the UD standard
- Tree visualization via `print_tree()`
- Easy-to-use Python interface

**Example Usage**

```python
from shekar import DependencyParser

parser = DependencyParser()
text = "ما با آنچه می‌سازیم ایرانی هستیم."

result = parser(text)
for word, head, deprel in result:
    print(f"{word} ← (head: {head}, relation: {deprel})")
```

```shell
ما ← (head: 6, relation: nsubj)
با ← (head: 3, relation: case)
آنچه ← (head: 6, relation: obl)
می‌سازیم ← (head: 3, relation: acl)
ایرانی ← (head: 6, relation: xcomp)
هستیم ← (head: 0, relation: root)
. ← (head: 6, relation: punct)
```

## Tree Visualization

You can visualize the parse result as a readable tree structure using `print_tree()`:

```python
parser.print_tree(result)
```

```shell
ROOT
└── [root] هستیم
    ├── [nsubj] ما
    ├── [obl] آنچه
    │   ├── [case] با
    │   └── [acl] می‌سازیم
    ├── [xcomp] ایرانی
    └── [punct] .
```
