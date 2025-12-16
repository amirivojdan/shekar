import pytest
from shekar.morphology.conjugator import Conjugator


class TestConjugator:
    @pytest.fixture
    def conjugator(self):
        return Conjugator()

    def test_verb_prefix(self, conjugator):
        stem, verb_prefix = conjugator.get_verb_prefix("برگشت")
        assert verb_prefix == "بر"
        assert stem == "گشت"

        stem, verb_prefix = conjugator.get_verb_prefix("برید")
        assert verb_prefix == ""
        assert stem == "برید"

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

        # Test with example from docstring
        result = conjugator.simple_past("شناخت", negative=True)
        expected = ["نشناختم", "نشناختی", "نشناخت", "نشناختیم", "نشناختید", "نشناختند"]
        assert result == expected

        # Test with another verb
        result = conjugator.simple_past("رفت", negative=True)
        expected = ["نرفتم", "نرفتی", "نرفت", "نرفتیم", "نرفتید", "نرفتند"]
        assert result == expected

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

        result = conjugator.simple_past(past_stem="خوند", informal=True)
        expected = ["خوندم", "خوندی", "خوند", "خوندیم", "خوندید", "خوندین", "خوندن"]
        assert result == expected

        result = conjugator.simple_past(past_stem="خوند", negative=True, informal=True)
        expected = [
            "نخوندم",
            "نخوندی",
            "نخوند",
            "نخوندیم",
            "نخوندید",
            "نخوندین",
            "نخوندن",
        ]
        assert result == expected

        result = conjugator.simple_past(past_stem="خوند", passive=True, informal=True)
        expected = [
            "خونده شدم",
            "خونده شدی",
            "خونده شد",
            "خونده شدیم",
            "خونده شدید",
            "خونده شدین",
            "خونده شدن",
        ]
        assert result == expected

        result = conjugator.simple_past(
            past_stem="خوند", passive=True, negative=True, informal=True
        )
        expected = [
            "خونده نشدم",
            "خونده نشدی",
            "خونده نشد",
            "خونده نشدیم",
            "خونده نشدید",
            "خونده نشدین",
            "خونده نشدن",
        ]
        assert result == expected

        result = conjugator.simple_past(
            past_stem="گشت",
            prefix="بر",
            compound_preverb="خوش",
            negative=False,
            passive=False,
            informal=False,
        )

        expected = [
            "خوش برگشتم",
            "خوش برگشتی",
            "خوش برگشت",
            "خوش برگشتیم",
            "خوش برگشتید",
            "خوش برگشتند",
        ]
        assert result == expected

        result = conjugator.simple_past(
            past_stem="گشت",
            prefix="بر",
            compound_preverb="خوش",
            negative=True,
            passive=False,
            informal=False,
        )

        expected = [
            "خوش برنگشتم",
            "خوش برنگشتی",
            "خوش برنگشت",
            "خوش برنگشتیم",
            "خوش برنگشتید",
            "خوش برنگشتند",
        ]
        assert result == expected

        result = conjugator.simple_past(
            past_stem="گشت",
            prefix="بر",
            compound_preverb="خوش",
            negative=True,
            passive=True,
            informal=False,
        )

        expected = [
            "خوش برگشته نشدم",
            "خوش برگشته نشدی",
            "خوش برگشته نشد",
            "خوش برگشته نشدیم",
            "خوش برگشته نشدید",
            "خوش برگشته نشدند",
        ]
        assert result == expected

        result = conjugator.simple_past(
            past_stem="گشت",
            prefix="بر",
            compound_preverb="خوش",
            negative=True,
            passive=True,
            informal=True,
        )

        expected = [
            "خوش برگشته نشدم",
            "خوش برگشته نشدی",
            "خوش برگشته نشد",
            "خوش برگشته نشدیم",
            "خوش برگشته نشدید",
            "خوش برگشته نشدین",
            "خوش برگشته نشدن",
        ]
        assert result == expected

    def test_simple_past_empty_string(self, conjugator):
        # Test with empty string
        result = conjugator.simple_past("")
        expected = ["م", "ی", "", "یم", "ید", "ند"]
        assert result == expected

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

        result = conjugator.present_perfect("آمد", negative=True)
        expected = [
            "نیامده\u200cام",
            "نیامده\u200cای",
            "نیامده\u200cاست",
            "نیامده\u200cایم",
            "نیامده\u200cاید",
            "نیامده\u200cاند",
        ]
        assert result == expected

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

        result = conjugator.present_perfect("آمد", passive=True)
        expected = [
            "آمده شده\u200cام",
            "آمده شده\u200cای",
            "آمده شده\u200cاست",
            "آمده شده\u200cایم",
            "آمده شده\u200cاید",
            "آمده شده\u200cاند",
        ]
        assert result == expected

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

        result = conjugator.present_perfect("ایستاد", negative=True, passive=True)
        expected = [
            "ایستاده نشده\u200cام",
            "ایستاده نشده\u200cای",
            "ایستاده نشده\u200cاست",
            "ایستاده نشده\u200cایم",
            "ایستاده نشده\u200cاید",
            "ایستاده نشده\u200cاند",
        ]
        assert result == expected

        result = conjugator.present_perfect(past_stem="خوند", informal=True)
        expected = ["خوندم", "خوندی", "خونده", "خوندیم", "خوندید", "خوندین", "خوندن"]
        assert result == expected
        result = conjugator.present_perfect(
            past_stem="خوند", negative=True, informal=True
        )
        expected = [
            "نخوندم",
            "نخوندی",
            "نخونده",
            "نخوندیم",
            "نخوندید",
            "نخوندین",
            "نخوندن",
        ]
        assert result == expected
        result = conjugator.present_perfect(
            past_stem="خوند", passive=True, informal=True
        )
        expected = [
            "خونده شدم",
            "خونده شدی",
            "خونده شد",
            "خونده شدیم",
            "خونده شدید",
            "خونده شدین",
            "خونده شدن",
        ]
        assert result == expected
        result = conjugator.present_perfect(
            past_stem="خوند", passive=True, negative=True, informal=True
        )
        expected = [
            "خونده نشدم",
            "خونده نشدی",
            "خونده نشد",
            "خونده نشدیم",
            "خونده نشدید",
            "خونده نشدین",
            "خونده نشدن",
        ]
        assert result == expected

        result = conjugator.present_perfect(
            "گشت", prefix="بر", compound_preverb="خوش", negative=True, passive=False
        )
        expected = [
            "خوش برنگشته\u200cام",
            "خوش برنگشته\u200cای",
            "خوش برنگشته\u200cاست",
            "خوش برنگشته\u200cایم",
            "خوش برنگشته\u200cاید",
            "خوش برنگشته\u200cاند",
        ]
        assert result == expected

        result = conjugator.present_perfect(
            "گشت",
            prefix="بر",
            compound_preverb="خوش",
            informal=True,
            negative=True,
            passive=True,
        )
        expected = [
            "خوش  برگشته نشدم",
            "خوش  برگشته نشدی",
            "خوش  برگشته نشد",
            "خوش  برگشته نشدیم",
            "خوش  برگشته نشدید",
            "خوش  برگشته نشدین",
            "خوش  برگشته نشدن",
        ]
        assert result == expected

        result = conjugator.present_perfect(
            "گشت",
            prefix="بر",
            compound_preverb="خوش",
            informal=True,
            negative=True,
            passive=False,
        )
        expected = [
            "خوش برنگشتم",
            "خوش برنگشتی",
            "خوش برنگشته",
            "خوش برنگشتیم",
            "خوش برنگشتید",
            "خوش برنگشتین",
            "خوش برنگشتن",
        ]
        assert result == expected

        result = conjugator.present_perfect(
            "آمد",
            prefix="بر",
            compound_preverb="باز",
            informal=False,
            negative=True,
            passive=False,
        )
        expected = [
            "باز برنیامده\u200cام",
            "باز برنیامده\u200cای",
            "باز برنیامده\u200cاست",
            "باز برنیامده\u200cایم",
            "باز برنیامده\u200cاید",
            "باز برنیامده\u200cاند",
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

        result = conjugator.past_continuous("آمد", passive=True)
        expected = [
            "آمده می\u200cشدم",
            "آمده می\u200cشدی",
            "آمده می\u200cشد",
            "آمده می\u200cشدیم",
            "آمده می\u200cشدید",
            "آمده می\u200cشدند",
        ]
        assert result == expected

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

        result = conjugator.past_continuous(past_stem="خوند", informal=True)
        expected = [
            "می\u200cخوندم",
            "می\u200cخوندی",
            "می\u200cخوند",
            "می\u200cخوندیم",
            "می\u200cخوندید",
            "می\u200cخوندین",
            "می\u200cخوندن",
        ]
        assert result == expected

        result = conjugator.past_continuous(
            past_stem="خوند", negative=True, informal=True
        )
        expected = [
            "نمی\u200cخوندم",
            "نمی\u200cخوندی",
            "نمی\u200cخوند",
            "نمی\u200cخوندیم",
            "نمی\u200cخوندید",
            "نمی\u200cخوندین",
            "نمی\u200cخوندن",
        ]
        assert result == expected

        result = conjugator.past_continuous(
            past_stem="خوند", passive=True, informal=True
        )
        expected = [
            "خونده می\u200cشدم",
            "خونده می\u200cشدی",
            "خونده می\u200cشد",
            "خونده می\u200cشدیم",
            "خونده می\u200cشدید",
            "خونده می\u200cشدین",
            "خونده می\u200cشدن",
        ]
        assert result == expected

        result = conjugator.past_continuous(
            past_stem="خوند", passive=True, negative=True, informal=True
        )
        expected = [
            "خونده نمی\u200cشدم",
            "خونده نمی\u200cشدی",
            "خونده نمی\u200cشد",
            "خونده نمی\u200cشدیم",
            "خونده نمی\u200cشدید",
            "خونده نمی\u200cشدین",
            "خونده نمی\u200cشدن",
        ]
        assert result == expected

        result = conjugator.past_continuous(
            "آمد",
            prefix="بر",
            compound_preverb="باز",
            informal=False,
            negative=True,
            passive=False,
        )
        expected = [
            "باز برنمی\u200cآمدم",
            "باز برنمی\u200cآمدی",
            "باز برنمی\u200cآمد",
            "باز برنمی\u200cآمدیم",
            "باز برنمی\u200cآمدید",
            "باز برنمی\u200cآمدند",
        ]
        assert result == expected

        result = conjugator.past_continuous(
            "آمد",
            prefix="بر",
            compound_preverb="باز",
            informal=False,
            negative=True,
            passive=True,
        )
        expected = [
            "باز برآمده نمی\u200cشدم",
            "باز برآمده نمی\u200cشدی",
            "باز برآمده نمی\u200cشد",
            "باز برآمده نمی\u200cشدیم",
            "باز برآمده نمی\u200cشدید",
            "باز برآمده نمی\u200cشدند",
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

        result = conjugator.present_perfect_continuous(
            "آمد", prefix="بر", compound_preverb="باز", negative=True, passive=True
        )
        expected = [
            "باز برآمده نمی\u200cشده\u200cام",
            "باز برآمده نمی\u200cشده\u200cای",
            "باز برآمده نمی\u200cشده\u200cاست",
            "باز برآمده نمی\u200cشده\u200cایم",
            "باز برآمده نمی\u200cشده\u200cاید",
            "باز برآمده نمی\u200cشده\u200cاند",
        ]
        assert result == expected

    def test_present_perfect_continuous_empty_string(self, conjugator):
        # Test with empty string
        result = conjugator.present_perfect_continuous("")
        expected = ["می‌ه‌ام", "می‌ه‌ای", "می‌ه‌است", "می‌ه‌ایم", "می‌ه‌اید", "می‌ه‌اند"]
        assert result == expected

    def test_past_perfect_regular(self, conjugator):
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

        result = result = conjugator.past_perfect(
            "آمد", prefix="بر", compound_preverb="باز", negative=True, passive=False
        )
        expected = [
            "باز برنیامده بودم",
            "باز برنیامده بودی",
            "باز برنیامده بود",
            "باز برنیامده بودیم",
            "باز برنیامده بودید",
            "باز برنیامده بودند",
        ]
        assert result == expected

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

        result = result = conjugator.past_perfect(
            "آمد", prefix="بر", compound_preverb="باز", negative=True, passive=True
        )
        expected = [
            "باز برآمده نشده بودم",
            "باز برآمده نشده بودی",
            "باز برآمده نشده بود",
            "باز برآمده نشده بودیم",
            "باز برآمده نشده بودید",
            "باز برآمده نشده بودند",
        ]
        assert result == expected

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

        result = conjugator.past_perfect(past_stem="خوند", informal=True)
        expected = [
            "خونده بودم",
            "خونده بودی",
            "خونده بود",
            "خونده بودیم",
            "خونده بودید",
            "خونده بودین",
            "خونده بودن",
        ]
        assert result == expected

        result = conjugator.past_perfect(past_stem="خوند", negative=True, informal=True)
        expected = [
            "نخونده بودم",
            "نخونده بودی",
            "نخونده بود",
            "نخونده بودیم",
            "نخونده بودید",
            "نخونده بودین",
            "نخونده بودن",
        ]
        assert result == expected

        result = conjugator.past_perfect(past_stem="خوند", passive=True, informal=True)
        expected = [
            "خونده شده بودم",
            "خونده شده بودی",
            "خونده شده بود",
            "خونده شده بودیم",
            "خونده شده بودید",
            "خونده شده بودین",
            "خونده شده بودن",
        ]
        assert result == expected

        result = conjugator.past_perfect(
            past_stem="خوند", passive=True, negative=True, informal=True
        )
        expected = [
            "خونده نشده بودم",
            "خونده نشده بودی",
            "خونده نشده بود",
            "خونده نشده بودیم",
            "خونده نشده بودید",
            "خونده نشده بودین",
            "خونده نشده بودن",
        ]
        assert result == expected

    def test_past_perfect_empty_string(self, conjugator):
        # Test with empty string
        result = conjugator.past_perfect("")
        expected = ["ه بودم", "ه بودی", "ه بود", "ه بودیم", "ه بودید", "ه بودند"]
        assert result == expected

    def test_past_perfect_of_past_perfect_regular(self, conjugator):
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

        result = conjugator.past_perfect_of_past_perfect(
            "آمد", prefix="بر", compound_preverb="باز", negative=True, passive=True
        )
        expected = [
            "باز برآمده نشده بوده\u200cام",
            "باز برآمده نشده بوده\u200cای",
            "باز برآمده نشده بوده\u200cاست",
            "باز برآمده نشده بوده\u200cایم",
            "باز برآمده نشده بوده\u200cاید",
            "باز برآمده نشده بوده\u200cاند",
        ]
        assert result == expected

        result = conjugator.past_perfect_of_past_perfect(
            "آمد", prefix="بر", compound_preverb="باز", negative=True, passive=False
        )
        expected = [
            "باز برنیامده بوده\u200cام",
            "باز برنیامده بوده\u200cای",
            "باز برنیامده بوده\u200cاست",
            "باز برنیامده بوده\u200cایم",
            "باز برنیامده بوده\u200cاید",
            "باز برنیامده بوده\u200cاند",
        ]
        assert result == expected

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

        result = conjugator.past_subjunctive(past_stem="خوند", informal=True)
        expected = [
            "خونده باشم",
            "خونده باشی",
            "خونده باشه",
            "خونده باشیم",
            "خونده باشید",
            "خونده باشین",
            "خونده باشن",
        ]
        assert result == expected

        result = conjugator.past_subjunctive(
            past_stem="خوند", negative=True, informal=True
        )
        expected = [
            "نخونده باشم",
            "نخونده باشی",
            "نخونده باشه",
            "نخونده باشیم",
            "نخونده باشید",
            "نخونده باشین",
            "نخونده باشن",
        ]
        assert result == expected

        result = conjugator.past_subjunctive(
            past_stem="خوند", passive=True, informal=True
        )
        expected = [
            "خونده شده باشم",
            "خونده شده باشی",
            "خونده شده باشه",
            "خونده شده باشیم",
            "خونده شده باشید",
            "خونده شده باشین",
            "خونده شده باشن",
        ]
        assert result == expected

        result = conjugator.past_subjunctive(
            past_stem="خوند", passive=True, negative=True, informal=True
        )
        expected = [
            "خونده نشده باشم",
            "خونده نشده باشی",
            "خونده نشده باشه",
            "خونده نشده باشیم",
            "خونده نشده باشید",
            "خونده نشده باشین",
            "خونده نشده باشن",
        ]
        assert result == expected

        result = conjugator.past_subjunctive(
            "آمد", prefix="بر", compound_preverb="باز", negative=True, passive=False
        )
        expected = [
            "باز برنیامده باشم",
            "باز برنیامده باشی",
            "باز برنیامده باشد",
            "باز برنیامده باشیم",
            "باز برنیامده باشید",
            "باز برنیامده باشند",
        ]
        assert result == expected

        result = conjugator.past_subjunctive(
            "آمد", prefix="بر", compound_preverb="باز", negative=True, passive=True
        )
        expected = [
            "باز برآمده نشده باشم",
            "باز برآمده نشده باشی",
            "باز برآمده نشده باشد",
            "باز برآمده نشده باشیم",
            "باز برآمده نشده باشید",
            "باز برآمده نشده باشند",
        ]
        assert result == expected

    def test_past_subjunctive_empty_string(self, conjugator):
        result = conjugator.past_subjunctive("")
        expected = ["ه باشم", "ه باشی", "ه باشد", "ه باشیم", "ه باشید", "ه باشند"]
        assert result == expected

    def test_past_progressive_regular(self, conjugator):
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

        result = conjugator.past_progressive(
            "آمد", prefix="بر", compound_preverb="باز", passive=True
        )
        expected = [
            "داشتم باز برآمده می\u200cشدم",
            "داشتی باز برآمده می\u200cشدی",
            "داشت باز برآمده می\u200cشد",
            "داشتیم باز برآمده می\u200cشدیم",
            "داشتید باز برآمده می\u200cشدید",
            "داشتند باز برآمده می\u200cشدند",
        ]
        assert result == expected

    def test_past_progressive_empty_string(self, conjugator):
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

    def test_past_progressive_informal(self, conjugator):
        result = conjugator.past_progressive(past_stem="خوند", informal=True)
        expected = [
            "داشتم می\u200cخوندم",
            "داشتی می\u200cخوندی",
            "داشت می\u200cخوند",
            "داشتیم می\u200cخوندیم",
            "داشتید می\u200cخوندید",
            "داشتین می\u200cخوندین",
            "داشتن می\u200cخوندن",
        ]
        assert result == expected

        result = conjugator.past_progressive(
            past_stem="خوند", passive=True, informal=True
        )
        expected = [
            "داشتم خونده می\u200cشدم",
            "داشتی خونده می\u200cشدی",
            "داشت خونده می\u200cشد",
            "داشتیم خونده می\u200cشدیم",
            "داشتید خونده می\u200cشدید",
            "داشتین خونده می\u200cشدین",
            "داشتن خونده می\u200cشدن",
        ]
        assert result == expected

    def test_past_progressive_with_third_person(self, conjugator):
        # Test specifically focusing on third person singular
        result = conjugator.past_progressive("رفت")
        assert result[2] == "داشت می‌رفت"

        # Test specifically focusing on third person plural
        assert result[5] == "داشتند می‌رفتند"

    def test_past_perfect_progressive_regular(self, conjugator):
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

        result = conjugator.past_perfect_progressive("رفت")
        assert result[2] == "داشته‌است می‌رفته‌است"

        assert result[5] == "داشته‌اند می‌رفته‌اند"

        result = conjugator.past_perfect_progressive(
            "آمد", prefix="بر", compound_preverb="باز", passive=True
        )
        expected = [
            "داشته\u200cام باز برآمده می\u200cشده\u200cام",
            "داشته\u200cای باز برآمده می\u200cشده\u200cای",
            "داشته\u200cاست باز برآمده می\u200cشده\u200cاست",
            "داشته\u200cایم باز برآمده می\u200cشده\u200cایم",
            "داشته\u200cاید باز برآمده می\u200cشده\u200cاید",
            "داشته\u200cاند باز برآمده می\u200cشده\u200cاند",
        ]
        assert result == expected

    def test_simple_present_regular(self, conjugator):
        result = conjugator.simple_present("شناخت", "شناس")
        expected = ["شناسم", "شناسی", "شناسد", "شناسیم", "شناسید", "شناسند"]
        assert result == expected

        result = conjugator.simple_present("خورد", "خور")
        expected = ["خورم", "خوری", "خورد", "خوریم", "خورید", "خورند"]
        assert result == expected

        result = conjugator.simple_present("شناخت", "شناس", negative=True)
        expected = ["نشناسم", "نشناسی", "نشناسد", "نشناسیم", "نشناسید", "نشناسند"]
        assert result == expected

        result = conjugator.simple_present("رفت", "رو", negative=True)
        expected = ["نروم", "نروی", "نرود", "نرویم", "نروید", "نروند"]
        assert result == expected

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

        result = conjugator.simple_present(
            present_stem="خون", past_stem="خوند", informal=True
        )
        expected = ["خونم", "خونی", "خونه", "خونیم", "خونید", "خونین", "خونن"]
        assert result == expected

        result = conjugator.simple_present(
            present_stem="خون", past_stem="خوند", negative=True, informal=True
        )
        expected = ["نخونم", "نخونی", "نخونه", "نخونیم", "نخونید", "نخونین", "نخونن"]
        assert result == expected

        result = conjugator.simple_present(
            present_stem="خون", past_stem="خوند", passive=True, informal=True
        )
        expected = [
            "خونده شم",
            "خونده شی",
            "خونده شه",
            "خونده شیم",
            "خونده شید",
            "خونده شین",
            "خونده شن",
        ]
        assert result == expected
        result = conjugator.simple_present(
            present_stem="خون",
            past_stem="خوند",
            passive=True,
            negative=True,
            informal=True,
        )
        expected = [
            "خونده نشم",
            "خونده نشی",
            "خونده نشه",
            "خونده نشیم",
            "خونده نشید",
            "خونده نشین",
            "خونده نشن",
        ]
        assert result == expected

        result = conjugator.simple_present(
            past_stem="آمد",
            present_stem="آ",
            prefix="بر",
            compound_preverb="باز",
            passive=False,
        )
        expected = [
            "باز برآیم",
            "باز برآیی",
            "باز برآید",
            "باز برآییم",
            "باز برآیید",
            "باز برآیند",
        ]
        assert result == expected

        result = conjugator.simple_present(
            past_stem="آمد",
            present_stem="آ",
            prefix="بر",
            compound_preverb="باز",
            negative=True,
            passive=False,
        )
        expected = [
            "باز برنیایم",
            "باز برنیایی",
            "باز برنیاید",
            "باز برنیاییم",
            "باز برنیایید",
            "باز برنیایند",
        ]
        assert result == expected

        result = conjugator.simple_present("رفت", "رو")
        assert result[2] == "رود"
        assert result[5] == "روند"

    def test_simple_present_empty_string(self, conjugator):
        result = conjugator.simple_present("", "")
        expected = ["م", "ی", "د", "یم", "ید", "ند"]
        assert result == expected

    def test_present_indicative_regular(self, conjugator):
        result = conjugator.present_indicative("شناخت", "شناس")
        expected = ["می‌شناسم", "می‌شناسی", "می‌شناسد", "می‌شناسیم", "می‌شناسید", "می‌شناسند"]
        assert result == expected

        result = conjugator.present_indicative("خورد", "خور")
        expected = ["می‌خورم", "می‌خوری", "می‌خورد", "می‌خوریم", "می‌خورید", "می‌خورند"]
        assert result == expected

    def test_present_indicative_negative(self, conjugator):
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

        result = conjugator.present_indicative("رفت", "رو", negative=True)
        expected = ["نمی‌روم", "نمی‌روی", "نمی‌رود", "نمی‌رویم", "نمی‌روید", "نمی‌روند"]
        assert result == expected

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

        result = conjugator.present_indicative(
            past_stem="خوند", present_stem="خون", informal=True
        )
        expected = [
            "می\u200cخونم",
            "می\u200cخونی",
            "می\u200cخونه",
            "می\u200cخونیم",
            "می\u200cخونید",
            "می\u200cخونین",
            "می\u200cخونن",
            "می\u200cخونید",
        ]
        assert result == expected

        result = conjugator.present_indicative(
            past_stem="خوند", present_stem="خون", negative=True, informal=True
        )
        expected = [
            "نمی\u200cخونم",
            "نمی\u200cخونی",
            "نمی\u200cخونه",
            "نمی\u200cخونیم",
            "نمی\u200cخونید",
            "نمی\u200cخونین",
            "نمی\u200cخونن",
            "نمی\u200cخونید",
        ]
        assert result == expected

        result = conjugator.present_indicative(
            past_stem="خوند", present_stem="خون", passive=True, informal=True
        )
        expected = [
            "خونده می\u200cشم",
            "خونده می\u200cشی",
            "خونده می\u200cشه",
            "خونده می\u200cشیم",
            "خونده می\u200cشید",
            "خونده می\u200cشین",
            "خونده می\u200cشن",
            "خونده می\u200cشید",
        ]
        assert result == expected

        result = conjugator.present_indicative(
            past_stem="خوند",
            present_stem="خون",
            passive=True,
            negative=True,
            informal=True,
        )
        expected = [
            "خونده نمی\u200cشم",
            "خونده نمی\u200cشی",
            "خونده نمی\u200cشه",
            "خونده نمی\u200cشیم",
            "خونده نمی\u200cشید",
            "خونده نمی\u200cشین",
            "خونده نمی\u200cشن",
            "خونده نمی\u200cشید",
        ]
        assert result == expected

        result = conjugator.present_indicative(
            past_stem="آمد",
            present_stem="آ",
            prefix="بر",
            compound_preverb="باز",
            negative=True,
            passive=False,
        )
        expected = [
            "باز برنمی\u200cآیم",
            "باز برنمی\u200cآیی",
            "باز برنمی\u200cآید",
            "باز برنمی\u200cآییم",
            "باز برنمی\u200cآیید",
            "باز برنمی\u200cآیند",
        ]
        assert result == expected

        result = conjugator.present_indicative(
            past_stem="آمد",
            present_stem="آ",
            prefix="بر",
            compound_preverb="باز",
            negative=True,
            passive=True,
        )
        expected = [
            "باز برآمده نمی\u200cشوم",
            "باز برآمده نمی\u200cشوی",
            "باز برآمده نمی\u200cشود",
            "باز برآمده نمی\u200cشویم",
            "باز برآمده نمی\u200cشوید",
            "باز برآمده نمی\u200cشوند",
        ]
        assert result == expected

        result = conjugator.present_indicative("رفت", "رو")
        assert result[2] == "می‌رود"
        assert result[5] == "می‌روند"

    def test_present_indicative_empty_string(self, conjugator):
        result = conjugator.present_indicative("", "")
        expected = ["می‌م", "می‌ی", "می‌د", "می‌یم", "می‌ید", "می‌ند"]
        assert result == expected

    def test_present_subjunctive_regular(self, conjugator):
        result = conjugator.present_subjunctive("شناخت", "شناس")
        expected = ["بشناسم", "بشناسی", "بشناسد", "بشناسیم", "بشناسید", "بشناسند"]
        assert result == expected

        result = conjugator.present_subjunctive("خورد", "خور")
        expected = ["بخورم", "بخوری", "بخورد", "بخوریم", "بخورید", "بخورند"]
        assert result == expected

        result = conjugator.present_subjunctive("شناخت", "شناس", negative=True)
        expected = ["نشناسم", "نشناسی", "نشناسد", "نشناسیم", "نشناسید", "نشناسند"]
        assert result == expected

        result = conjugator.present_subjunctive("رفت", "رو", negative=True)
        expected = ["نروم", "نروی", "نرود", "نرویم", "نروید", "نروند"]
        assert result == expected

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

        result = conjugator.present_subjunctive(
            past_stem="خوند", present_stem="خون", informal=True
        )
        expected = [
            "بخونم",
            "بخونی",
            "بخونه",
            "بخونیم",
            "بخونید",
            "بخونین",
            "بخونن",
            "بخونید",
        ]
        assert result == expected

        result = conjugator.present_subjunctive(
            past_stem="خوند", present_stem="خون", negative=True, informal=True
        )
        expected = [
            "نخونم",
            "نخونی",
            "نخونه",
            "نخونیم",
            "نخونید",
            "نخونین",
            "نخونن",
            "نخونید",
        ]
        assert result == expected

        result = conjugator.present_subjunctive(
            past_stem="خوند", present_stem="خون", passive=True, informal=True
        )

        expected = [
            "خونده بشم",
            "خونده بشی",
            "خونده بشه",
            "خونده بشیم",
            "خونده بشید",
            "خونده بشین",
            "خونده بشن",
            "خونده بشید",
        ]
        assert result == expected

        result = conjugator.present_subjunctive(
            past_stem="خوند",
            present_stem="خون",
            passive=True,
            negative=True,
            informal=True,
        )
        expected = [
            "خونده نشم",
            "خونده نشی",
            "خونده نشه",
            "خونده نشیم",
            "خونده نشید",
            "خونده نشین",
            "خونده نشن",
            "خونده نشید",
        ]
        assert result == expected

        result = conjugator.present_subjunctive("رفت", "رو")
        assert result[2] == "برود"
        assert result[5] == "بروند"

        result = conjugator.present_subjunctive(
            past_stem="آمد",
            present_stem="آ",
            prefix="بر",
            compound_preverb="باز",
            negative=False,
            passive=False,
        )
        expected = [
            "باز برآیم",
            "باز برآیی",
            "باز برآید",
            "باز برآییم",
            "باز برآیید",
            "باز برآیند",
            "باز بربیایم",
            "باز بربیایی",
            "باز بربیاید",
            "باز بربیاییم",
            "باز بربیایید",
            "باز بربیایند",
        ]
        assert result == expected

        result = conjugator.present_subjunctive(
            past_stem="آمد",
            present_stem="آ",
            prefix="بر",
            compound_preverb="باز",
            negative=True,
            passive=False,
        )
        expected = [
            "باز برنیایم",
            "باز برنیایی",
            "باز برنیاید",
            "باز برنیاییم",
            "باز برنیایید",
            "باز برنیایند",
        ]
        assert result == expected

        result = conjugator.present_subjunctive(
            past_stem="آمد",
            present_stem="آ",
            prefix="بر",
            compound_preverb="باز",
            negative=True,
            passive=True,
        )
        expected = [
            "باز برآمده نشوم",
            "باز برآمده نشوی",
            "باز برآمده نشود",
            "باز برآمده نشویم",
            "باز برآمده نشوید",
            "باز برآمده نشوند",
        ]
        assert result == expected

    def test_present_subjunctive_empty_string(self, conjugator):
        result = conjugator.present_subjunctive("", "", passive=False)
        expected = ["بم", "بی", "بد", "بیم", "بید", "بند"]
        assert result == expected

    def test_present_progressive_regular(self, conjugator):
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

        result = conjugator.present_progressive("رفت", "رو")
        assert result[2] == "دارد می‌رود"

        # Test specifically focusing on third person plural
        assert result[5] == "دارند می‌روند"

        result = conjugator.present_progressive("خوند", "خون", informal=True)
        expected = [
            "دارم می\u200cخونم",
            "داری می\u200cخونی",
            "داره می\u200cخونه",
            "داریم می\u200cخونیم",
            "دارید می\u200cخونید",
            "دارین می\u200cخونین",
            "دارن می\u200cخونن",
            "دارید می\u200cخونید",
        ]
        assert result == expected

        result = conjugator.present_progressive(
            past_stem="خوند", present_stem="خون", passive=True, informal=True
        )
        expected = [
            "دارم خونده می\u200cشم",
            "داری خونده می\u200cشی",
            "داره خونده می\u200cشه",
            "داریم خونده می\u200cشیم",
            "دارید خونده می\u200cشید",
            "دارین خونده می\u200cشین",
            "دارن خونده می\u200cشن",
            "دارید خونده می\u200cشید",
        ]
        assert result == expected

        result = conjugator.present_progressive(
            past_stem="آمد",
            present_stem="آ",
            prefix="بر",
            compound_preverb="باز",
            passive=True,
        )
        expected = [
            "دارم باز برآمده می\u200cشوم",
            "داری باز برآمده می\u200cشوی",
            "دارد باز برآمده می\u200cشود",
            "داریم باز برآمده می\u200cشویم",
            "دارید باز برآمده می\u200cشوید",
            "دارند باز برآمده می\u200cشوند",
        ]
        assert result == expected

        result = conjugator.present_progressive(
            past_stem="آمد",
            present_stem="آ",
            prefix="بر",
            compound_preverb="باز",
            passive=False,
            informal=True,
        )
        expected = [
            "دارم باز برمی\u200cآم",
            "داری باز برمی\u200cآی",
            "داره باز برمی\u200cآد",
            "داریم باز برمی\u200cآیم",
            "دارید باز برمی\u200cآید",
            "دارین باز برمی\u200cآین",
            "دارن باز برمی\u200cآن",
            "دارید باز برمی\u200cآید",
        ]
        assert result == expected

    def test_present_progressive_empty_string(self, conjugator):
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

    def test_future_simple_regular(self, conjugator):
        result = conjugator.simple_future("شناخت")
        expected = [
            "خواهم شناخت",
            "خواهی شناخت",
            "خواهد شناخت",
            "خواهیم شناخت",
            "خواهید شناخت",
            "خواهند شناخت",
        ]
        assert result == expected

        result = conjugator.simple_future("خورد")
        expected = [
            "خواهم خورد",
            "خواهی خورد",
            "خواهد خورد",
            "خواهیم خورد",
            "خواهید خورد",
            "خواهند خورد",
        ]
        assert result == expected

        result = conjugator.simple_future("شناخت", negative=True)
        expected = [
            "نخواهم شناخت",
            "نخواهی شناخت",
            "نخواهد شناخت",
            "نخواهیم شناخت",
            "نخواهید شناخت",
            "نخواهند شناخت",
        ]
        assert result == expected

        result = conjugator.simple_future("رفت", negative=True)
        expected = [
            "نخواهم رفت",
            "نخواهی رفت",
            "نخواهد رفت",
            "نخواهیم رفت",
            "نخواهید رفت",
            "نخواهند رفت",
        ]
        assert result == expected

        result = conjugator.simple_future("شناخت", passive=True)
        expected = [
            "شناخته خواهم شد",
            "شناخته خواهی شد",
            "شناخته خواهد شد",
            "شناخته خواهیم شد",
            "شناخته خواهید شد",
            "شناخته خواهند شد",
        ]
        assert result == expected

        result = conjugator.simple_future("دید", passive=True)
        expected = [
            "دیده خواهم شد",
            "دیده خواهی شد",
            "دیده خواهد شد",
            "دیده خواهیم شد",
            "دیده خواهید شد",
            "دیده خواهند شد",
        ]
        assert result == expected

        result = conjugator.simple_future("شناخت", negative=True, passive=True)
        expected = [
            "شناخته نخواهم شد",
            "شناخته نخواهی شد",
            "شناخته نخواهد شد",
            "شناخته نخواهیم شد",
            "شناخته نخواهید شد",
            "شناخته نخواهند شد",
        ]
        assert result == expected

        result = conjugator.simple_future("خواند", negative=True, passive=True)
        expected = [
            "خوانده نخواهم شد",
            "خوانده نخواهی شد",
            "خوانده نخواهد شد",
            "خوانده نخواهیم شد",
            "خوانده نخواهید شد",
            "خوانده نخواهند شد",
        ]
        assert result == expected

        result = conjugator.simple_future("رفت")
        assert result[2] == "خواهد رفت"
        assert result[5] == "خواهند رفت"

        result = conjugator.simple_future(
            past_stem="گشت",
            prefix="بر",
            compound_preverb="باز",
            passive=False,
            negative=True,
        )
        expected = [
            "باز بر نخواهم گشت",
            "باز بر نخواهی گشت",
            "باز بر نخواهد گشت",
            "باز بر نخواهیم گشت",
            "باز بر نخواهید گشت",
            "باز بر نخواهند گشت",
        ]
        assert result == expected

        result = conjugator.simple_future(
            past_stem="گشت",
            prefix="بر",
            compound_preverb="باز",
            passive=True,
            negative=True,
        )
        expected = [
            "باز برگشته نخواهم شد",
            "باز برگشته نخواهی شد",
            "باز برگشته نخواهد شد",
            "باز برگشته نخواهیم شد",
            "باز برگشته نخواهید شد",
            "باز برگشته نخواهند شد",
        ]
        assert result == expected

    def test_future_simple_empty_string(self, conjugator):
        result = conjugator.simple_future("")
        expected = ["خواهم ", "خواهی ", "خواهد ", "خواهیم ", "خواهید ", "خواهند "]
        assert result == expected

    def test_imperative_informal(self, conjugator):
        result = conjugator.imperative("خون", informal=True)
        expected = ["بخون", "بخونید", "بخونین"]
        assert result == expected

        result = conjugator.imperative("خون", negative=True, informal=True)
        expected = ["نخون", "نخونید", "نخونین"]
        assert result == expected

    def test_imperative_regular(self, conjugator):
        result = conjugator.imperative("شناس")
        expected = ["بشناس", "بشناسید"]
        assert result == expected

        result = conjugator.imperative("خور")
        expected = ["بخور", "بخورید"]
        assert result == expected

        result = conjugator.imperative("شناس", negative=True)
        expected = ["نشناس", "نشناسید"]
        assert result == expected

        result = conjugator.imperative("رو", negative=True)
        expected = ["نرو", "نروید"]
        assert result == expected

        result = conjugator.imperative(
            present_stem="آ", prefix="بر", compound_preverb="باز", negative=True
        )
        expected = ["باز برنیا", "باز برنیایید"]
        assert result == expected

        result = conjugator.imperative(
            present_stem="آ", prefix="بر", compound_preverb="باز", negative=False
        )
        expected = ["باز برآ", "باز برآیید", "باز بربیا", "باز بربیایید"]
        assert result == expected

    def test_imperative_empty_string(self, conjugator):
        result = conjugator.imperative("")
        expected = ["ب", "بید"]
        assert result == expected

        result = conjugator.imperative("", negative=True)
        expected = ["ن", "نید"]
        assert result == expected

    def test_imperative_special_verbs(self, conjugator):
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
        result = conjugator.conjugate("شناخت", "شناس")

        assert len(result) == 574

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
        result = conjugator.conjugate("شناخت")

        assert len(result) == 348

        assert "شناختم" in result  # simple past
        assert "شناخته‌ام" in result  # present perfect
        assert "می‌شناختم" in result  # past continuous
        assert "شناخته بودم" in result  # past perfect
        assert "می‌شناسم" not in result  # present indicative should not be present
        assert "خواهم شناخت" not in result  # future simple should not be present

    def test_conjugate_empty_strings(self, conjugator):
        result = conjugator.conjugate("", "")
        assert len(result) == 0

        result = conjugator.conjugate("", "شناس")
        assert len(result) == 226

        result = conjugator.conjugate("شناخت", "")
        assert len(result) == 348

    def test_conjugate_different_verbs(self, conjugator):
        result_go = conjugator.conjugate("رفت", "رو")
        assert "رفتم" in result_go
        assert "می‌روم" in result_go
        assert "نخواهم رفت" in result_go

        result_eat = conjugator.conjugate("خورد", "خور")
        assert "خوردم" in result_eat
        assert "می‌خورم" in result_eat
        assert "خواهم خورد" in result_eat

        result_see = conjugator.conjugate("دید", "بین")
        assert "دیدم" in result_see
        assert "می‌بینم" in result_see
        assert "دیده خواهم شد" in result_see

    def test_conjugate_consistency(self, conjugator):
        past_stem = "شناخت"
        present_stem = "شناس"

        full_result = conjugator.conjugate(past_stem, present_stem)

        simple_past = conjugator.simple_past(past_stem)
        present_indicative = conjugator.present_indicative(past_stem, present_stem)
        future_simple = conjugator.simple_future(past_stem)

        for form in simple_past:
            assert form in full_result

        for form in present_indicative:
            assert form in full_result

        for form in future_simple:
            assert form in full_result
