from __future__ import annotations
from typing import List
from shekar import data
from functools import lru_cache


class Conjugator:
    """
    A class to generate conjugations of Persian verbs in various tenses.
    This class provides methods to generate conjugated forms of verbs in different tenses,
    including simple past, present perfect, past continuous, and more. It supports both
    negative and passive forms of the verbs.

    Reference:
    This class implements Persian verb conjugation rules as described in:
    https://blog.faradars.org/%D8%B5%D8%B1%D9%81-%D9%81%D8%B9%D9%84-%D9%81%D8%A7%D8%B1%D8%B3%DB%8C/
    """

    def __init__(self):
        self._past_personal_suffixes = data.past_personal_suffixes
        self._informal_past_personal_suffixes = data.informal_past_personal_suffixes
        self._present_personal_suffixes = data.present_personal_suffixes
        self._perfect_personal_suffixes = data.perfect_personal_suffixes
        self.verbal_prefixes = []

        for pref in data.verbal_prefixes:
            if pref[-1] not in data.non_left_joiner_letters:
                self.verbal_prefixes.append(pref + data.ZWNJ)
                continue
            self.verbal_prefixes.append(pref)

        self.compound_verb_exceptions = data.compound_verb_exceptions

    def get_verb_prefix(self, stem: str):
        if any(
            (stem == exception[0] or stem == exception[1])
            for exception in self.compound_verb_exceptions
        ):
            return (stem, "")

        for vprefix in self.verbal_prefixes:
            if stem.startswith(vprefix):
                new_stem = stem.replace(vprefix, "", 1)
                return (new_stem, vprefix)

        return (stem, "")

    def normalize_preverb(self, s: str | None) -> str:
        return f"{s} " if s else ""

    def normalize_prefix(self, prefix: str):
        if (
            prefix
            and (prefix[-1] not in data.non_left_joiner_letters)
            and prefix[-1] != data.ZWNJ
        ):
            prefix = prefix + data.ZWNJ
            return prefix
        return prefix

    def normalize_y(self, stem: str):
        y_after = "ی" if (stem.endswith("آ") or stem.endswith("ا")) else ""
        y_before = "ی" if (stem.startswith("آ") or stem.startswith("ا")) else ""

        # exceptions here
        if stem == "ایستاد" or stem == "ایست":
            y_before = ""

        return y_before, y_after

    def normalize_stem(self, stem: str):
        if stem.startswith("آ"):
            normalized_present_stem = "ا" + stem[1:]
            return normalized_present_stem
        return stem

    def simple_past(
        self,
        past_stem: str,
        prefix: str = "",
        compound_preverb: str = "",
        negative: bool = False,
        passive: bool = False,
        informal: bool = False,
    ) -> List[str]:
        """
        Generates the simple past or passive simple past tense conjugations for a given verb stem in Persian.
        Args:
            past_stem (str): The stem of the verb in the past tense.
            negative (bool, optional): If True, generates the negative form of the verb. Defaults to False.
            passive (bool, optional): If True, generates the passive form. Defaults to False.
            informal (bool, optional): If True, generates the informal form. Defaults to False.
        Returns:
            List[str]: A list of conjugated verb forms in the (passive) simple past tense for all persons.
        Example:
            conjugator = Conjugator()
            conjugator.simple_past("شناخت")
            # Returns: ['شناختم', 'شناختی', 'شناخت', 'شناختیم', 'شناختید', 'شناختند']
            conjugator.simple_past("شناخت", negative=True)
            # Returns: ['نشناختم', 'نشناختی', 'نشناخت', 'نشناختیم', 'نشناختید', 'نشناختند']
            conjugator.simple_past("شناخت", passive=True)
            # Returns: ['شناخته شدم', 'شناخته شدی', 'شناخته شد', 'شناخته شدیم', 'شناخته شدید', 'شناخته شدند']
            conjugator.simple_past("شناخت", negative=True, passive=True)
            # Returns: ['شناخته نشدم', 'شناخته نشدی', 'شناخته نشد', 'شناخته نشدیم', 'شناخته نشدید', 'شناخته نشدند']
        """

        prefix = self.normalize_prefix(prefix)
        compound_preverb = self.normalize_preverb(compound_preverb)
        y_after = y_before = ""

        suffixes = (
            self._informal_past_personal_suffixes
            if informal
            else self._past_personal_suffixes
        )
        negation_prefix = "ن" if negative else ""
        if not passive:
            # normalize stem in negative form آمد-> امد
            if negative:
                y_before, y_after = self.normalize_y(past_stem)
                past_stem = self.normalize_stem(past_stem)
            return [
                f"{compound_preverb}{prefix}{negation_prefix}{y_before}{past_stem}{suffix}"
                for suffix in suffixes
            ]
        else:
            auxiliary = "شد"
            return [
                f"{compound_preverb}{prefix}{past_stem}ه {negation_prefix}{y_before}{auxiliary}{suffix}"
                for suffix in suffixes
            ]

    def present_perfect(
        self,
        past_stem: str,
        prefix: str = "",
        compound_preverb: str = "",
        negative=False,
        passive=False,
        informal: bool = False,
    ) -> List[str]:
        """
        Generates the present perfect or passive present perfect tense conjugations for a given verb stem in Persian.
        Args:
            past_stem (str): The stem of the verb in the past tense.
            negative (bool, optional): If True, generates the negative form of the verb. Defaults to False.
            passive (bool, optional): If True, generates the passive form. Defaults to False.
            informal (bool, optional): If True, generates the informal form. Defaults to False.
        Returns:
            List[str]: A list of conjugated verb forms in the (passive) present perfect tense for all persons.
        Example:
            conjugator = Conjugator()
            conjugator.present_perfect("شناخت")
            # Returns: ['شناخته‌ام', 'شناخته‌ای', 'شناخته است', 'شناخته‌ایم', 'شناخته‌اید', 'شناخته‌اند']
            conjugator.present_perfect("شناخت", negative=True)
            # Returns: ['نشناخته‌ام', 'نشناخته‌ای', 'نشناخته است', 'نشناخته‌ایم', 'نشناخته‌اید', 'نشناخته‌اند']
            conjugator.present_perfect("شناخت", passive=True)
            # Returns: ['شناخته شده‌ام', 'شناخته شده‌ای', 'شناخته شده است', 'شناخته شده‌ایم', 'شناخته شده‌اید', 'شناخته شده‌اند']
            conjugator.present_perfect("شناخت", negative=True, passive=True)
            # Returns: ['شناخته نشده‌ام', 'شناخته نشده‌ای', 'شناخته نشده است', 'شناخته نشده‌ایم', 'شناخته نشده‌اید', 'شناخته نشده‌اند']
        """

        prefix = self.normalize_prefix(prefix)
        compound_preverb = self.normalize_preverb(compound_preverb)

        neg = "ن" if negative else ""
        auxiliary = "شده"
        y_after = y_before = ""

        if not passive:
            if negative:
                y_before, y_after = self.normalize_y(past_stem)
                past_stem = self.normalize_stem(past_stem)

            if not informal:
                return [
                    f"{compound_preverb}{prefix}{neg}{y_before}{past_stem}ه{suffix}"
                    for suffix in self._perfect_personal_suffixes
                ]
            else:
                informal_conjs = [
                    f"{compound_preverb}{prefix}{neg}{y_before}{past_stem}{suffix}"
                    for suffix in self._informal_past_personal_suffixes
                ]
                informal_conjs[2] = informal_conjs[2] + "ه"
                return informal_conjs
        else:
            if not informal:
                return [
                    f"{compound_preverb}{prefix}{past_stem}ه {neg}{auxiliary}{suffix}"
                    for suffix in self._perfect_personal_suffixes
                ]
            else:
                return self.simple_past(
                    past_stem,
                    prefix=prefix,
                    compound_preverb=compound_preverb,
                    negative=negative,
                    passive=True,
                    informal=True,
                )

    def past_continuous(
        self,
        past_stem: str,
        prefix: str = "",
        compound_preverb: str = "",
        negative=False,
        passive=False,
        informal: bool = False,
    ) -> List[str]:
        """
        Generates the past continuous or passive past continuous tense conjugations for a given verb stem in Persian.
        Args:
            past_stem (str): The stem of the verb in the past tense.
            negative (bool, optional): If True, generates the negative form of the verb. Defaults to False.
            passive (bool, optional): If True, generates the passive form. Defaults to False.
            informal (bool, optional): If True, generates the informal form. Defaults to False.
        Returns:
            List[str]: A list of conjugated verb forms in the (passive) past continuous tense for all persons.
        Example:
            conjugator = Conjugator()
            conjugator.past_continuous("شناخت")
            # Returns: ['می‌شناختم', 'می‌شناختی', 'می‌شناخت', 'می‌شناختیم', 'می‌شناختید', 'می‌شناختند']
            conjugator.past_continuous("شناخت", negative=True)
            # Returns: ['نمی‌شناختم', 'نمی‌شناختی', 'نمی‌شناخت', 'نمی‌شناختیم', 'نمی‌شناختید', 'نمی‌شناختند']
            conjugator.past_continuous("شناخت", passive=True)
            # Returns: ['شناخته می‌شدم', 'شناخته می‌شدی', 'شناخته می‌شد', 'شناخته می‌شدیم', 'شناخته می‌شدید', 'شناخته می‌شدند']
            conjugator.past_continuous("شناخت", negative=True, passive=True)
            # Returns: ['شناخته نمی‌شدم', 'شناخته نمی‌شدی', 'شناخته نمی‌شد', 'شناخته نمی‌شدیم', 'شناخته نمی‌شدید', 'شناخته نمی‌شدند']
        """

        prefix = self.normalize_prefix(prefix)
        compound_preverb = self.normalize_preverb(compound_preverb)

        negation_prefix = "ن" if negative else ""
        mi = "می‌"
        if not passive:
            if not informal:
                return [
                    f"{compound_preverb}{prefix}{negation_prefix}{mi}{past_stem}{suffix}"
                    for suffix in self._past_personal_suffixes
                ]
            else:
                return [
                    f"{compound_preverb}{prefix}{negation_prefix}{mi}{past_stem}{suffix}"
                    for suffix in self._informal_past_personal_suffixes
                ]
        else:
            auxiliary = "شد"
            if not informal:
                return [
                    f"{compound_preverb}{prefix}{past_stem}ه {negation_prefix}{mi}{auxiliary}{suffix}"
                    for suffix in self._past_personal_suffixes
                ]
            else:
                return [
                    f"{compound_preverb}{prefix}{past_stem}ه {negation_prefix}{mi}{auxiliary}{suffix}"
                    for suffix in self._informal_past_personal_suffixes
                ]

    def present_perfect_continuous(
        self,
        past_stem: str,
        prefix: str = "",
        compound_preverb: str = "",
        negative=False,
        passive=False,
    ) -> List[str]:
        """
        Generates the present perfect continuous or passive present perfect continuous tense conjugations for a given verb stem in Persian.
        Args:
            past_stem (str): The stem of the verb in the past tense.
            negative (bool, optional): If True, generates the negative form of the verb. Defaults to False.
            passive (bool, optional): If True, generates the passive form. Defaults to False.
        Returns:
            List[str]: A list of conjugated verb forms in the (passive) present perfect continuous tense for all persons.
        Example:
            conjugator = Conjugator()
            conjugator.present_perfect_continuous("شناخت")
            # Returns: ["می‌شناخته‌ام", "می‌شناخته‌ای", "می‌شناخته است", "می‌شناخته‌ایم", "می‌شناخته‌اید", "می‌شناخته‌اند"]
            conjugator.present_perfect_continuous("شناخت", negative=True)
            # Returns: ["نمی‌شناخته‌ام", "نمی‌شناخته‌ای", "نمی‌شناخته است", "نمی‌شناخته‌ایم", "نمی‌شناخته‌اید", "نمی‌شناخته‌اند"]
            conjugator.present_perfect_continuous("شناخت", passive=True)
            # Returns: ["شناخته می‌شده‌ام", "شناخته می‌شده‌ای", "شناخته می‌شده است", "شناخته می‌شده‌ایم", "شناخته می‌شده‌اید", "شناخته می‌شده‌اند"]
            conjugator.present_perfect_continuous("شناخت", negative=True, passive=True)
            # Returns: ["شناخته نمی‌شده‌ام", "شناخته نمی‌شده‌ای", "شناخته نمی‌شده است", "شناخته نمی‌شده‌ایم", "شناخته نمی‌شده‌اید", "شناخته نمی‌شده‌اند"]
        """

        prefix = self.normalize_prefix(prefix)
        compound_preverb = self.normalize_preverb(compound_preverb)

        negation_prefix = "ن" if negative else ""
        mi = "می‌"

        if not passive:
            return [
                f"{compound_preverb}{prefix}{negation_prefix}{mi}{past_stem}ه{suffix}"
                for suffix in self._perfect_personal_suffixes
            ]
        else:
            auxiliary = "شده"
            return [
                f"{compound_preverb}{prefix}{past_stem}ه {negation_prefix}{mi}{auxiliary}{suffix}"
                for suffix in self._perfect_personal_suffixes
            ]

    def past_perfect(
        self,
        past_stem: str,
        prefix: str = "",
        compound_preverb: str = "",
        negative=False,
        passive=False,
        informal=False,
    ) -> List[str]:
        """
        Generates the past perfect or passive past perfect tense conjugations for a given verb stem in Persian.
        Args:
            past_stem (str): The stem of the verb in the past tense.
            negative (bool, optional): If True, generates the negative form of the verb. Defaults to False.
            passive (bool, optional): If True, generates the passive form. Defaults to False.
            informal (bool, optional): If True, generates the informal form. Defaults to False.
        Returns:
            List[str]: A list of conjugated verb forms in the (passive) past perfect tense for all persons.
        Example:
            conjugator = Conjugator()
            conjugator.past_perfect("شناخت")
            # Returns: ['شناخته بودم', 'شناخته بودی', 'شناخته بود', 'شناخته بودیم', 'شناخته بودید', 'شناخته بودند']
            conjugator.past_perfect("شناخت", negative=True)
            # Returns: ['نشناخته بودم', 'نشناخته بودی', 'نشناخته بود', 'نشناخته بودیم', 'نشناخته بودید', 'نشناخته بودند']
            conjugator.past_perfect("شناخت", passive=True)
            # Returns: ['شناخته شده بودم', 'شناخته شده بودی', 'شناخته شده بود', 'شناخته شده بودیم', 'شناخته شده بودید', 'شناخته شده بودند']
            conjugator.past_perfect("شناخت", negative=True, passive=True)
            # Returns: ['شناخته نشده بودم', 'شناخته نشده بودی', 'شناخته نشده بود', 'شناخته نشده بودیم', 'شناخته نشده بودید', 'شناخته نشده بودند']
        """

        prefix = self.normalize_prefix(prefix)
        compound_preverb = self.normalize_preverb(compound_preverb)

        negation_prefix = "ن" if negative else ""
        auxiliary = "بود"
        y_before = y_after = ""

        if not passive:
            if negative:
                y_before, y_after = self.normalize_y(past_stem)
                past_stem = self.normalize_stem(past_stem)
            if not informal:
                return [
                    f"{compound_preverb}{prefix}{negation_prefix}{y_before}{past_stem}ه {auxiliary}{suffix}"
                    for suffix in self._past_personal_suffixes
                ]
            else:
                return [
                    f"{compound_preverb}{prefix}{negation_prefix}{y_before}{past_stem}ه {auxiliary}{suffix}"
                    for suffix in self._informal_past_personal_suffixes
                ]
        else:
            if not informal:
                return [
                    f"{compound_preverb}{prefix}{past_stem}ه {negation_prefix}شده {auxiliary}{suffix}"
                    for suffix in self._past_personal_suffixes
                ]
            else:
                return [
                    f"{compound_preverb}{prefix}{past_stem}ه {negation_prefix}شده {auxiliary}{suffix}"
                    for suffix in self._informal_past_personal_suffixes
                ]

    def past_perfect_of_past_perfect(
        self,
        past_stem: str,
        prefix: str = "",
        compound_preverb: str = "",
        negative=False,
        passive=False,
    ) -> List[str]:
        """
        Generates the past perfect of past perfect or passive past perfect of past perfect tense conjugations for a given verb stem in Persian.
        Args:
            past_stem (str): The stem of the verb in the past tense.
            negative (bool, optional): If True, generates the negative form of the verb. Defaults to False.
            passive (bool, optional): If True, generates the passive form. Defaults to False.
        Returns:
            List[str]: A list of conjugated verb forms in the (passive) past perfect of past perfect tense for all persons.
        Example:
            conjugator = Conjugator()
            conjugator.past_perfect_of_past_perfect("شناخت")
            # Returns: ['شناخته بوده‌ام', 'شناخته بوده‌ای', 'شناخته بوده است', 'شناخته بوده‌ایم', 'شناخته بوده‌اید', 'شناخته بوده‌اند']
            conjugator.past_perfect_of_past_perfect("شناخت", negative=True)
            # Returns: ['نشناخته بوده‌ام', 'نشناخته بوده‌ای', 'نشناخته بوده است', 'نشناخته بوده‌ایم', 'نشناخته بوده‌اید', 'نشناخته بوده‌اند']
            conjugator.past_perfect_of_past_perfect("شناخت", passive=True)
            # Returns: ['شناخته شده بوده‌ام', 'شناخته شده بوده‌ای', 'شناخته شده بوده است', 'شناخته شده بوده‌ایم', 'شناخته شده بوده‌اید', 'شناخته شده بوده‌اند']
            conjugator.past_perfect_of_past_perfect("شناخت", negative=True, passive=True)
            # Returns: ['شناخته نشده بوده‌ام', 'شناخته نشده بوده‌ای', 'شناخته نشده بوده است', 'شناخته نشده بوده‌ایم', 'شناخته نشده بوده‌اید', 'شناخته نشده بوده‌اند']
        """
        prefix = self.normalize_prefix(prefix)
        compound_preverb = self.normalize_preverb(compound_preverb)

        negation_prefix = "ن" if negative else ""
        auxiliary = "بوده"

        y_before = y_after = ""

        if not passive:
            if negative:
                y_before, y_after = self.normalize_y(past_stem)
                past_stem = self.normalize_stem(past_stem)

            return [
                f"{compound_preverb}{prefix}{negation_prefix}{y_before}{past_stem}ه {auxiliary}{suffix}"
                for suffix in self._perfect_personal_suffixes
            ]
        else:
            return [
                f"{compound_preverb}{prefix}{past_stem}ه {negation_prefix}شده {auxiliary}{suffix}"
                for suffix in self._perfect_personal_suffixes
            ]

    def past_subjunctive(
        self,
        past_stem: str,
        prefix: str = "",
        compound_preverb: str = "",
        negative=False,
        passive=False,
        informal: bool = False,
    ) -> List[str]:
        """
        Generates the past subjunctive or passive past subjunctive tense conjugations for a given verb stem in Persian.
        Args:
            past_stem (str): The stem of the verb in the past tense.
            negative (bool, optional): If True, generates the negative form of the verb. Defaults to False.
            passive (bool, optional): If True, generates the passive form. Defaults to False.
            informal (bool, optional): If True, generates the informal form. Defaults to False.
        Returns:
            List[str]: A list of conjugated verb forms in the (passive) past subjunctive tense for all persons.
        Example:
            conjugator = Conjugator()
            conjugator.past_subjunctive("شناخت")
            # Returns: ['شناخته باشم", 'شناخته باشی', 'شناخته باشد', 'شناخته باشیم', 'شناخته باشید', 'شناخته باشند']
            conjugator.past_subjunctive("شناخت", negative=True)
            # Returns: ['نشناخته باشم', 'نشناخته باشی', 'نشناخته باشد', 'نشناخته باشیم', 'نشناخته باشید', 'نشناخته باشند']
            conjugator.past_subjunctive("شناخت", passive=True)
            # Returns: ['شناخته شده باشم', 'شناخته شده باشی', 'شناخته شده باشد', 'شناخته شده باشیم', 'شناخته شده باشید', 'شناخته شده باشند']
            conjugator.past_subjunctive("شناخت", negative=True, passive=True)
            # Returns: ['شناخته نشده باشم', 'شناخته نشده باشی', 'شناخته نشده باشد', 'شناخته نشده باشیم', 'شناخته نشده باشید', 'شناخته نشده باشند']
        """

        prefix = self.normalize_prefix(prefix)
        compound_preverb = self.normalize_preverb(compound_preverb)

        negation_prefix = "ن" if negative else ""
        auxiliary = "باش"

        y_before = y_after = ""

        if not passive:
            if negative:
                y_before, y_after = self.normalize_y(past_stem)
                past_stem = self.normalize_stem(past_stem)

            if not informal:
                return [
                    f"{compound_preverb}{prefix}{negation_prefix}{y_before}{past_stem}ه {auxiliary}{suffix}"
                    for suffix in self._present_personal_suffixes
                ]

            else:
                informal_conjs = [
                    f"{compound_preverb}{prefix}{negation_prefix}{y_before}{past_stem}ه {auxiliary}{suffix}"
                    for suffix in self._informal_past_personal_suffixes
                ]

                informal_conjs[2] = informal_conjs[2] + "ه"
                return informal_conjs
        else:
            if not informal:
                return [
                    f"{compound_preverb}{prefix}{past_stem}ه {negation_prefix}شده {auxiliary}{suffix}"
                    for suffix in self._present_personal_suffixes
                ]
            else:
                informal_conjs = [
                    f"{compound_preverb}{prefix}{past_stem}ه {negation_prefix}شده {auxiliary}{suffix}"
                    for suffix in self._informal_past_personal_suffixes
                ]
                informal_conjs[2] = informal_conjs[2] + "ه"
                return informal_conjs

    def past_progressive(
        self,
        past_stem: str,
        prefix: str = "",
        compound_preverb: str = "",
        passive=False,
        informal=False,
    ) -> List[str]:
        """
        Generates the past progressive or passive past progressive tense conjugations for a given verb stem in Persian.
        Args:
            past_stem (str): The stem of the verb in the past tense.
            passive (bool, optional): If True, generates the passive form. Defaults to False.
            informal (bool, optional): If True, generates the informal form. Defaults to False.
        Returns:
            List[str]: A list of conjugated verb forms in the (passive) past progressive tense for all persons.
        Example:
            conjugator = Conjugator()
            conjugator.past_progressive("شناخت")
            # Returns: ['داشتم می‌شناختم', 'داشتی می‌شناختی', 'داشت می‌شناخت', 'داشتیم می‌شناختیم', 'داشتید می‌شناختید', 'داشتند می‌شناختند']
            conjugator.past_progressive("شناخت", passive=True)
            # Returns: ['داشتم شناخته می‌شدم', 'داشتی شناخته می‌شدی', 'داشت شناخته می‌شد', 'داشتیم شناخته می‌شدیم', 'داشتید شناخته می‌شدید', 'داشتند شناخته می‌شدند']
        """

        prefix = self.normalize_prefix(prefix)
        compound_preverb = self.normalize_preverb(compound_preverb)

        auxiliary = "داشت"
        mi = "می‌"
        suffixes = (
            self._informal_past_personal_suffixes
            if informal
            else self._past_personal_suffixes
        )

        if not passive:
            return [
                f"{auxiliary}{suffix} {compound_preverb}{prefix}{mi}{past_stem}{suffix}"
                for suffix in suffixes
            ]
        else:
            return [
                f"{auxiliary}{suffix} {compound_preverb}{prefix}{past_stem}ه {mi}شد{suffix}"
                for suffix in suffixes
            ]

    def past_perfect_progressive(
        self,
        past_stem: str,
        prefix: str = "",
        compound_preverb: str = "",
        passive=False,
    ) -> List[str]:
        """
        Generates the past perfect progressive or passive past perfect progressive tense conjugations for a given verb stem in Persian.
        Args:
            past_stem (str): The stem of the verb in the past tense.
            passive (bool, optional): If True, generates the passive form. Defaults to False.
        Returns:
            List[str]: A list of conjugated verb forms in the (passive) past perfect progressive tense for all persons.
        Example:
            conjugator = Conjugator()
            conjugator.past_perfect_progressive("شناخت")
            # Returns: ['داشته‌ام می‌شناخته‌ام', 'داشته‌ای می‌شناخته‌ای', 'داشته است می‌شناخته است', 'داشته‌ایم می‌شناخته‌ایم', 'داشته‌اید می‌شناخته‌اید', 'داشته‌اند می‌شناخته‌اند']
            conjugator.past_perfect_progressive("شناخت", passive=True)
            # Returns: ['داشته‌ام شناخته می‌شده‌ام', 'داشته‌ای شناخته می‌شده‌ای', 'داشته است شناخته می‌شده است', 'داشته‌ایم شناخته می‌شده‌ایم', 'داشته‌اید شناخته می‌شده‌اید', 'داشته‌اند شناخته می‌شده‌اند']
        """
        prefix = self.normalize_prefix(prefix)
        compound_preverb = self.normalize_preverb(compound_preverb)

        auxiliary = "داشته"
        mi = "می‌"

        if not passive:
            return [
                f"{auxiliary}{suffix} {compound_preverb}{prefix}{mi}{past_stem}ه{suffix}"
                for suffix in self._perfect_personal_suffixes
            ]
        else:
            return [
                f"{auxiliary}{suffix} {compound_preverb}{prefix}{past_stem}ه {mi}شده{suffix}"
                for suffix in self._perfect_personal_suffixes
            ]

    def simple_present(
        self,
        past_stem: str,
        present_stem: str,
        prefix: str = "",
        compound_preverb: str = "",
        negative=False,
        passive=False,
        informal: bool = False,
    ) -> List[str]:
        """
        Generates the simple present or passive simple present tense conjugations for a given verb stem in Persian.
        Args:
            present_stem (str): The stem of the verb in the present tense.
            negative (bool, optional): If True, generates the negative form. Defaults to False.
            passive (bool, optional): If True, generates the passive form. Defaults to False.
        Returns:
            List[str]: A list of conjugated verb forms in the (passive) simple present tense for all persons.
        Example:
            conjugator = Conjugator()
            conjugator.simple_present("شناس", "شناخت")
            # Returns: ['شناسم', 'شناسی', 'شناسد', 'شناسیم', 'شناسید', 'شناسند']
            conjugator.simple_present("شناس", "شناخت", negative=True)
            # Returns: ['نشناسم', 'نشناسی', 'نشناسد', 'نشناسیم', 'نشناسید', 'نشناسند']
            conjugator.simple_present("شناس", "شناخت", passive=True)
            # Returns: ['شناخته شوم', 'شناخته شوی', 'شناخته شود', 'شناخته شویم', 'شناخته شوید', 'شناخته شوند']
            conjugator.simple_present("شناس", "شناخت", negative=True, passive=True)
            # Returns: ['شناخته نشوم', 'شناخته نشوی', 'شناخته نشود', 'شناخته نشویم', 'شناخته نشوید', 'شناخته نشوند']
        """

        prefix = self.normalize_prefix(prefix)
        compound_preverb = self.normalize_preverb(compound_preverb)

        negation_prefix = "ن" if negative else ""
        y_before = y_after = ""
        if not passive:
            _, y_after = self.normalize_y(present_stem)
            if negative:
                y_before, y_after = self.normalize_y(present_stem)
                present_stem = self.normalize_stem(present_stem)

            if not informal:
                return [
                    f"{compound_preverb}{prefix}{negation_prefix}{y_before}{present_stem}{y_after}{suffix}"
                    for suffix in self._present_personal_suffixes
                ]
            else:
                informal_conjs = [
                    f"{compound_preverb}{prefix}{negation_prefix}{y_before}{present_stem}{suffix}"
                    for suffix in self._informal_past_personal_suffixes
                ]

                if not informal_conjs[2].endswith("ا"):
                    informal_conjs[2] = informal_conjs[2] + "ه"
                else:
                    informal_conjs[2] = informal_conjs[2] + "د"

                return informal_conjs
        else:
            if not informal:
                auxiliary = "شو"
                return [
                    f"{compound_preverb}{prefix}{past_stem}ه {negation_prefix}{auxiliary}{suffix}"
                    for suffix in self._present_personal_suffixes
                ]
            else:
                auxiliary = "ش"
                informal_conjs = [
                    f"{compound_preverb}{prefix}{past_stem}ه {negation_prefix}{auxiliary}{suffix}"
                    for suffix in self._informal_past_personal_suffixes
                ]
                informal_conjs[2] = informal_conjs[2] + "ه"
                return informal_conjs

    def present_indicative(
        self,
        past_stem: str,
        present_stem: str,
        prefix: str = "",
        compound_preverb: str = "",
        negative=False,
        passive=False,
        informal: bool = False,
    ) -> List[str]:
        """
        Generates the present indicative or passive present indicative tense conjugations for a given verb stem in Persian.
        Args:
            present_stem (str): The stem of the verb in the present tense.
            negative (bool, optional): If True, generates the negative form. Defaults to False.
            passive (bool, optional): If True, generates the passive form. Defaults to False.
        Returns:
            List[str]: A list of conjugated verb forms in the (passive) present indicative tense for all persons.
        Example:
            conjugator = Conjugator()
            conjugator.present_indicative("شناس", "شناخت")
            # Returns: ['می‌شناسم', 'می‌شناسی', 'می‌شناسد', 'می‌شناسیم', 'می‌شناسید', 'می‌شناسند']
            conjugator.present_indicative("شناس", "شناخت", negative=True)
            # Returns: ['نمی‌شناسم', 'نمی‌شناسی', 'نمی‌شناسد', 'نمی‌شناسیم', 'نمی‌شناسید', 'نمی‌شناسند']
            conjugator.present_indicative("شناس", "شناخت", passive=True)
            # Returns: ['شناخته می‌شوم', 'شناخته می‌شوی', 'شناخته می‌شود', 'شناخته می‌شویم', 'شناخته می‌شوید', 'شناخته می‌شوند']
            conjugator.present_indicative("شناس", "شناخت", negative=True, passive=True)
            # Returns: ['شناخته نمی‌شوم', 'شناخته نمی‌شوی', 'شناخته نمی‌شود', 'شناخته نمی‌شویم', 'شناخته نمی‌شوید', 'شناخته نمی‌شوند']
        """

        prefix = self.normalize_prefix(prefix)
        compound_preverb = self.normalize_preverb(compound_preverb)

        negation_prefix = "ن" if negative else ""
        mi = "می‌"

        if not passive:
            y_before, y_after = self.normalize_y(present_stem)
            if not informal:
                return [
                    f"{compound_preverb}{prefix}{negation_prefix}{mi}{present_stem}{y_after}{suffix}"
                    for suffix in self._present_personal_suffixes
                ]
            else:
                informal_conjs = [
                    f"{compound_preverb}{prefix}{negation_prefix}{mi}{present_stem}{y_after}{suffix}"
                    for suffix in self._informal_past_personal_suffixes + ["ید"]
                ]
                informal_conjs[2] = informal_conjs[2] + "ه"
                return informal_conjs
        else:
            if not informal:
                auxiliary = "شو"
                return [
                    f"{compound_preverb}{prefix}{past_stem}ه {negation_prefix}{mi}{auxiliary}{suffix}"
                    for suffix in self._present_personal_suffixes
                ]
            else:
                auxiliary = "ش"
                informal_conjs = [
                    f"{compound_preverb}{prefix}{past_stem}ه {negation_prefix}{mi}{auxiliary}{suffix}"
                    for suffix in self._informal_past_personal_suffixes + ["ید"]
                ]
                informal_conjs[2] = informal_conjs[2] + "ه"
                return informal_conjs

    def present_subjunctive(
        self,
        past_stem: str,
        present_stem: str,
        prefix: str = "",
        compound_preverb: str = "",
        negative=False,
        passive=False,
        informal: bool = False,
    ) -> List[str]:
        """
        Generates the present subjunctive or passive present subjunctive tense conjugations for a given verb stem in Persian.
        Args:
            present_stem (str): The stem of the verb in the present tense.
            negative (bool, optional): If True, generates the negative form. Defaults to False.
            passive (bool, optional): If True, generates the passive form. Defaults to False.
            informal (bool, optional): If True, generates the informal form. Defaults to False.
        Returns:
            List[str]: A list of conjugated verb forms in the (passive) present subjunctive tense for all persons.
        Example:
            conjugator = Conjugator()
            conjugator.present_subjunctive("شناس", "شناخت")
            # Returns: ['بشناسم', 'بشناسی', 'بشناسد', 'بشناسیم', 'بشناسید', 'بشناسند']
            conjugator.present_subjunctive("شناس", "شناخت", negative=True)
            # Returns: ['نشناسم', 'نشناسی', 'نشناسد', 'نشناسیم', 'نشناسید', 'نشناسند']
            conjugator.present_subjunctive("شناس", "شناخت", passive=True)
            # Returns: ['شناخته بشوم', 'شناخته بشوی', 'شناخته بشود', 'شناخته بشویم', 'شناخته بشوید', 'شناخته بشوند']
            conjugator.present_subjunctive("شناس", "شناخت", negative=True, passive=True)
            # Returns: ['شناخته نشوم', 'شناخته نشوی', 'شناخته نشود', 'شناخته نشویم', 'شناخته نشوید', 'شناخته نشوند']
        """

        prefix = self.normalize_prefix(prefix)
        compound_preverb = self.normalize_preverb(compound_preverb)

        subjunctive_prefix = "ن" if negative else "ب"

        auxiliary = "شو"
        if not passive:
            y_before, y_after = self.normalize_y(present_stem)
            normalized_present_stem = self.normalize_stem(present_stem)

            if not informal:
                conjs = []

                if prefix and not negative:
                    # باید بازگردیم!
                    conjs.extend(
                        [
                            f"{compound_preverb}{prefix}{present_stem}{y_after}{suffix}"
                            for suffix in self._present_personal_suffixes
                        ]
                    )

                conjs.extend(
                    [
                        f"{compound_preverb}{prefix}{subjunctive_prefix}{y_before}{normalized_present_stem}{y_after}{suffix}"
                        for suffix in self._present_personal_suffixes
                    ]
                )

                return conjs

            else:
                informal_conjs = [
                    f"{compound_preverb}{prefix}{subjunctive_prefix}{y_before}{normalized_present_stem}{suffix}"
                    for suffix in self._informal_past_personal_suffixes + ["ید"]
                ]

                if not informal_conjs[2].endswith("ا"):
                    informal_conjs[2] = informal_conjs[2] + "ه"
                else:
                    informal_conjs[2] = informal_conjs[2] + "د"

                return informal_conjs
        else:
            if not informal:
                return [
                    f"{compound_preverb}{prefix}{past_stem}ه {subjunctive_prefix}{auxiliary}{suffix}"
                    for suffix in self._present_personal_suffixes
                ]
            else:
                auxiliary = "ش"
                informal_conjs = [
                    f"{compound_preverb}{prefix}{past_stem}ه {subjunctive_prefix}{auxiliary}{suffix}"
                    for suffix in self._informal_past_personal_suffixes + ["ید"]
                ]

                informal_conjs[2] = informal_conjs[2] + "ه"
                return informal_conjs

    def present_progressive(
        self,
        past_stem: str,
        present_stem: str,
        prefix: str = "",
        compound_preverb: str = "",
        passive=False,
        informal: bool = False,
    ) -> List[str]:
        """
        Generates the present progressive or passive present progressive tense conjugations for a given verb stem in Persian.
        Args:
            present_stem (str): The stem of the verb in the present tense.
            passive (bool, optional): If True, generates the passive form. Defaults to False.
        Returns:
            List[str]: A list of conjugated verb forms in the (passive) present progressive tense for all persons.
        Example:
            conjugator = Conjugator()
            conjugator.present_progressive("شناس", "شناخت")
            # Returns: ['دارم می‌شناسم', 'داری می‌شناسی', 'دارد می‌شناسد', 'داریم می‌شناسیم', 'دارید می‌شناسید', 'دارند می‌شناسند']
            conjugator.present_progressive("شناس", "شناخت", passive=True)
            # Returns: ['دارم شناخته می‌شوم', 'داری شناخته می‌شوی', 'دارد شناخته می‌شود', 'داریم شناخته می‌شویم', 'دارید شناخته می‌شوید', 'دارند شناخته می‌شوند']
        """

        prefix = self.normalize_prefix(prefix)
        compound_preverb = self.normalize_preverb(compound_preverb)

        first_auxiliary_stem = "دار"
        second_auxiliary_stem = "شو"
        mi = "می‌"

        if not passive:
            if not informal:
                return [
                    f"{first_auxiliary_stem}{suffix} {compound_preverb}{prefix}{mi}{present_stem}{suffix}"
                    for suffix in self._present_personal_suffixes
                ]
            else:
                suffixes = self._informal_past_personal_suffixes + ["ید"]
                suffixes[2] = "ه"
                informal_conjs = [
                    f"{first_auxiliary_stem}{suffix} {compound_preverb}{prefix}{mi}{present_stem}{suffix}"
                    for suffix in suffixes
                ]
                if present_stem[-1] == "ا" or present_stem[-1] == "آ":
                    informal_conjs[2] = informal_conjs[2][:-1] + "د"
                return informal_conjs
        else:
            if not informal:
                return [
                    f"{first_auxiliary_stem}{suffix} {compound_preverb}{prefix}{past_stem}ه {mi}{second_auxiliary_stem}{suffix}"
                    for suffix in self._present_personal_suffixes
                ]
            else:
                second_auxiliary_stem = "ش"
                suffixes = self._informal_past_personal_suffixes + ["ید"]
                suffixes[2] = "ه"
                return [
                    f"{first_auxiliary_stem}{suffix} {compound_preverb}{prefix}{past_stem}ه {mi}{second_auxiliary_stem}{suffix}"
                    for suffix in suffixes
                ]

    def simple_future(
        self,
        past_stem: str,
        prefix: str = "",
        compound_preverb: str = "",
        negative=False,
        passive=False,
    ) -> List[str]:
        """
        Generates the future simple or passive future simple tense conjugations for a given verb stem in Persian.
        Args:
            present_stem (str): The stem of the verb in the present tense.
            negative (bool, optional): If True, generates the negative form. Defaults to False.
            passive (bool, optional): If True, generates the passive form. Defaults to False.
        Returns:
            List[str]: A list of conjugated verb forms in the (passive) future simple tense for all persons.
        Example:
            conjugator = Conjugator()
            conjugator.future_simple("شناخت")
            # Returns: ['خواهم شناخت', 'خواهی شناخت', 'خواهد شناخت', 'خواهیم شناخت', 'خواهید شناخت', 'خواهند شناخت']
            conjugator.future_simple("شناخت", negative=True)
            # Returns: ['نخواهم شناخت', 'نخواهی شناخت', 'نخواهد شناخت', 'نخواهیم شناخت', 'نخواهید شناخت', 'نخواهند شناخت']
            conjugator.future_simple("شناخت", passive=True)
            # Returns: ['شناخته خواهم شد', 'شناخته خواهی شد', 'شناخته خواهد شد', 'شناخته خواهیم شد', 'شناخته خواهید شد', 'شناخته خواهند شد']
            conjugator.future_simple("شناخت", negative=True, passive=True)
            # Returns: ['شناخته نخواهم شد', 'شناخته نخواهی شد', 'شناخته نخواهد شد', 'شناخته نخواهیم شد', 'شناخته نخواهید شد', 'شناخته نخواهند شد']
        """
        # Based on apll.ir
        # Verbal prefix separated by an auxiliary verb,
        # should lead with a space.
        # Effectivly treated just like a compound prefix!

        normalized_prefix = self.normalize_prefix(prefix)
        spaced_prefix = self.normalize_preverb(prefix)
        compound_preverb = self.normalize_preverb(compound_preverb)

        negation_prefix = "ن" if negative else ""
        auxiliary = "خواه"

        if not passive:
            return [
                f"{compound_preverb}{spaced_prefix}{negation_prefix}{auxiliary}{suffix} {past_stem}"
                for suffix in self._present_personal_suffixes
            ]
        else:
            return [
                f"{compound_preverb}{normalized_prefix}{past_stem}ه {negation_prefix}{auxiliary}{suffix} شد"
                for suffix in self._present_personal_suffixes
            ]

    def imperative(
        self,
        present_stem: str,
        prefix: str = "",
        compound_preverb: str = "",
        negative: bool = False,
        informal: bool = False,
    ) -> List[str]:
        """
        Generates the imperative tense conjugations for a given verb stem in Persian.

        Args:
            present_stem (str, optional): The stem of the verb in the present tense.
            negative (bool, optional): If True, generates the negative form of the verb. Defaults to False.
        Returns:
            List[str]: A list containing all conjugated forms of the verb in the imperative tense.
        Example:
            conjugator = Conjugator()
            conjugator.imperative("شناس")
            # Returns: ['بشناس', 'بشناسید']
            conjugator.imperative("شناس", negative=True)
            # Returns: ['نشناس', 'نشناسید']
        """

        prefix = self.normalize_prefix(prefix)
        compound_preverb = self.normalize_preverb(compound_preverb)

        y_before, y_after = self.normalize_y(present_stem)

        normalized_present_stem = self.normalize_stem(present_stem)

        imperative_prefix = "ب" if not negative else "ن"

        if not informal:
            conjs = []

            if prefix and not negative:
                # باید بازگردیم!
                conjs.extend(
                    [
                        f"{compound_preverb}{prefix}{present_stem}",
                        f"{compound_preverb}{prefix}{present_stem}{y_after}ید",
                    ]
                )

            conjs.extend(
                [
                    f"{compound_preverb}{prefix}{imperative_prefix}{y_before}{normalized_present_stem}",
                    f"{compound_preverb}{prefix}{imperative_prefix}{y_before}{normalized_present_stem}{y_after}ید",
                ]
            )

            return conjs

        else:
            return [
                f"{compound_preverb}{prefix}{imperative_prefix}{y_before}{normalized_present_stem}",
                f"{compound_preverb}{prefix}{imperative_prefix}{y_before}{normalized_present_stem}ید",
                f"{compound_preverb}{prefix}{imperative_prefix}{y_before}{normalized_present_stem}ین",
            ]

    def conjugate(
        self,
        past_stem: str = None,
        present_stem: str = None,
        informal_past_stem: str = None,
        informal_present_stem: str = None,
        prefix: str = "",
    ) -> List[str]:
        """
        Generates all conjugations for a given verb in all tenses.

        Args:
            past_stem (str): The stem of the verb in the past tense.
            present_stem (str, optional): The stem of the verb in the present tense.
            If not provided, only past tenses will be conjugated.

        Returns:
            dict: A list containing all conjugated forms of the verb in different tenses.
        """
        conjugations = []
        if past_stem:
            infinitive = past_stem + "ن"
            past_participle = past_stem + "ه"
            conjugations.append(infinitive)
            conjugations.append(past_participle)

            conjugations.extend(self.simple_past(past_stem, prefix=prefix))
            conjugations.extend(
                self.simple_past(past_stem, prefix=prefix, negative=True)
            )
            conjugations.extend(
                self.simple_past(past_stem, prefix=prefix, passive=True)
            )
            conjugations.extend(
                self.simple_past(past_stem, prefix=prefix, negative=True, passive=True)
            )

            # Weird cases of formal informal mixing

            conjugations.extend(
                self.simple_past(past_stem, prefix=prefix, informal=True)
            )
            conjugations.extend(
                self.simple_past(past_stem, prefix=prefix, negative=True, informal=True)
            )
            conjugations.extend(
                self.simple_past(past_stem, prefix=prefix, passive=True, informal=True)
            )
            conjugations.extend(
                self.simple_past(
                    past_stem, prefix=prefix, negative=True, passive=True, informal=True
                )
            )

            if informal_past_stem:
                conjugations.extend(
                    self.simple_past(informal_past_stem, prefix=prefix, informal=True)
                )
                conjugations.extend(
                    self.simple_past(
                        informal_past_stem, prefix=prefix, negative=True, informal=True
                    )
                )
                conjugations.extend(
                    self.simple_past(
                        informal_past_stem, prefix=prefix, passive=True, informal=True
                    )
                )
                conjugations.extend(
                    self.simple_past(
                        informal_past_stem,
                        prefix=prefix,
                        negative=True,
                        passive=True,
                        informal=True,
                    )
                )

            conjugations.extend(
                self.past_continuous(
                    past_stem,
                    prefix=prefix,
                )
            )
            conjugations.extend(
                self.past_continuous(past_stem, prefix=prefix, negative=True)
            )
            conjugations.extend(
                self.past_continuous(past_stem, prefix=prefix, passive=True)
            )
            conjugations.extend(
                self.past_continuous(
                    past_stem, prefix=prefix, negative=True, passive=True
                )
            )

            # Weird mix of formal informal
            conjugations.extend(
                self.past_continuous(past_stem, prefix=prefix, informal=True)
            )
            conjugations.extend(
                self.past_continuous(
                    past_stem, prefix=prefix, negative=True, informal=True
                )
            )
            conjugations.extend(
                self.past_continuous(
                    past_stem, prefix=prefix, passive=True, informal=True
                )
            )
            conjugations.extend(
                self.past_continuous(
                    past_stem, prefix=prefix, negative=True, passive=True, informal=True
                )
            )

            if informal_past_stem:
                conjugations.extend(
                    self.past_continuous(
                        informal_past_stem, prefix=prefix, informal=True
                    )
                )
                conjugations.extend(
                    self.past_continuous(
                        informal_past_stem, prefix=prefix, negative=True, informal=True
                    )
                )
                conjugations.extend(
                    self.past_continuous(
                        informal_past_stem, prefix=prefix, passive=True, informal=True
                    )
                )
                conjugations.extend(
                    self.past_continuous(
                        informal_past_stem,
                        prefix=prefix,
                        negative=True,
                        passive=True,
                        informal=True,
                    )
                )

            conjugations.extend(
                self.present_perfect(
                    past_stem,
                    prefix=prefix,
                )
            )
            conjugations.extend(
                self.present_perfect(past_stem, prefix=prefix, negative=True)
            )
            conjugations.extend(
                self.present_perfect(past_stem, prefix=prefix, passive=True)
            )
            conjugations.extend(
                self.present_perfect(
                    past_stem, prefix=prefix, negative=True, passive=True
                )
            )

            # Weird mix of formal informal
            conjugations.extend(
                self.present_perfect(past_stem, prefix=prefix, informal=True)
            )
            conjugations.extend(
                self.present_perfect(
                    past_stem, prefix=prefix, negative=True, informal=True
                )
            )
            conjugations.extend(
                self.present_perfect(
                    past_stem, prefix=prefix, passive=True, informal=True
                )
            )
            conjugations.extend(
                self.present_perfect(
                    past_stem, prefix=prefix, negative=True, passive=True, informal=True
                )
            )

            if informal_past_stem:
                conjugations.extend(
                    self.present_perfect(
                        informal_past_stem, prefix=prefix, informal=True
                    )
                )
                conjugations.extend(
                    self.present_perfect(
                        informal_past_stem, prefix=prefix, negative=True, informal=True
                    )
                )
                conjugations.extend(
                    self.present_perfect(
                        informal_past_stem, prefix=prefix, passive=True, informal=True
                    )
                )
                conjugations.extend(
                    self.present_perfect(
                        informal_past_stem,
                        prefix=prefix,
                        negative=True,
                        passive=True,
                        informal=True,
                    )
                )

            conjugations.extend(
                self.present_perfect_continuous(past_stem, prefix=prefix)
            )
            conjugations.extend(
                self.present_perfect_continuous(past_stem, prefix=prefix, negative=True)
            )
            conjugations.extend(
                self.present_perfect_continuous(past_stem, prefix=prefix, passive=True)
            )
            conjugations.extend(
                self.present_perfect_continuous(
                    past_stem, prefix=prefix, negative=True, passive=True
                )
            )

            conjugations.extend(
                self.past_perfect(
                    past_stem,
                    prefix=prefix,
                )
            )
            conjugations.extend(
                self.past_perfect(past_stem, prefix=prefix, negative=True)
            )
            conjugations.extend(
                self.past_perfect(past_stem, prefix=prefix, passive=True)
            )
            conjugations.extend(
                self.past_perfect(past_stem, prefix=prefix, negative=True, passive=True)
            )

            # Weird mix of formal informal
            conjugations.extend(
                self.past_perfect(past_stem, prefix=prefix, informal=True)
            )
            conjugations.extend(
                self.past_perfect(
                    past_stem, prefix=prefix, negative=True, informal=True
                )
            )
            conjugations.extend(
                self.past_perfect(past_stem, prefix=prefix, passive=True, informal=True)
            )
            conjugations.extend(
                self.past_perfect(
                    past_stem, prefix=prefix, negative=True, passive=True, informal=True
                )
            )

            if informal_past_stem:
                conjugations.extend(
                    self.past_perfect(informal_past_stem, prefix=prefix, informal=True)
                )
                conjugations.extend(
                    self.past_perfect(
                        informal_past_stem, prefix=prefix, negative=True, informal=True
                    )
                )
                conjugations.extend(
                    self.past_perfect(
                        informal_past_stem, prefix=prefix, passive=True, informal=True
                    )
                )
                conjugations.extend(
                    self.past_perfect(
                        informal_past_stem,
                        prefix=prefix,
                        negative=True,
                        passive=True,
                        informal=True,
                    )
                )

            conjugations.extend(
                self.past_perfect_of_past_perfect(past_stem, prefix=prefix)
            )
            conjugations.extend(
                self.past_perfect_of_past_perfect(
                    past_stem, prefix=prefix, negative=True
                )
            )
            conjugations.extend(
                self.past_perfect_of_past_perfect(
                    past_stem, prefix=prefix, passive=True
                )
            )
            conjugations.extend(
                self.past_perfect_of_past_perfect(
                    past_stem, prefix=prefix, negative=True, passive=True
                )
            )

            conjugations.extend(
                self.past_subjunctive(
                    past_stem,
                    prefix=prefix,
                )
            )
            conjugations.extend(
                self.past_subjunctive(past_stem, prefix=prefix, negative=True)
            )
            conjugations.extend(
                self.past_subjunctive(past_stem, prefix=prefix, passive=True)
            )
            conjugations.extend(
                self.past_subjunctive(
                    past_stem, prefix=prefix, negative=True, passive=True
                )
            )

            # Weird mix of formal informal
            conjugations.extend(
                self.past_subjunctive(past_stem, prefix=prefix, informal=True)
            )
            conjugations.extend(
                self.past_subjunctive(
                    past_stem, prefix=prefix, negative=True, informal=True
                )
            )
            conjugations.extend(
                self.past_subjunctive(
                    past_stem, prefix=prefix, passive=True, informal=True
                )
            )
            conjugations.extend(
                self.past_subjunctive(
                    past_stem, prefix=prefix, negative=True, passive=True, informal=True
                )
            )

            if informal_past_stem:
                conjugations.extend(
                    self.past_subjunctive(
                        informal_past_stem, prefix=prefix, informal=True
                    )
                )
                conjugations.extend(
                    self.past_subjunctive(
                        informal_past_stem, prefix=prefix, negative=True, informal=True
                    )
                )
                conjugations.extend(
                    self.past_subjunctive(
                        informal_past_stem, prefix=prefix, passive=True, informal=True
                    )
                )
                conjugations.extend(
                    self.past_subjunctive(
                        informal_past_stem,
                        prefix=prefix,
                        negative=True,
                        passive=True,
                        informal=True,
                    )
                )

            conjugations.extend(
                self.past_progressive(
                    past_stem,
                    prefix=prefix,
                )
            )
            conjugations.extend(
                self.past_progressive(past_stem, prefix=prefix, passive=True)
            )

            # mixed formal informal
            conjugations.extend(
                self.past_progressive(past_stem, prefix=prefix, informal=True)
            )
            conjugations.extend(
                self.past_progressive(
                    past_stem, prefix=prefix, passive=True, informal=True
                )
            )
            if informal_past_stem:
                conjugations.extend(
                    self.past_progressive(
                        informal_past_stem, prefix=prefix, informal=True
                    )
                )
                conjugations.extend(
                    self.past_progressive(
                        informal_past_stem, prefix=prefix, passive=True, informal=True
                    )
                )

            conjugations.extend(
                self.past_perfect_progressive(
                    past_stem,
                    prefix=prefix,
                )
            )
            conjugations.extend(
                self.past_perfect_progressive(past_stem, prefix=prefix, passive=True)
            )

        # Present and future tenses (require present stem)
        if present_stem:
            conjugations.extend(
                self.simple_present(past_stem, present_stem, prefix=prefix)
            )
            conjugations.extend(
                self.simple_present(
                    past_stem, present_stem, prefix=prefix, negative=True
                )
            )
            conjugations.extend(
                self.simple_present(
                    past_stem, present_stem, prefix=prefix, passive=True
                )
            )
            conjugations.extend(
                self.simple_present(
                    past_stem, present_stem, prefix=prefix, negative=True, passive=True
                )
            )

            # mix of formal informal
            conjugations.extend(
                self.simple_present(
                    past_stem, present_stem, prefix=prefix, informal=True
                )
            )
            conjugations.extend(
                self.simple_present(
                    past_stem, present_stem, prefix=prefix, negative=True, informal=True
                )
            )
            conjugations.extend(
                self.simple_present(
                    past_stem, present_stem, prefix=prefix, passive=True, informal=True
                )
            )
            conjugations.extend(
                self.simple_present(
                    past_stem,
                    present_stem,
                    prefix=prefix,
                    negative=True,
                    passive=True,
                    informal=True,
                )
            )
            if informal_present_stem and informal_past_stem:
                conjugations.extend(
                    self.simple_present(
                        informal_past_stem,
                        informal_present_stem,
                        prefix=prefix,
                        informal=True,
                    )
                )
                conjugations.extend(
                    self.simple_present(
                        informal_past_stem,
                        informal_present_stem,
                        prefix=prefix,
                        negative=True,
                        informal=True,
                    )
                )
                conjugations.extend(
                    self.simple_present(
                        informal_past_stem,
                        informal_present_stem,
                        prefix=prefix,
                        passive=True,
                        informal=True,
                    )
                )
                conjugations.extend(
                    self.simple_present(
                        informal_past_stem,
                        informal_present_stem,
                        prefix=prefix,
                        negative=True,
                        passive=True,
                        informal=True,
                    )
                )

            conjugations.extend(
                self.present_indicative(past_stem, present_stem, prefix=prefix)
            )
            conjugations.extend(
                self.present_indicative(
                    past_stem, present_stem, prefix=prefix, negative=True
                )
            )
            conjugations.extend(
                self.present_indicative(
                    past_stem, present_stem, prefix=prefix, passive=True
                )
            )
            conjugations.extend(
                self.present_indicative(
                    past_stem, present_stem, prefix=prefix, negative=True, passive=True
                )
            )

            # mix of formal informal
            conjugations.extend(
                self.present_indicative(
                    past_stem, present_stem, prefix=prefix, informal=True
                )
            )
            conjugations.extend(
                self.present_indicative(
                    past_stem, present_stem, prefix=prefix, negative=True, informal=True
                )
            )
            conjugations.extend(
                self.present_indicative(
                    past_stem, present_stem, prefix=prefix, passive=True, informal=True
                )
            )
            conjugations.extend(
                self.present_indicative(
                    past_stem,
                    present_stem,
                    prefix=prefix,
                    negative=True,
                    passive=True,
                    informal=True,
                )
            )

            if informal_present_stem and informal_past_stem:
                conjugations.extend(
                    self.present_indicative(
                        informal_past_stem,
                        informal_present_stem,
                        prefix=prefix,
                        informal=True,
                    )
                )
                conjugations.extend(
                    self.present_indicative(
                        informal_past_stem,
                        informal_present_stem,
                        prefix=prefix,
                        negative=True,
                        informal=True,
                    )
                )
                conjugations.extend(
                    self.present_indicative(
                        informal_past_stem,
                        informal_present_stem,
                        prefix=prefix,
                        passive=True,
                        informal=True,
                    )
                )
                conjugations.extend(
                    self.present_indicative(
                        informal_past_stem,
                        informal_present_stem,
                        prefix=prefix,
                        negative=True,
                        passive=True,
                        informal=True,
                    )
                )

            conjugations.extend(
                self.present_subjunctive(past_stem, present_stem, prefix=prefix)
            )
            conjugations.extend(
                self.present_subjunctive(
                    past_stem, present_stem, prefix=prefix, negative=True
                )
            )
            conjugations.extend(
                self.present_subjunctive(
                    past_stem, present_stem, prefix=prefix, passive=True
                )
            )
            conjugations.extend(
                self.present_subjunctive(
                    past_stem, present_stem, prefix=prefix, negative=True, passive=True
                )
            )

            # mix of formal informal
            conjugations.extend(
                self.present_subjunctive(
                    past_stem, present_stem, prefix=prefix, informal=True
                )
            )
            conjugations.extend(
                self.present_subjunctive(
                    past_stem, present_stem, prefix=prefix, negative=True, informal=True
                )
            )
            conjugations.extend(
                self.present_subjunctive(
                    past_stem, present_stem, prefix=prefix, passive=True, informal=True
                )
            )
            conjugations.extend(
                self.present_subjunctive(
                    past_stem,
                    present_stem,
                    prefix=prefix,
                    negative=True,
                    passive=True,
                    informal=True,
                )
            )

            if informal_present_stem and informal_past_stem:
                conjugations.extend(
                    self.present_subjunctive(
                        informal_past_stem,
                        informal_present_stem,
                        prefix=prefix,
                        informal=True,
                    )
                )
                conjugations.extend(
                    self.present_subjunctive(
                        informal_past_stem,
                        informal_present_stem,
                        prefix=prefix,
                        negative=True,
                        informal=True,
                    )
                )
                conjugations.extend(
                    self.present_subjunctive(
                        informal_past_stem,
                        informal_present_stem,
                        prefix=prefix,
                        passive=True,
                        informal=True,
                    )
                )
                conjugations.extend(
                    self.present_subjunctive(
                        informal_past_stem,
                        informal_present_stem,
                        prefix=prefix,
                        negative=True,
                        passive=True,
                        informal=True,
                    )
                )

            conjugations.extend(
                self.present_progressive(past_stem, present_stem, prefix=prefix)
            )
            conjugations.extend(
                self.present_progressive(
                    past_stem, present_stem, prefix=prefix, passive=True
                )
            )

            # mix of formal informal
            conjugations.extend(
                self.present_progressive(
                    past_stem, present_stem, prefix=prefix, informal=True
                )
            )
            conjugations.extend(
                self.present_progressive(
                    past_stem, present_stem, prefix=prefix, passive=True, informal=True
                )
            )
            if informal_present_stem and informal_past_stem:
                conjugations.extend(
                    self.present_progressive(
                        informal_past_stem,
                        informal_present_stem,
                        prefix=prefix,
                        informal=True,
                    )
                )
                conjugations.extend(
                    self.present_progressive(
                        informal_past_stem,
                        informal_present_stem,
                        prefix=prefix,
                        passive=True,
                        informal=True,
                    )
                )

            conjugations.extend(self.simple_future(past_stem, prefix=prefix))
            conjugations.extend(
                self.simple_future(past_stem, prefix=prefix, negative=True)
            )
            conjugations.extend(
                self.simple_future(past_stem, prefix=prefix, passive=True)
            )
            conjugations.extend(
                self.simple_future(
                    past_stem, prefix=prefix, negative=True, passive=True
                )
            )

            conjugations.extend(
                self.imperative(
                    present_stem,
                    prefix=prefix,
                )
            )
            conjugations.extend(
                self.imperative(present_stem, prefix=prefix, negative=True)
            )

            # mix of formal informal
            conjugations.extend(
                self.imperative(present_stem, prefix=prefix, informal=True)
            )
            conjugations.extend(
                self.imperative(
                    present_stem, prefix=prefix, negative=True, informal=True
                )
            )

            if informal_present_stem:
                conjugations.extend(
                    self.imperative(informal_present_stem, prefix=prefix, informal=True)
                )
                conjugations.extend(
                    self.imperative(
                        informal_present_stem,
                        prefix=prefix,
                        negative=True,
                        informal=True,
                    )
                )

        return conjugations


@lru_cache(maxsize=1)
def get_conjugated_verbs() -> dict[str, tuple[str | None, str]]:
    conjugator = Conjugator()
    conjugated_verbs: dict[str, tuple[str | None, str]] = {}

    for (
        past_stem,
        present_stem,
        informal_past_stem,
        informal_present_stem,
    ) in data.verbs:
        base_past_stem, prefix = conjugator.get_verb_prefix(past_stem)
        base_present_stem, _ = conjugator.get_verb_prefix(present_stem)

        informal_base_past_stem, _ = conjugator.get_verb_prefix(informal_past_stem)
        informal_base_present_stem, _ = conjugator.get_verb_prefix(
            informal_present_stem
        )

        conjugations = conjugator.conjugate(
            base_past_stem,
            base_present_stem,
            informal_base_past_stem,
            informal_base_present_stem,
            prefix=prefix,
        )

        for form in conjugations:
            conjugated_verbs[form] = (past_stem, present_stem)

    for form in conjugator.simple_present(past_stem=None, present_stem="هست"):
        conjugated_verbs[form] = (None, "هست")

    for form in conjugator.simple_present(past_stem=None, present_stem="نیست"):
        conjugated_verbs[form] = (None, "نیست")

    return conjugated_verbs
