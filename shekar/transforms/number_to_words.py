import re
from shekar.base import BaseTextTransform


class NumberToWords(BaseTextTransform):
    def __init__(self):
        super().__init__()

        self._digit_translation = str.maketrans(
            "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
            "01234567890123456789",
        )

        self._units = {
            0: "صفر",
            1: "یک",
            2: "دو",
            3: "سه",
            4: "چهار",
            5: "پنج",
            6: "شش",
            7: "هفت",
            8: "هشت",
            9: "نه",
            10: "ده",
            11: "یازده",
            12: "دوازده",
            13: "سیزده",
            14: "چهارده",
            15: "پانزده",
            16: "شانزده",
            17: "هفده",
            18: "هجده",
            19: "نوزده",
        }

        self._tens = {
            20: "بیست",
            30: "سی",
            40: "چهل",
            50: "پنجاه",
            60: "شصت",
            70: "هفتاد",
            80: "هشتاد",
            90: "نود",
        }

        self._hundreds = {
            100: "صد",
            200: "دویست",
            300: "سیصد",
            400: "چهارصد",
            500: "پانصد",
            600: "ششصد",
            700: "هفتصد",
            800: "هشتصد",
            900: "نهصد",
        }

        self._scales = [
            "",
            "هزار",
            "میلیون",
            "میلیارد",
            "تریلیون",
        ]

        self._number_re = re.compile(
            r"^-?[0-9\u06F0-\u06F9\u0660-\u0669]+(?:\.[0-9\u06F0-\u06F9\u0660-\u0669]+)?$"
        )

    def _function(self, text: str) -> str:
        text = text.strip()

        if not self._number_re.fullmatch(text):
            raise ValueError(f"Invalid numeric input: {text}")

        text = text.translate(self._digit_translation)

        negative = text.startswith("-")
        if negative:
            text = text[1:]

        if "." in text:
            integer_part, decimal_part = text.split(".", 1)

            integer_words = self._convert_integer(int(integer_part))
            decimal_words = self._convert_integer(int(decimal_part))

            result = f"{integer_words} ممیز {decimal_words}"
        else:
            result = self._convert_integer(int(text))

        if negative:
            result = f"منفی {result}"

        return result

    def _convert_integer(self, number: int) -> str:
        if number == 0:
            return self._units[0]

        parts = []

        scale_index = 0

        while number > 0:
            chunk = number % 1000

            if chunk:
                chunk_words = self._convert_chunk(chunk)

                scale = self._scales[scale_index]

                if scale:
                    parts.append(f"{chunk_words} {scale}")
                else:
                    parts.append(chunk_words)

            number //= 1000
            scale_index += 1

        return " و ".join(reversed(parts))

    def _convert_chunk(self, number: int) -> str:
        parts = []

        hundreds = (number // 100) * 100
        remainder = number % 100

        if hundreds:
            parts.append(self._hundreds[hundreds])

        if remainder:
            if remainder < 20:
                parts.append(self._units[remainder])
            else:
                tens = (remainder // 10) * 10
                units = remainder % 10

                parts.append(self._tens[tens])

                if units:
                    parts.append(self._units[units])

        return " و ".join(parts)
