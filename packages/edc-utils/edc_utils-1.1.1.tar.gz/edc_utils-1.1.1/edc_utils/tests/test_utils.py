from datetime import date, datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

import time_machine
from django.test import TestCase

from edc_utils import (
    AgeValueError,
    age,
    formatted_age,
    formatted_datetime,
    get_age_in_days,
    get_datetime_from_env,
    get_dob,
    get_safe_random_string,
    truncate_string,
)
from edc_utils.round_up import round_half_away_from_zero


class TestUtils(TestCase):
    def test_get_safe_random_string(self):
        """With default parameters"""
        _safe_string = get_safe_random_string()
        allowed_chars = "ABCDEFGHKMNPRTUVWXYZ2346789"
        for character in _safe_string:
            if character not in allowed_chars:
                self.fail("Unexpected char")

    def test_formatted_age(self):
        datetime(2016, 12, 12).astimezone(ZoneInfo("UTC"))
        self.assertEqual(
            formatted_age(None, datetime(2016, 12, 12).astimezone(ZoneInfo("UTC"))), "?"
        )

        self.assertEqual(
            formatted_age(
                date(1990, 12, 12), datetime(2016, 12, 12).astimezone(ZoneInfo("UTC"))
            ),
            "26y",
        )
        self.assertEqual(
            formatted_age(
                date(2016, 9, 9), datetime(2016, 12, 12).astimezone(ZoneInfo("UTC"))
            ),
            "3m",
        )
        self.assertEqual(
            formatted_age(
                date(2016, 10, 28), datetime(2016, 12, 12).astimezone(ZoneInfo("UTC"))
            ),
            "1m14d",
        )
        self.assertEqual(
            formatted_age(
                date(2016, 12, 6), datetime(2016, 12, 12).astimezone(ZoneInfo("UTC"))
            ),
            "6d",
        )
        self.assertEqual(
            formatted_age(
                date(2015, 12, 12), datetime(2016, 12, 12).astimezone(ZoneInfo("UTC"))
            ),
            "12m",
        )

        self.assertRaises(
            AgeValueError,
            formatted_age,
            date(2016, 12, 12),
            datetime(2015, 12, 12).astimezone(ZoneInfo("UTC")),
        )

    @time_machine.travel(datetime(2016, 10, 28, 10, 00, tzinfo=ZoneInfo("UTC")))
    def test_age_in_days(self):
        born = date(2016, 10, 20)
        reference_date = datetime(2016, 10, 28, 10).astimezone(ZoneInfo("UTC"))
        self.assertEqual(get_age_in_days(reference_date, born), 8)

    @time_machine.travel(datetime(2016, 10, 28, 10, 00, tzinfo=ZoneInfo("UTC")))
    def test_age(self):
        born = date(1990, 5, 1)
        reference_dt = datetime(2000, 5, 1).astimezone(ZoneInfo("UTC"))
        self.assertEqual(age(born, reference_dt).years, 10)

        self.assertEqual(get_dob(age_in_years=10, now=reference_dt), born)
        self.assertEqual(get_dob(age_in_years=10, now=reference_dt.date()), born)

    def test_age_without_tz(self):
        born = datetime(1990, 5, 1).astimezone(ZoneInfo("UTC"))
        reference_dt = datetime(2000, 5, 1)
        self.assertEqual(age(born, reference_dt).years, 10)

    def test_age_born_date(self):
        born = date(1990, 5, 1)
        reference_dt = datetime(2000, 5, 1, tzinfo=ZoneInfo("UTC"))
        self.assertEqual(age(born, reference_dt).years, 10)

    def test_age_reference_as_date(self):
        born = datetime(1990, 5, 1).astimezone(ZoneInfo("UTC")).date()
        reference_dt = date(2000, 5, 1)
        self.assertEqual(age(born, reference_dt).years, 10)

    def test_age_zero1(self):
        """Assert born precedes reference considering timezones."""
        born = datetime(1990, 5, 1, 0, 0, tzinfo=ZoneInfo("Africa/Gaborone"))
        reference_dt = datetime(1990, 5, 1, 0, 0, tzinfo=ZoneInfo("UTC"))
        self.assertEqual(age(born, reference_dt).years, 0)

    def test_age_zero2(self):
        """Assert born == reference considering timezones."""
        born = datetime(1990, 5, 1, 2, 0, tzinfo=ZoneInfo("Africa/Gaborone"))
        reference_dt = datetime(1990, 5, 1, 0, 0, tzinfo=ZoneInfo("UTC"))
        self.assertEqual(age(born, reference_dt).hours, 0)

    def test_age_zero3(self):
        """Assert born after reference date considering timezones."""
        born = datetime(1990, 5, 2, 5, 0, tzinfo=ZoneInfo("Africa/Gaborone"))
        reference_dt = datetime(1990, 5, 2, 2, 0, tzinfo=ZoneInfo("UTC"))
        self.assertRaises(AgeValueError, age, born, reference_dt)

    def test_age_zero4(self):
        """Assert born 2hrs before reference date considering timezones."""
        born = datetime(1990, 5, 2, 0, 0, tzinfo=ZoneInfo("Africa/Gaborone"))
        reference_dt = datetime(1990, 5, 2, 2, 0, tzinfo=ZoneInfo("Africa/Gaborone"))
        self.assertEqual(age(born, reference_dt).hours, 2)

    def test_age_zero5(self):
        """Assert born 8hrs before reference date considering timezones."""
        born = datetime(1990, 5, 2, 0, 0, tzinfo=ZoneInfo("Africa/Gaborone"))
        reference_dt = datetime(1990, 5, 2, 2, 0, tzinfo=ZoneInfo("America/New_York"))
        dst = reference_dt.dst()
        seconds = dst.days * 24 * 60 * 60 + dst.seconds
        dst_hours, _ = divmod(seconds, 3600)
        self.assertEqual(age(born, reference_dt).hours, 7 + 2 - dst_hours)

    def test_formatted_datetime(self):
        born = datetime(1990, 5, 2, 0, 0, tzinfo=ZoneInfo("Africa/Gaborone"))
        self.assertTrue(formatted_datetime(born))

    def get_datetime_from_env(self):
        dt = datetime(1990, 5, 2, 0, 0, tzinfo=ZoneInfo("Africa/Gaborone"))
        self.assertEqual(dt, get_datetime_from_env(1990, 5, 2, 0, 0, 0, "Africa/Gaborone"))

    def test_round_up(self):
        self.assertEqual(round_half_away_from_zero(1.5, 0), 2)
        self.assertEqual(round_half_away_from_zero(1.55, 1), 1.6)
        self.assertEqual(round_half_away_from_zero(1.54, 1), 1.5)
        self.assertEqual(round_half_away_from_zero(1.555, 2), 1.56)
        self.assertEqual(round_half_away_from_zero(1.555, 2), 1.56)

        self.assertEqual(round_half_away_from_zero(-1.5, 0), -2)
        self.assertEqual(round_half_away_from_zero(-1.55, 1), -1.6)
        self.assertEqual(round_half_away_from_zero(-1.54, 1), -1.5)
        self.assertEqual(round_half_away_from_zero(-1.555, 2), -1.56)
        self.assertEqual(round_half_away_from_zero(-1.5554, 3), -1.555)

        self.assertEqual(round_half_away_from_zero(Decimal("1.5"), 0), Decimal("2"))
        self.assertEqual(round_half_away_from_zero(Decimal("1.55"), 1), Decimal("1.6"))
        self.assertEqual(round_half_away_from_zero(Decimal("1.54"), 1), Decimal("1.5"))
        self.assertEqual(round_half_away_from_zero(Decimal("1.555"), 2), Decimal("1.56"))
        self.assertEqual(round_half_away_from_zero(Decimal("1.5554"), 3), Decimal("1.555"))

    def test_truncate_string_with_len_eq_max_length_returns_orig_string(self):
        orig_string = "String of len 16"
        self.assertEqual(
            truncate_string(string=orig_string, max_length=len(orig_string)),
            orig_string,
        )

        self.assertEqual(
            truncate_string(string="a", max_length=1),
            "a",
        )
        self.assertEqual(
            truncate_string(string="ab", max_length=2),
            "ab",
        )
        self.assertEqual(
            truncate_string(string="abc", max_length=3),
            "abc",
        )
        self.assertEqual(
            truncate_string(string="ab c", max_length=4),
            "ab c",
        )

    def test_truncate_string_with_len_lt_max_length_returns_orig_string(self):
        orig_string = "String of len 16"
        for max_length in [17, 20, 100]:
            with self.subTest(max_length=max_length):
                self.assertEqual(
                    truncate_string(string=orig_string, max_length=max_length),
                    orig_string,
                )

    def test_truncate_empty_string_returns_empty_string(self):
        empty_string = ""
        for max_length in [1, 10, 100]:
            with self.subTest(max_length=max_length):
                self.assertEqual(
                    truncate_string(string=empty_string, max_length=max_length),
                    empty_string,
                )

    def test_truncate_string_len_1_max_len_1_returns_orig_string(self):
        self.assertEqual(
            truncate_string(string="a", max_length=1),
            "a",
        )

    def test_truncate_string_max_len_lt_1_raises_value_error(self):
        for string in ["", "a", "a long string"]:
            for max_length in [0, -1, -10]:
                with self.subTest(string=string, max_length=max_length):
                    with self.assertRaises(ValueError):
                        truncate_string(string=string, max_length=max_length),

    def test_truncate_string_gt_max_len_as_expected(self):
        orig_string = "String of len 16"
        self.assertEqual(
            truncate_string(string=orig_string, max_length=15),
            "String of len…",
        )
        self.assertEqual(
            truncate_string(string=orig_string, max_length=14),
            "String of len…",
        )
        self.assertEqual(
            truncate_string(string=orig_string, max_length=13),
            "String of le…",
        )
        self.assertEqual(
            truncate_string(string=orig_string, max_length=12),
            "String of l…",
        )
        self.assertEqual(
            truncate_string(string=orig_string, max_length=11),
            "String of…",
        )
        self.assertEqual(
            truncate_string(string=orig_string, max_length=10),
            "String of…",
        )
        self.assertEqual(
            truncate_string(string=orig_string, max_length=7),
            "String…",
        )
        self.assertEqual(
            truncate_string(string=orig_string, max_length=6),
            "Strin…",
        )
        self.assertEqual(
            truncate_string(string=orig_string, max_length=2),
            "S…",
        )
        self.assertEqual(
            truncate_string(string=orig_string, max_length=1),
            "…",
        )
