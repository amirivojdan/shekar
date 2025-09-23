# Spell Checking

The `SpellChecker` class provides simple and effective spelling correction for Persian text. It can automatically detect and fix common errors such as extra characters, spacing mistakes, or misspelled words. You can use it directly as a callable on a sentence to clean up the text, or call `suggest()` to get a ranked list of correction candidates for a single word.

**Example Usage**

```python
from shekar import SpellChecker

spell_checker = SpellChecker()
print(spell_checker("سسلام بر ششما ددوست من"))

print(spell_checker.suggest("درود"))
```

```output
سلام بر شما دوست من
['درود', 'درصد', 'ورود', 'درد', 'درون']
```