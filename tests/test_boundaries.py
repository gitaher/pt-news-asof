import copy
import unittest

import test_verifier as helpers

from plugin.logic import solve
from verifier import verify_input


class BoundaryTests(unittest.TestCase):
    setUp = helpers.VerifierTests.setUp
    check = helpers.VerifierTests.check

    def reject(self, x):
        self.assertFalse(verify_input("compute", x)["valid"])

    def accept(self, x, gold):
        self.assertTrue(self.check(gold, x))
        self.assertEqual(solve(x), gold)

    def test_no_articles(self):
        self.accept(dict(self.x, articles=[]), {"selected_ids": []})

    def test_zero_lookback_inclusive_cutoff(self):
        x = copy.deepcopy(self.x)
        x["lookback_hours"] = 0
        x["articles"][0]["published_at"] = x["cutoff"]
        x["articles"][0]["available_at"] = x["cutoff"]
        self.accept(x, {"selected_ids": ["a"]})

    def test_lower_bound_minus_one_second_excluded(self):
        x = copy.deepcopy(self.x)
        x["articles"][-1]["published_at"] = "2026-01-04T11:59:59Z"
        self.accept(x, {"selected_ids": ["a"]})

    def test_duplicate_tie_id_order(self):
        x = copy.deepcopy(self.x)
        x["articles"][1]["available_at"] = x["articles"][0]["available_at"]
        x["articles"].reverse()
        self.accept(x, self.gold)

    def test_unrelated_early_duplicate_does_not_hide_relevant(self):
        x = copy.deepcopy(self.x)
        x["articles"][0]["symbols"] = ["MSFT"]
        self.accept(x, {"selected_ids": ["e", "b"]})

    def test_late_arrival_is_excluded(self):
        x = copy.deepcopy(self.x)
        x["articles"][0]["available_at"] = "2026-01-05T12:00:01Z"
        self.accept(x, {"selected_ids": ["e", "b"]})

    def test_input_permutation_invariance(self):
        self.accept(dict(self.x, articles=list(reversed(self.x["articles"]))), self.gold)

    def test_duplicate_id_is_invalid(self):
        x = copy.deepcopy(self.x)
        x["articles"][1]["id"] = "a"
        self.reject(x)

    def test_bad_times(self):
        for t in ["2026-01-05T12:00:00+00:00", "2026-02-29T12:00:00Z", "2026-01-05T24:00:00Z"]:
            self.reject(dict(self.x, cutoff=t))

    def test_availability_before_publication(self):
        x = copy.deepcopy(self.x)
        x["articles"][0]["available_at"] = "2026-01-04T00:00:00Z"
        self.reject(x)

    def test_empty_query_or_negative_window(self):
        self.reject(dict(self.x, symbols=[]))
        self.reject(dict(self.x, lookback_hours=-1))
