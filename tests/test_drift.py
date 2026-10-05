import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ladder.drift import Ladder  # noqa: E402


class DriftTest(unittest.TestCase):
    def test_win_adds_rating(self):
        l = Ladder(10_000, 1_000, 5, 0)
        l.join("p1", 100, 0)
        self.assertEqual(l.settle("m1", "p1", 20, 100)[0], 120)

    def test_no_decay_before_window(self):
        l = Ladder(10_000, 1_000, 5, 0)
        l.join("p1", 100, 0)
        self.assertEqual(l.settle("m1", "p1", 20, 5_000)[0], 120)

    def test_unknown_player_is_rejected(self):
        l = Ladder(10_000, 1_000, 5, 0)
        self.assertEqual(l.settle("m1", "ghost", 20, 0)[1], "unknown")

    def test_join_records_start(self):
        l = Ladder(10_000, 1_000, 5, 0)
        l.join("p1", 90, 7)
        self.assertEqual(l.players["p1"]["last_ms"], 7)


if __name__ == "__main__":
    unittest.main()
