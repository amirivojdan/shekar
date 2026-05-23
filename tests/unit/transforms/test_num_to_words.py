import pytest

from shekar.transforms import NumberToWords


class TestNumberToWords:
    def setup_method(self):
        self.converter = NumberToWords()

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("0", "صفر"),
            ("1", "یک"),
            ("2", "دو"),
            ("5", "پنج"),
            ("9", "نه"),
            ("10", "ده"),
            ("11", "یازده"),
            ("15", "پانزده"),
            ("19", "نوزده"),
        ],
    )
    def test_units_and_teens(self, value, expected):
        assert self.converter(value) == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("20", "بیست"),
            ("21", "بیست و یک"),
            ("34", "سی و چهار"),
            ("40", "چهل"),
            ("58", "پنجاه و هشت"),
            ("67", "شصت و هفت"),
            ("70", "هفتاد"),
            ("89", "هشتاد و نه"),
            ("99", "نود و نه"),
        ],
    )
    def test_tens(self, value, expected):
        assert self.converter(value) == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("100", "صد"),
            ("101", "صد و یک"),
            ("110", "صد و ده"),
            ("125", "صد و بیست و پنج"),
            ("200", "دویست"),
            ("256", "دویست و پنجاه و شش"),
            ("300", "سیصد"),
            ("444", "چهارصد و چهل و چهار"),
            ("500", "پانصد"),
            ("666", "ششصد و شصت و شش"),
            ("700", "هفتصد"),
            ("888", "هشتصد و هشتاد و هشت"),
            ("999", "نهصد و نود و نه"),
        ],
    )
    def test_hundreds(self, value, expected):
        assert self.converter(value) == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("1000", "یک هزار"),
            ("1001", "یک هزار و یک"),
            ("1010", "یک هزار و ده"),
            ("1100", "یک هزار و صد"),
            ("1250", "یک هزار و دویست و پنجاه"),
            (
                "9999",
                "نه هزار و نهصد و نود و نه",
            ),
        ],
    )
    def test_thousands(self, value, expected):
        assert self.converter(value) == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("1000000", "یک میلیون"),
            (
                "2000001",
                "دو میلیون و یک",
            ),
            (
                "1234567",
                "یک میلیون و دویست و سی و چهار هزار و پانصد و شصت و هفت",
            ),
            (
                "1000000000",
                "یک میلیارد",
            ),
            (
                "1000000000000",
                "یک تریلیون",
            ),
        ],
    )
    def test_large_numbers(self, value, expected):
        assert self.converter(value) == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("-1", "منفی یک"),
            ("-12", "منفی دوازده"),
            ("-125", "منفی صد و بیست و پنج"),
            (
                "-1250",
                "منفی یک هزار و دویست و پنجاه",
            ),
        ],
    )
    def test_negative_numbers(self, value, expected):
        assert self.converter(value) == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("1.5", "یک ممیز پنج"),
            ("12.75", "دوازده ممیز هفتاد و پنج"),
            (
                "1250.25",
                "یک هزار و دویست و پنجاه ممیز بیست و پنج",
            ),
        ],
    )
    def test_decimal_numbers(self, value, expected):
        assert self.converter(value) == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("۱۲۳", "صد و بیست و سه"),
            ("۴۵۶۷", "چهار هزار و پانصد و شصت و هفت"),
            ("-۱۲", "منفی دوازده"),
            ("۱۲.۵", "دوازده ممیز پنج"),
        ],
    )
    def test_persian_digits(self, value, expected):
        assert self.converter(value) == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("١٢٣", "صد و بیست و سه"),
            ("٤٥٦٧", "چهار هزار و پانصد و شصت و هفت"),
            ("-١٢", "منفی دوازده"),
            ("١٢.٥", "دوازده ممیز پنج"),
        ],
    )
    def test_arabic_digits(self, value, expected):
        assert self.converter(value) == expected

    def test_strips_whitespace(self):
        assert self.converter("   1250   ") == "یک هزار و دویست و پنجاه"

    @pytest.mark.parametrize(
        "value",
        [
            "",
            "abc",
            "12a",
            "1,000",
            "--12",
            "12..5",
            "۱۲۳abc",
            "۳٫۱۴",
            "+12",
        ],
    )
    def test_invalid_inputs_raise_value_error(self, value):
        with pytest.raises(ValueError):
            self.converter(value)

    def test_transform_alias(self):
        assert self.converter.transform("1250") == "یک هزار و دویست و پنجاه"

    def test_callable_interface(self):
        assert callable(self.converter)

    def test_no_double_and(self):
        result = self.converter("1005")

        assert "و و" not in result
        assert result == "یک هزار و پنج"

    def test_zero_inside_large_number(self):
        assert self.converter("1000005") == "یک میلیون و پنج"

    def test_exact_hundreds_do_not_append_extra_text(self):
        assert self.converter("500") == "پانصد"

    def test_exact_thousands_do_not_append_extra_text(self):
        assert self.converter("2000") == "دو هزار"

    def test_exact_millions_do_not_append_extra_text(self):
        assert self.converter("3000000") == "سه میلیون"
