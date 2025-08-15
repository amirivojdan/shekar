import pytest
from shekar.morphology.conjugator import Conjugator


class TestConjugator:
    @pytest.fixture
    def conjugator(self):
        return Conjugator()

    def test_init(self, conjugator):
        assert conjugator._past_personal_suffixes == ["م", "ی", "", "یم", "ید", "ند"]
        assert conjugator._present_personal_suffixes == [
            "م",
            "ی",
            "د",
            "یم",
            "ید",
            "ند",
        ]

    def test_simple_past_regular(self, conjugator):
        # Test with example from docstring
        result = conjugator.simple_past("شناخت")
        expected = ["شناختم", "شناختی", "شناخت", "شناختیم", "شناختید", "شناختند"]
        assert result == expected

        # Test with another verb
        result = conjugator.simple_past("خورد")
        expected = ["خوردم", "خوردی", "خورد", "خوردیم", "خوردید", "خوردند"]
        assert result == expected

    def test_simple_past_negative(self, conjugator):
        # Test with example from docstring
        result = conjugator.simple_past("شناخت", negative=True)
        expected = ["نشناختم", "نشناختی", "نشناخت", "نشناختیم", "نشناختید", "نشناختند"]
        assert result == expected

        # Test with another verb
        result = conjugator.simple_past("رفت", negative=True)
        expected = ["نرفتم", "نرفتی", "نرفت", "نرفتیم", "نرفتید", "نرفتند"]
        assert result == expected

    def test_simple_past_passive(self, conjugator):
        # Test with example from docstring
        result = conjugator.simple_past("شناخت", passive=True)
        expected = [
            "شناخته شدم",
            "شناخته شدی",
            "شناخته شد",
            "شناخته شدیم",
            "شناخته شدید",
            "شناخته شدند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.simple_past("دید", passive=True)
        expected = [
            "دیده شدم",
            "دیده شدی",
            "دیده شد",
            "دیده شدیم",
            "دیده شدید",
            "دیده شدند",
        ]
        assert result == expected

    def test_simple_past_negative_passive(self, conjugator):
        # Test with example from docstring
        result = conjugator.simple_past("شناخت", negative=True, passive=True)
        expected = [
            "شناخته نشدم",
            "شناخته نشدی",
            "شناخته نشد",
            "شناخته نشدیم",
            "شناخته نشدید",
            "شناخته نشدند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.simple_past("خواند", negative=True, passive=True)
        expected = [
            "خوانده نشدم",
            "خوانده نشدی",
            "خوانده نشد",
            "خوانده نشدیم",
            "خوانده نشدید",
            "خوانده نشدند",
        ]
        assert result == expected

    def test_simple_past_empty_string(self, conjugator):
        # Test with empty string
        result = conjugator.simple_past("")
        expected = ["م", "ی", "", "یم", "ید", "ند"]
        assert result == expected

    def test_present_perfect_regular(self, conjugator):
        # Test with example from docstring
        result = conjugator.present_perfect("شناخت")
        expected = [
            "شناخته‌ام",
            "شناخته‌ای",
            "شناخته‌است",
            "شناخته‌ایم",
            "شناخته‌اید",
            "شناخته‌اند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.present_perfect("خورد")
        expected = [
            "خورده‌ام",
            "خورده‌ای",
            "خورده‌است",
            "خورده‌ایم",
            "خورده‌اید",
            "خورده‌اند",
        ]
        assert result == expected

    def test_present_perfect_negative(self, conjugator):
        # Test with example from docstring
        result = conjugator.present_perfect("شناخت", negative=True)
        expected = [
            "نشناخته‌ام",
            "نشناخته‌ای",
            "نشناخته‌است",
            "نشناخته‌ایم",
            "نشناخته‌اید",
            "نشناخته‌اند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.present_perfect("رفت", negative=True)
        expected = [
            "نرفته‌ام",
            "نرفته‌ای",
            "نرفته‌است",
            "نرفته‌ایم",
            "نرفته‌اید",
            "نرفته‌اند",
        ]
        assert result == expected

    def test_present_perfect_passive(self, conjugator):
        # Test with example from docstring
        result = conjugator.present_perfect("شناخت", passive=True)
        expected = [
            "شناخته شده‌ام",
            "شناخته شده‌ای",
            "شناخته شده‌است",
            "شناخته شده‌ایم",
            "شناخته شده‌اید",
            "شناخته شده‌اند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.present_perfect("دید", passive=True)
        expected = [
            "دیده شده‌ام",
            "دیده شده‌ای",
            "دیده شده‌است",
            "دیده شده‌ایم",
            "دیده شده‌اید",
            "دیده شده‌اند",
        ]
        assert result == expected

    def test_present_perfect_negative_passive(self, conjugator):
        # Test with example from docstring
        result = conjugator.present_perfect("شناخت", negative=True, passive=True)
        expected = [
            "شناخته نشده‌ام",
            "شناخته نشده‌ای",
            "شناخته نشده‌است",
            "شناخته نشده‌ایم",
            "شناخته نشده‌اید",
            "شناخته نشده‌اند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.present_perfect("خواند", negative=True, passive=True)
        expected = [
            "خوانده نشده‌ام",
            "خوانده نشده‌ای",
            "خوانده نشده‌است",
            "خوانده نشده‌ایم",
            "خوانده نشده‌اید",
            "خوانده نشده‌اند",
        ]
        assert result == expected

    def test_present_perfect_empty_string(self, conjugator):
        # Test with empty string
        result = conjugator.present_perfect("")
        expected = ["ه‌ام", "ه‌ای", "ه‌است", "ه‌ایم", "ه‌اید", "ه‌اند"]
        assert result == expected

    def test_past_continuous_regular(self, conjugator):
        # Test with example from docstring
        result = conjugator.past_continuous("شناخت")
        expected = [
            "می‌شناختم",
            "می‌شناختی",
            "می‌شناخت",
            "می‌شناختیم",
            "می‌شناختید",
            "می‌شناختند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.past_continuous("خورد")
        expected = ["می‌خوردم", "می‌خوردی", "می‌خورد", "می‌خوردیم", "می‌خوردید", "می‌خوردند"]
        assert result == expected

    def test_past_continuous_negative(self, conjugator):
        # Test with example from docstring
        result = conjugator.past_continuous("شناخت", negative=True)
        expected = [
            "نمی‌شناختم",
            "نمی‌شناختی",
            "نمی‌شناخت",
            "نمی‌شناختیم",
            "نمی‌شناختید",
            "نمی‌شناختند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.past_continuous("رفت", negative=True)
        expected = ["نمی‌رفتم", "نمی‌رفتی", "نمی‌رفت", "نمی‌رفتیم", "نمی‌رفتید", "نمی‌رفتند"]
        assert result == expected

    def test_past_continuous_passive(self, conjugator):
        # Test with example from docstring
        result = conjugator.past_continuous("شناخت", passive=True)
        expected = [
            "شناخته می‌شدم",
            "شناخته می‌شدی",
            "شناخته می‌شد",
            "شناخته می‌شدیم",
            "شناخته می‌شدید",
            "شناخته می‌شدند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.past_continuous("دید", passive=True)
        expected = [
            "دیده می‌شدم",
            "دیده می‌شدی",
            "دیده می‌شد",
            "دیده می‌شدیم",
            "دیده می‌شدید",
            "دیده می‌شدند",
        ]
        assert result == expected

    def test_past_continuous_negative_passive(self, conjugator):
        # Test with example from docstring
        result = conjugator.past_continuous("شناخت", negative=True, passive=True)
        expected = [
            "شناخته نمی‌شدم",
            "شناخته نمی‌شدی",
            "شناخته نمی‌شد",
            "شناخته نمی‌شدیم",
            "شناخته نمی‌شدید",
            "شناخته نمی‌شدند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.past_continuous("خواند", negative=True, passive=True)
        expected = [
            "خوانده نمی‌شدم",
            "خوانده نمی‌شدی",
            "خوانده نمی‌شد",
            "خوانده نمی‌شدیم",
            "خوانده نمی‌شدید",
            "خوانده نمی‌شدند",
        ]
        assert result == expected

    def test_past_continuous_empty_string(self, conjugator):
        # Test with empty string
        result = conjugator.past_continuous("")
        expected = ["می‌م", "می‌ی", "می‌", "می‌یم", "می‌ید", "می‌ند"]
        assert result == expected

    def test_present_perfect_continuous_regular(self, conjugator):
        # Test with example from docstring
        result = conjugator.present_perfect_continuous("شناخت")
        expected = [
            "می‌شناخته‌ام",
            "می‌شناخته‌ای",
            "می‌شناخته‌است",
            "می‌شناخته‌ایم",
            "می‌شناخته‌اید",
            "می‌شناخته‌اند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.present_perfect_continuous("خورد")
        expected = [
            "می‌خورده‌ام",
            "می‌خورده‌ای",
            "می‌خورده‌است",
            "می‌خورده‌ایم",
            "می‌خورده‌اید",
            "می‌خورده‌اند",
        ]
        assert result == expected

    def test_present_perfect_continuous_negative(self, conjugator):
        # Test with example from docstring
        result = conjugator.present_perfect_continuous("شناخت", negative=True)
        expected = [
            "نمی‌شناخته‌ام",
            "نمی‌شناخته‌ای",
            "نمی‌شناخته‌است",
            "نمی‌شناخته‌ایم",
            "نمی‌شناخته‌اید",
            "نمی‌شناخته‌اند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.present_perfect_continuous("رفت", negative=True)
        expected = [
            "نمی‌رفته‌ام",
            "نمی‌رفته‌ای",
            "نمی‌رفته‌است",
            "نمی‌رفته‌ایم",
            "نمی‌رفته‌اید",
            "نمی‌رفته‌اند",
        ]
        assert result == expected

    def test_present_perfect_continuous_passive(self, conjugator):
        # Test with example from docstring
        result = conjugator.present_perfect_continuous("شناخت", passive=True)
        expected = [
            "شناخته می‌شده‌ام",
            "شناخته می‌شده‌ای",
            "شناخته می‌شده‌است",
            "شناخته می‌شده‌ایم",
            "شناخته می‌شده‌اید",
            "شناخته می‌شده‌اند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.present_perfect_continuous("دید", passive=True)
        expected = [
            "دیده می‌شده‌ام",
            "دیده می‌شده‌ای",
            "دیده می‌شده‌است",
            "دیده می‌شده‌ایم",
            "دیده می‌شده‌اید",
            "دیده می‌شده‌اند",
        ]
        assert result == expected

    def test_present_perfect_continuous_negative_passive(self, conjugator):
        # Test with example from docstring
        result = conjugator.present_perfect_continuous(
            "شناخت", negative=True, passive=True
        )
        expected = [
            "شناخته نمی‌شده‌ام",
            "شناخته نمی‌شده‌ای",
            "شناخته نمی‌شده‌است",
            "شناخته نمی‌شده‌ایم",
            "شناخته نمی‌شده‌اید",
            "شناخته نمی‌شده‌اند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.present_perfect_continuous(
            "خواند", negative=True, passive=True
        )
        expected = [
            "خوانده نمی‌شده‌ام",
            "خوانده نمی‌شده‌ای",
            "خوانده نمی‌شده‌است",
            "خوانده نمی‌شده‌ایم",
            "خوانده نمی‌شده‌اید",
            "خوانده نمی‌شده‌اند",
        ]
        assert result == expected

    def test_present_perfect_continuous_empty_string(self, conjugator):
        # Test with empty string
        result = conjugator.present_perfect_continuous("")
        expected = ["می‌ه‌ام", "می‌ه‌ای", "می‌ه‌است", "می‌ه‌ایم", "می‌ه‌اید", "می‌ه‌اند"]
        assert result == expected

    def test_past_perfect_regular(self, conjugator):
        # Test with example from docstring
        result = conjugator.past_perfect("شناخت")
        expected = [
            "شناخته بودم",
            "شناخته بودی",
            "شناخته بود",
            "شناخته بودیم",
            "شناخته بودید",
            "شناخته بودند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.past_perfect("خورد")
        expected = [
            "خورده بودم",
            "خورده بودی",
            "خورده بود",
            "خورده بودیم",
            "خورده بودید",
            "خورده بودند",
        ]
        assert result == expected

    def test_past_perfect_negative(self, conjugator):
        # Test with example from docstring
        result = conjugator.past_perfect("شناخت", negative=True)
        expected = [
            "نشناخته بودم",
            "نشناخته بودی",
            "نشناخته بود",
            "نشناخته بودیم",
            "نشناخته بودید",
            "نشناخته بودند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.past_perfect("رفت", negative=True)
        expected = [
            "نرفته بودم",
            "نرفته بودی",
            "نرفته بود",
            "نرفته بودیم",
            "نرفته بودید",
            "نرفته بودند",
        ]
        assert result == expected

    def test_past_perfect_passive(self, conjugator):
        # Test with example from docstring
        result = conjugator.past_perfect("شناخت", passive=True)
        expected = [
            "شناخته شده بودم",
            "شناخته شده بودی",
            "شناخته شده بود",
            "شناخته شده بودیم",
            "شناخته شده بودید",
            "شناخته شده بودند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.past_perfect("دید", passive=True)
        expected = [
            "دیده شده بودم",
            "دیده شده بودی",
            "دیده شده بود",
            "دیده شده بودیم",
            "دیده شده بودید",
            "دیده شده بودند",
        ]
        assert result == expected

    def test_past_perfect_negative_passive(self, conjugator):
        # Test with example from docstring
        result = conjugator.past_perfect("شناخت", negative=True, passive=True)
        expected = [
            "شناخته نشده بودم",
            "شناخته نشده بودی",
            "شناخته نشده بود",
            "شناخته نشده بودیم",
            "شناخته نشده بودید",
            "شناخته نشده بودند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.past_perfect("خواند", negative=True, passive=True)
        expected = [
            "خوانده نشده بودم",
            "خوانده نشده بودی",
            "خوانده نشده بود",
            "خوانده نشده بودیم",
            "خوانده نشده بودید",
            "خوانده نشده بودند",
        ]
        assert result == expected

    def test_past_perfect_empty_string(self, conjugator):
        # Test with empty string
        result = conjugator.past_perfect("")
        expected = ["ه بودم", "ه بودی", "ه بود", "ه بودیم", "ه بودید", "ه بودند"]
        assert result == expected

    def test_past_perfect_of_past_perfect_regular(self, conjugator):
        # Test with example from docstring
        result = conjugator.past_perfect_of_past_perfect("شناخت")
        expected = [
            "شناخته بوده‌ام",
            "شناخته بوده‌ای",
            "شناخته بوده‌است",
            "شناخته بوده‌ایم",
            "شناخته بوده‌اید",
            "شناخته بوده‌اند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.past_perfect_of_past_perfect("خورد")
        expected = [
            "خورده بوده‌ام",
            "خورده بوده‌ای",
            "خورده بوده‌است",
            "خورده بوده‌ایم",
            "خورده بوده‌اید",
            "خورده بوده‌اند",
        ]
        assert result == expected

    def test_past_perfect_of_past_perfect_negative(self, conjugator):
        # Test with example from docstring
        result = conjugator.past_perfect_of_past_perfect("شناخت", negative=True)
        expected = [
            "نشناخته بوده‌ام",
            "نشناخته بوده‌ای",
            "نشناخته بوده‌است",
            "نشناخته بوده‌ایم",
            "نشناخته بوده‌اید",
            "نشناخته بوده‌اند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.past_perfect_of_past_perfect("رفت", negative=True)
        expected = [
            "نرفته بوده‌ام",
            "نرفته بوده‌ای",
            "نرفته بوده‌است",
            "نرفته بوده‌ایم",
            "نرفته بوده‌اید",
            "نرفته بوده‌اند",
        ]
        assert result == expected

    def test_past_perfect_of_past_perfect_passive(self, conjugator):
        # Test with example from docstring
        result = conjugator.past_perfect_of_past_perfect("شناخت", passive=True)
        expected = [
            "شناخته شده بوده‌ام",
            "شناخته شده بوده‌ای",
            "شناخته شده بوده‌است",
            "شناخته شده بوده‌ایم",
            "شناخته شده بوده‌اید",
            "شناخته شده بوده‌اند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.past_perfect_of_past_perfect("دید", passive=True)
        expected = [
            "دیده شده بوده‌ام",
            "دیده شده بوده‌ای",
            "دیده شده بوده‌است",
            "دیده شده بوده‌ایم",
            "دیده شده بوده‌اید",
            "دیده شده بوده‌اند",
        ]
        assert result == expected

    def test_past_perfect_of_past_perfect_negative_passive(self, conjugator):
        # Test with example from docstring
        result = conjugator.past_perfect_of_past_perfect(
            "شناخت", negative=True, passive=True
        )
        expected = [
            "شناخته نشده بوده‌ام",
            "شناخته نشده بوده‌ای",
            "شناخته نشده بوده‌است",
            "شناخته نشده بوده‌ایم",
            "شناخته نشده بوده‌اید",
            "شناخته نشده بوده‌اند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.past_perfect_of_past_perfect(
            "خواند", negative=True, passive=True
        )
        expected = [
            "خوانده نشده بوده‌ام",
            "خوانده نشده بوده‌ای",
            "خوانده نشده بوده‌است",
            "خوانده نشده بوده‌ایم",
            "خوانده نشده بوده‌اید",
            "خوانده نشده بوده‌اند",
        ]
        assert result == expected

    def test_past_perfect_of_past_perfect_empty_string(self, conjugator):
        # Test with empty string
        result = conjugator.past_perfect_of_past_perfect("")
        expected = [
            "ه بوده‌ام",
            "ه بوده‌ای",
            "ه بوده‌است",
            "ه بوده‌ایم",
            "ه بوده‌اید",
            "ه بوده‌اند",
        ]
        assert result == expected

    def test_past_subjunctive_regular(self, conjugator):
        # Test with example from docstring
        result = conjugator.past_subjunctive("شناخت")
        expected = [
            "شناخته باشم",
            "شناخته باشی",
            "شناخته باشد",
            "شناخته باشیم",
            "شناخته باشید",
            "شناخته باشند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.past_subjunctive("خورد")
        expected = [
            "خورده باشم",
            "خورده باشی",
            "خورده باشد",
            "خورده باشیم",
            "خورده باشید",
            "خورده باشند",
        ]
        assert result == expected

    def test_past_subjunctive_negative(self, conjugator):
        # Test with example from docstring
        result = conjugator.past_subjunctive("شناخت", negative=True)
        expected = [
            "نشناخته باشم",
            "نشناخته باشی",
            "نشناخته باشد",
            "نشناخته باشیم",
            "نشناخته باشید",
            "نشناخته باشند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.past_subjunctive("رفت", negative=True)
        expected = [
            "نرفته باشم",
            "نرفته باشی",
            "نرفته باشد",
            "نرفته باشیم",
            "نرفته باشید",
            "نرفته باشند",
        ]
        assert result == expected

    def test_past_subjunctive_passive(self, conjugator):
        # Test with example from docstring
        result = conjugator.past_subjunctive("شناخت", passive=True)
        expected = [
            "شناخته شده باشم",
            "شناخته شده باشی",
            "شناخته شده باشد",
            "شناخته شده باشیم",
            "شناخته شده باشید",
            "شناخته شده باشند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.past_subjunctive("دید", passive=True)
        expected = [
            "دیده شده باشم",
            "دیده شده باشی",
            "دیده شده باشد",
            "دیده شده باشیم",
            "دیده شده باشید",
            "دیده شده باشند",
        ]
        assert result == expected

    def test_past_subjunctive_negative_passive(self, conjugator):
        # Test with example from docstring
        result = conjugator.past_subjunctive("شناخت", negative=True, passive=True)
        expected = [
            "شناخته نشده باشم",
            "شناخته نشده باشی",
            "شناخته نشده باشد",
            "شناخته نشده باشیم",
            "شناخته نشده باشید",
            "شناخته نشده باشند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.past_subjunctive("خواند", negative=True, passive=True)
        expected = [
            "خوانده نشده باشم",
            "خوانده نشده باشی",
            "خوانده نشده باشد",
            "خوانده نشده باشیم",
            "خوانده نشده باشید",
            "خوانده نشده باشند",
        ]
        assert result == expected

    def test_past_subjunctive_empty_string(self, conjugator):
        # Test with empty string
        result = conjugator.past_subjunctive("")
        expected = ["ه باشم", "ه باشی", "ه باشد", "ه باشیم", "ه باشید", "ه باشند"]
        assert result == expected

    def test_past_progressive_regular(self, conjugator):
        # Test with example from docstring
        result = conjugator.past_progressive("شناخت")
        expected = [
            "داشتم می‌شناختم",
            "داشتی می‌شناختی",
            "داشت می‌شناخت",
            "داشتیم می‌شناختیم",
            "داشتید می‌شناختید",
            "داشتند می‌شناختند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.past_progressive("خورد")
        expected = [
            "داشتم می‌خوردم",
            "داشتی می‌خوردی",
            "داشت می‌خورد",
            "داشتیم می‌خوردیم",
            "داشتید می‌خوردید",
            "داشتند می‌خوردند",
        ]
        assert result == expected

    def test_past_progressive_passive(self, conjugator):
        # Test with example from docstring
        result = conjugator.past_progressive("شناخت", passive=True)
        expected = [
            "داشتم شناخته می‌شدم",
            "داشتی شناخته می‌شدی",
            "داشت شناخته می‌شد",
            "داشتیم شناخته می‌شدیم",
            "داشتید شناخته می‌شدید",
            "داشتند شناخته می‌شدند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.past_progressive("دید", passive=True)
        expected = [
            "داشتم دیده می‌شدم",
            "داشتی دیده می‌شدی",
            "داشت دیده می‌شد",
            "داشتیم دیده می‌شدیم",
            "داشتید دیده می‌شدید",
            "داشتند دیده می‌شدند",
        ]
        assert result == expected

    def test_past_progressive_empty_string(self, conjugator):
        # Test with empty string
        result = conjugator.past_progressive("")
        expected = [
            "داشتم می‌م",
            "داشتی می‌ی",
            "داشت می‌",
            "داشتیم می‌یم",
            "داشتید می‌ید",
            "داشتند می‌ند",
        ]
        assert result == expected

    def test_past_progressive_with_third_person(self, conjugator):
        # Test specifically focusing on third person singular
        result = conjugator.past_progressive("رفت")
        assert result[2] == "داشت می‌رفت"

        # Test specifically focusing on third person plural
        assert result[5] == "داشتند می‌رفتند"

    def test_past_perfect_progressive_regular(self, conjugator):
        # Test with example from docstring
        result = conjugator.past_perfect_progressive("شناخت")
        expected = [
            "داشته‌ام می‌شناخته‌ام",
            "داشته‌ای می‌شناخته‌ای",
            "داشته‌است می‌شناخته‌است",
            "داشته‌ایم می‌شناخته‌ایم",
            "داشته‌اید می‌شناخته‌اید",
            "داشته‌اند می‌شناخته‌اند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.past_perfect_progressive("خورد")
        expected = [
            "داشته‌ام می‌خورده‌ام",
            "داشته‌ای می‌خورده‌ای",
            "داشته‌است می‌خورده‌است",
            "داشته‌ایم می‌خورده‌ایم",
            "داشته‌اید می‌خورده‌اید",
            "داشته‌اند می‌خورده‌اند",
        ]
        assert result == expected

    def test_past_perfect_progressive_passive(self, conjugator):
        # Test with example from docstring
        result = conjugator.past_perfect_progressive("شناخت", passive=True)
        expected = [
            "داشته‌ام شناخته می‌شده‌ام",
            "داشته‌ای شناخته می‌شده‌ای",
            "داشته‌است شناخته می‌شده‌است",
            "داشته‌ایم شناخته می‌شده‌ایم",
            "داشته‌اید شناخته می‌شده‌اید",
            "داشته‌اند شناخته می‌شده‌اند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.past_perfect_progressive("دید", passive=True)
        expected = [
            "داشته‌ام دیده می‌شده‌ام",
            "داشته‌ای دیده می‌شده‌ای",
            "داشته‌است دیده می‌شده‌است",
            "داشته‌ایم دیده می‌شده‌ایم",
            "داشته‌اید دیده می‌شده‌اید",
            "داشته‌اند دیده می‌شده‌اند",
        ]
        assert result == expected

    def test_past_perfect_progressive_empty_string(self, conjugator):
        # Test with empty string
        result = conjugator.past_perfect_progressive("")
        expected = [
            "داشته‌ام می‌ه‌ام",
            "داشته‌ای می‌ه‌ای",
            "داشته‌است می‌ه‌است",
            "داشته‌ایم می‌ه‌ایم",
            "داشته‌اید می‌ه‌اید",
            "داشته‌اند می‌ه‌اند",
        ]
        assert result == expected

    def test_past_perfect_progressive_third_person(self, conjugator):
        # Test specifically focusing on third person singular
        result = conjugator.past_perfect_progressive("رفت")
        assert result[2] == "داشته‌است می‌رفته‌است"

        # Test specifically focusing on third person plural
        assert result[5] == "داشته‌اند می‌رفته‌اند"

    def test_simple_present_regular(self, conjugator):
        # Test with example from docstring
        result = conjugator.simple_present("شناخت", "شناس")
        expected = ["شناسم", "شناسی", "شناسد", "شناسیم", "شناسید", "شناسند"]
        assert result == expected

        # Test with another verb
        result = conjugator.simple_present("خورد", "خور")
        expected = ["خورم", "خوری", "خورد", "خوریم", "خورید", "خورند"]
        assert result == expected

    def test_simple_present_negative(self, conjugator):
        # Test with example from docstring
        result = conjugator.simple_present("شناخت", "شناس", negative=True)
        expected = ["نشناسم", "نشناسی", "نشناسد", "نشناسیم", "نشناسید", "نشناسند"]
        assert result == expected

        # Test with another verb
        result = conjugator.simple_present("رفت", "رو", negative=True)
        expected = ["نروم", "نروی", "نرود", "نرویم", "نروید", "نروند"]
        assert result == expected

    def test_simple_present_passive(self, conjugator):
        # Test with example from docstring
        result = conjugator.simple_present("شناخت", "شناس", passive=True)
        expected = [
            "شناخته شوم",
            "شناخته شوی",
            "شناخته شود",
            "شناخته شویم",
            "شناخته شوید",
            "شناخته شوند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.simple_present("دید", "بین", passive=True)
        expected = [
            "دیده شوم",
            "دیده شوی",
            "دیده شود",
            "دیده شویم",
            "دیده شوید",
            "دیده شوند",
        ]
        assert result == expected

    def test_simple_present_negative_passive(self, conjugator):
        # Test with example from docstring
        result = conjugator.simple_present("شناخت", "شناس", negative=True, passive=True)
        expected = [
            "شناخته نشوم",
            "شناخته نشوی",
            "شناخته نشود",
            "شناخته نشویم",
            "شناخته نشوید",
            "شناخته نشوند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.simple_present("خواند", "خوان", negative=True, passive=True)
        expected = [
            "خوانده نشوم",
            "خوانده نشوی",
            "خوانده نشود",
            "خوانده نشویم",
            "خوانده نشوید",
            "خوانده نشوند",
        ]
        assert result == expected

    def test_simple_present_empty_string(self, conjugator):
        # Test with empty string
        result = conjugator.simple_present("", "")
        expected = ["م", "ی", "د", "یم", "ید", "ند"]
        assert result == expected

    def test_simple_present_third_person(self, conjugator):
        # Test specifically focusing on third person singular
        result = conjugator.simple_present("رفت", "رو")
        assert result[2] == "رود"

        # Test specifically focusing on third person plural
        assert result[5] == "روند"

    def test_present_indicative_regular(self, conjugator):
        # Test with example from docstring
        result = conjugator.present_indicative("شناخت", "شناس")
        expected = ["می‌شناسم", "می‌شناسی", "می‌شناسد", "می‌شناسیم", "می‌شناسید", "می‌شناسند"]
        assert result == expected

        # Test with another verb
        result = conjugator.present_indicative("خورد", "خور")
        expected = ["می‌خورم", "می‌خوری", "می‌خورد", "می‌خوریم", "می‌خورید", "می‌خورند"]
        assert result == expected

    def test_present_indicative_negative(self, conjugator):
        # Test with example from docstring
        result = conjugator.present_indicative("شناخت", "شناس", negative=True)
        expected = [
            "نمی‌شناسم",
            "نمی‌شناسی",
            "نمی‌شناسد",
            "نمی‌شناسیم",
            "نمی‌شناسید",
            "نمی‌شناسند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.present_indicative("رفت", "رو", negative=True)
        expected = ["نمی‌روم", "نمی‌روی", "نمی‌رود", "نمی‌رویم", "نمی‌روید", "نمی‌روند"]
        assert result == expected

    def test_present_indicative_passive(self, conjugator):
        # Test with example from docstring
        result = conjugator.present_indicative("شناخت", "شناس", passive=True)
        expected = [
            "شناخته می‌شوم",
            "شناخته می‌شوی",
            "شناخته می‌شود",
            "شناخته می‌شویم",
            "شناخته می‌شوید",
            "شناخته می‌شوند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.present_indicative("دید", "بین", passive=True)
        expected = [
            "دیده می‌شوم",
            "دیده می‌شوی",
            "دیده می‌شود",
            "دیده می‌شویم",
            "دیده می‌شوید",
            "دیده می‌شوند",
        ]
        assert result == expected

    def test_present_indicative_negative_passive(self, conjugator):
        # Test with example from docstring
        result = conjugator.present_indicative(
            "شناخت", "شناس", negative=True, passive=True
        )
        expected = [
            "شناخته نمی‌شوم",
            "شناخته نمی‌شوی",
            "شناخته نمی‌شود",
            "شناخته نمی‌شویم",
            "شناخته نمی‌شوید",
            "شناخته نمی‌شوند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.present_indicative(
            "خواند", "خوان", negative=True, passive=True
        )
        expected = [
            "خوانده نمی‌شوم",
            "خوانده نمی‌شوی",
            "خوانده نمی‌شود",
            "خوانده نمی‌شویم",
            "خوانده نمی‌شوید",
            "خوانده نمی‌شوند",
        ]
        assert result == expected

    def test_present_indicative_empty_string(self, conjugator):
        # Test with empty string
        result = conjugator.present_indicative("", "")
        expected = ["می‌م", "می‌ی", "می‌د", "می‌یم", "می‌ید", "می‌ند"]
        assert result == expected

    def test_present_indicative_third_person(self, conjugator):
        # Test specifically focusing on third person singular
        result = conjugator.present_indicative("رفت", "رو")
        assert result[2] == "می‌رود"

        # Test specifically focusing on third person plural
        assert result[5] == "می‌روند"

    def test_present_subjunctive_regular(self, conjugator):
        # Test with example from docstring
        result = conjugator.present_subjunctive("شناخت", "شناس")
        expected = ["بشناسم", "بشناسی", "بشناسد", "بشناسیم", "بشناسید", "بشناسند"]
        assert result == expected

        # Test with another verb
        result = conjugator.present_subjunctive("خورد", "خور")
        expected = ["بخورم", "بخوری", "بخورد", "بخوریم", "بخورید", "بخورند"]
        assert result == expected

    def test_present_subjunctive_negative(self, conjugator):
        # Test with example from docstring
        result = conjugator.present_subjunctive("شناخت", "شناس", negative=True)
        expected = ["نشناسم", "نشناسی", "نشناسد", "نشناسیم", "نشناسید", "نشناسند"]
        assert result == expected

        # Test with another verb
        result = conjugator.present_subjunctive("رفت", "رو", negative=True)
        expected = ["نروم", "نروی", "نرود", "نرویم", "نروید", "نروند"]
        assert result == expected

    def test_present_subjunctive_passive(self, conjugator):
        # Test with example from docstring
        result = conjugator.present_subjunctive("شناخت", "شناس", passive=True)
        expected = [
            "شناخته بشوم",
            "شناخته بشوی",
            "شناخته بشود",
            "شناخته بشویم",
            "شناخته بشوید",
            "شناخته بشوند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.present_subjunctive("دید", "بین", passive=True)
        expected = [
            "دیده بشوم",
            "دیده بشوی",
            "دیده بشود",
            "دیده بشویم",
            "دیده بشوید",
            "دیده بشوند",
        ]
        assert result == expected

    def test_present_subjunctive_negative_passive(self, conjugator):
        # Test with example from docstring
        result = conjugator.present_subjunctive(
            "شناخت", "شناس", negative=True, passive=True
        )
        expected = [
            "شناخته نشوم",
            "شناخته نشوی",
            "شناخته نشود",
            "شناخته نشویم",
            "شناخته نشوید",
            "شناخته نشوند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.present_subjunctive(
            "خواند", "خوان", negative=True, passive=True
        )
        expected = [
            "خوانده نشوم",
            "خوانده نشوی",
            "خوانده نشود",
            "خوانده نشویم",
            "خوانده نشوید",
            "خوانده نشوند",
        ]
        assert result == expected

    def test_present_subjunctive_empty_string(self, conjugator):
        # Test with empty string
        result = conjugator.present_subjunctive("", "", passive=False)
        expected = ["بم", "بی", "بد", "بیم", "بید", "بند"]
        assert result == expected

    def test_present_subjunctive_third_person(self, conjugator):
        # Test specifically focusing on third person singular
        result = conjugator.present_subjunctive("رفت", "رو")
        assert result[2] == "برود"

        # Test specifically focusing on third person plural
        assert result[5] == "بروند"

    def test_present_progressive_regular(self, conjugator):
        # Test with example from docstring
        result = conjugator.present_progressive("شناخت", "شناس")
        expected = [
            "دارم می‌شناسم",
            "داری می‌شناسی",
            "دارد می‌شناسد",
            "داریم می‌شناسیم",
            "دارید می‌شناسید",
            "دارند می‌شناسند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.present_progressive("خورد", "خور")
        expected = [
            "دارم می‌خورم",
            "داری می‌خوری",
            "دارد می‌خورد",
            "داریم می‌خوریم",
            "دارید می‌خورید",
            "دارند می‌خورند",
        ]
        assert result == expected

    def test_present_progressive_passive(self, conjugator):
        # Test with example from docstring
        result = conjugator.present_progressive("شناخت", "شناس", passive=True)
        expected = [
            "دارم شناخته می‌شوم",
            "داری شناخته می‌شوی",
            "دارد شناخته می‌شود",
            "داریم شناخته می‌شویم",
            "دارید شناخته می‌شوید",
            "دارند شناخته می‌شوند",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.present_progressive("دید", "بین", passive=True)
        expected = [
            "دارم دیده می‌شوم",
            "داری دیده می‌شوی",
            "دارد دیده می‌شود",
            "داریم دیده می‌شویم",
            "دارید دیده می‌شوید",
            "دارند دیده می‌شوند",
        ]
        assert result == expected

    def test_present_progressive_empty_string(self, conjugator):
        # Test with empty string
        result = conjugator.present_progressive("", "")
        expected = [
            "دارم می‌م",
            "داری می‌ی",
            "دارد می‌د",
            "داریم می‌یم",
            "دارید می‌ید",
            "دارند می‌ند",
        ]
        assert result == expected

    def test_present_progressive_third_person(self, conjugator):
        # Test specifically focusing on third person singular
        result = conjugator.present_progressive("رفت", "رو")
        assert result[2] == "دارد می‌رود"

        # Test specifically focusing on third person plural
        assert result[5] == "دارند می‌روند"

    def test_future_simple_regular(self, conjugator):
        # Test with example from docstring
        result = conjugator.future_simple("شناخت")
        expected = [
            "خواهم شناخت",
            "خواهی شناخت",
            "خواهد شناخت",
            "خواهیم شناخت",
            "خواهید شناخت",
            "خواهند شناخت",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.future_simple("خورد")
        expected = [
            "خواهم خورد",
            "خواهی خورد",
            "خواهد خورد",
            "خواهیم خورد",
            "خواهید خورد",
            "خواهند خورد",
        ]
        assert result == expected

    def test_future_simple_negative(self, conjugator):
        # Test with example from docstring
        result = conjugator.future_simple("شناخت", negative=True)
        expected = [
            "نخواهم شناخت",
            "نخواهی شناخت",
            "نخواهد شناخت",
            "نخواهیم شناخت",
            "نخواهید شناخت",
            "نخواهند شناخت",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.future_simple("رفت", negative=True)
        expected = [
            "نخواهم رفت",
            "نخواهی رفت",
            "نخواهد رفت",
            "نخواهیم رفت",
            "نخواهید رفت",
            "نخواهند رفت",
        ]
        assert result == expected

    def test_future_simple_passive(self, conjugator):
        # Test with example from docstring
        result = conjugator.future_simple("شناخت", passive=True)
        expected = [
            "شناخته خواهم شد",
            "شناخته خواهی شد",
            "شناخته خواهد شد",
            "شناخته خواهیم شد",
            "شناخته خواهید شد",
            "شناخته خواهند شد",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.future_simple("دید", passive=True)
        expected = [
            "دیده خواهم شد",
            "دیده خواهی شد",
            "دیده خواهد شد",
            "دیده خواهیم شد",
            "دیده خواهید شد",
            "دیده خواهند شد",
        ]
        assert result == expected

    def test_future_simple_negative_passive(self, conjugator):
        # Test with example from docstring
        result = conjugator.future_simple("شناخت", negative=True, passive=True)
        expected = [
            "شناخته نخواهم شد",
            "شناخته نخواهی شد",
            "شناخته نخواهد شد",
            "شناخته نخواهیم شد",
            "شناخته نخواهید شد",
            "شناخته نخواهند شد",
        ]
        assert result == expected

        # Test with another verb
        result = conjugator.future_simple("خواند", negative=True, passive=True)
        expected = [
            "خوانده نخواهم شد",
            "خوانده نخواهی شد",
            "خوانده نخواهد شد",
            "خوانده نخواهیم شد",
            "خوانده نخواهید شد",
            "خوانده نخواهند شد",
        ]
        assert result == expected

    def test_future_simple_empty_string(self, conjugator):
        # Test with empty string
        result = conjugator.future_simple("")
        expected = ["خواهم ", "خواهی ", "خواهد ", "خواهیم ", "خواهید ", "خواهند "]
        assert result == expected

    def test_future_simple_third_person(self, conjugator):
        # Test specifically focusing on third person singular
        result = conjugator.future_simple("رفت")
        assert result[2] == "خواهد رفت"

        # Test specifically focusing on third person plural
        assert result[5] == "خواهند رفت"

    def test_imperative_regular(self, conjugator):
        # Test with example from docstring
        result = conjugator.imperative("شناس")
        expected = ["بشناس", "بشناسید"]
        assert result == expected

        # Test with another verb
        result = conjugator.imperative("خور")
        expected = ["بخور", "بخورید"]
        assert result == expected

    def test_imperative_negative(self, conjugator):
        # Test with example from docstring
        result = conjugator.imperative("شناس", negative=True)
        expected = ["نشناس", "نشناسید"]
        assert result == expected

        # Test with another verb
        result = conjugator.imperative("رو", negative=True)
        expected = ["نرو", "نروید"]
        assert result == expected

    def test_imperative_empty_string(self, conjugator):
        # Test with empty string
        result = conjugator.imperative("")
        expected = ["ب", "بید"]
        assert result == expected

        result = conjugator.imperative("", negative=True)
        expected = ["ن", "نید"]
        assert result == expected

    def test_imperative_special_verbs(self, conjugator):
        # Test with common irregular verbs
        result = conjugator.imperative("گوی")  # گفتن (to say)
        expected = ["بگوی", "بگویید"]
        assert result == expected

        result = conjugator.imperative("بین")  # دیدن (to see)
        expected = ["ببین", "ببینید"]
        assert result == expected

        result = conjugator.imperative("کن")  # کردن (to do)
        expected = ["بکن", "بکنید"]
        assert result == expected

    def test_conjugate(self, conjugator):
        # Test conjugation of a verb with both past and present stem
        result = conjugator.conjugate("شناخت", "شناس")

        # Check that we got the expected number of conjugations
        # 30 forms (past tenses) + 20 forms (present/future tenses) = 50 forms x 6 persons = 300 conjugated forms
        assert len(result) == 306

        # Verify specific expected forms are present
        # Sample from each tense to ensure they're all included
        assert "شناختم" in result  # simple past
        assert "نشناختم" in result  # negative simple past
        assert "شناخته شدم" in result  # passive simple past
        assert "شناخته نشدم" in result  # negative passive simple past

        assert "شناخته‌ام" in result  # present perfect
        assert "نشناخته‌ام" in result  # negative present perfect
        assert "شناخته شده‌ام" in result  # passive present perfect

        assert "می‌شناختم" in result  # past continuous
        assert "شناخته می‌شدم" in result  # passive past continuous

        assert "می‌شناسم" in result  # present indicative
        assert "نمی‌شناسم" in result  # negative present indicative

        assert "بشناسم" in result  # present subjunctive
        assert "نشناسم" in result  # negative present subjunctive

        assert "خواهم شناخت" in result  # future simple
        assert "شناخته خواهم شد" in result  # passive future simple

    def test_conjugate_past_only(self, conjugator):
        # Test conjugation of a verb with only past stem
        result = conjugator.conjugate("شناخت")

        assert len(result) == 194

        # Verify specific expected forms are present
        assert "شناختم" in result  # simple past
        assert "شناخته‌ام" in result  # present perfect
        assert "می‌شناختم" in result  # past continuous
        assert "شناخته بودم" in result  # past perfect

        # Verify that no present/future forms are included
        assert "می‌شناسم" not in result  # present indicative should not be present
        assert "خواهم شناخت" not in result  # future simple should not be present

    def test_conjugate_empty_strings(self, conjugator):
        # Test with empty strings
        result = conjugator.conjugate("", "")

        # Should still produce conjugations with empty stems
        assert len(result) == 0

        result = conjugator.conjugate("", "شناس")
        assert len(result) == 112

        result = conjugator.conjugate("شناخت", "")
        assert len(result) == 194

    def test_conjugate_different_verbs(self, conjugator):
        # Test with different verbs to ensure general functionality

        # Test with verb "رفتن" (to go)
        result_go = conjugator.conjugate("رفت", "رو")
        assert "رفتم" in result_go
        assert "می‌روم" in result_go
        assert "نخواهم رفت" in result_go

        # Test with verb "خوردن" (to eat)
        result_eat = conjugator.conjugate("خورد", "خور")
        assert "خوردم" in result_eat
        assert "می‌خورم" in result_eat
        assert "خواهم خورد" in result_eat

        # Test with verb "دیدن" (to see)
        result_see = conjugator.conjugate("دید", "بین")
        assert "دیدم" in result_see
        assert "می‌بینم" in result_see
        assert "دیده خواهم شد" in result_see

    def test_conjugate_consistency(self, conjugator):
        # Test that the conjugate method outputs match individual method outputs
        past_stem = "شناخت"
        present_stem = "شناس"

        # Get the full conjugation
        full_result = conjugator.conjugate(past_stem, present_stem)

        # Get individual conjugations for comparison
        simple_past = conjugator.simple_past(past_stem)
        present_indicative = conjugator.present_indicative(past_stem, present_stem)
        future_simple = conjugator.future_simple(past_stem)

        # Verify that individual conjugations are included in the full result
        for form in simple_past:
            assert form in full_result

        for form in present_indicative:
            assert form in full_result

        for form in future_simple:
            assert form in full_result
