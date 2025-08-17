from shekar import data


class Inflector:
    """
    Based on the latest edition of Persian orthography rules published by the Academy of
    Persian Language and Literature available at: https://apll.ir/
    """

    def __init__(self):
        self.irregular_adjectives = {
            "خوب": ("بهتر", "بهترین"),
            "که": ("کهتر", "کهترین"),
            "به": ("بهتر", "بهترین"),
            "کم": ("کمتر", "کمترین"),
            "بیش": ("بیشتر", "بیشترین"),
            "مه": ("مهتر", "مهترین"),
        }

        self._possessive_suffixes = ["م", "ت", "ش", "مان", "تان", "شان"]

    def comparative(self, adj: str) -> str:
        """
        Returns the comparative form of an adjective.
        If the adjective is irregular, it returns the predefined form.
        If the adjective is not irregular, it appends "تر" with a ZWNJ if necessary.

        Args:
            adj (str): The adjective to convert to comparative form.

        Returns:
            str: The comparative form of the adjective.

        Example:
            inflector = Inflector()
            inflector.comparative("خوب")
        # Returns: 'بهتر'
            inflector.comparative("ناراحت")
        # Returns: 'ناراحت‌تر'

        """
        if adj in self.irregular_adjectives:
            return self.irregular_adjectives[adj][0]

        zwnj = "" if adj[-1] in data.non_left_joiner_letters else data.ZWNJ
        return adj + zwnj + "تر"

    def superlative(self, adj: str) -> str:
        """
        Returns the superlative form of an adjective.
        If the adjective is irregular, it returns the predefined form.
        If the adjective is not irregular, it appends "ترین" with a ZWNJ if necessary.

        Args:
            adj (str): The adjective to convert to superlative form.

        Returns:
            str: The superlative form of the adjective.

        Example:
            inflector = Inflector()
            inflector.superlative("خوب")
        # Returns: 'بهترین'
            inflector.superlative("ناراحت")
        # Returns: 'ناراحت‌ترین'

        """
        if adj in self.irregular_adjectives:
            return self.irregular_adjectives[adj][1]
        zwnj = "" if adj[-1] in data.non_left_joiner_letters else data.ZWNJ
        return adj + zwnj + "ترین"

    def plural(self, noun: str) -> str:
        """
        Returns the plural form of a noun.
        If the noun is not irregular, it appends "ها" with a ZWNJ if necessary.

        Args:
            noun (str): The noun to convert to plural form.

        Returns:
            str: The plural form of the noun.

        Example:
            inflector = Inflector()
            inflector.plural("کتاب")
        # Returns: 'کتاب‌ها'
            inflector.plural("میز")
        # Returns: 'میزها'

        """
        zwnj = "" if noun[-1] in data.non_left_joiner_letters else data.ZWNJ
        return noun + zwnj + "ها"

    def possessives(self, noun: str):
        """
        Returns a list of possessive forms of a noun.

        Args:
            noun (str): The noun to convert to possessive forms.

        Returns:
            list: A list of possessive forms of the noun.

        Example:
            inflector = Inflector()
            inflector.possessives("کتاب")
        # Returns: ['کتابم', 'کتابت', 'کتابش', 'کتاب‌مان', 'کتاب‌تان', 'کتاب‌شان']

        """
        zwnj = "" if noun[-1] in data.non_left_joiner_letters else data.ZWNJ
        return [noun + zwnj + suffix for suffix in self._possessive_suffixes]
