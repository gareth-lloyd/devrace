from unittest import TestCase

from devrace.contest import Player, Achievement
from devrace.scoreboard import (pairs, _convert_for_display,
        _convert_to_bytes, _normalize_scores, SCORE_DIVISOR)
from devrace import scoreboard

class PairsTests(TestCase):
    def test_empty(self):
        self.assertRaises(StopIteration, pairs([]).next)

    def test_one_member(self):
        pairs_gen = pairs([1])
        self.assertEquals((1, 0), pairs_gen.next())
        self.assertRaises(StopIteration, pairs_gen.next)

    def test_two_members(self):
        pairs_gen = pairs([1, 2])
        self.assertEquals((1, 2), pairs_gen.next())
        self.assertRaises(StopIteration, pairs_gen.next)

    def test_three_members(self):
        pairs_gen = pairs([1, 2, 3])
        self.assertEquals((1, 2), pairs_gen.next())
        self.assertEquals((3, 0), pairs_gen.next())
        self.assertRaises(StopIteration, pairs_gen.next)

class DisplayFunctionsTests(TestCase):
    def setUp(self):
        self.players = [
            Player('p1', {}),
            Player('p2', {}),
        ]
        self.players[0].achievements.append(Achievement(3 * SCORE_DIVISOR))
        self.players[1].achievements.append(Achievement(2 * SCORE_DIVISOR))

    def test_convert_for_display_no_scores(self):
        self.players[0].achievements = []
        self.players[1].achievements = []
        self.assertEquals([], _convert_for_display(self.players))

    def test_convert_for_display(self):
        expected = [
            (1,0),
            (1,1),
            (1,1),
        ]
        self.assertEquals(expected, _convert_for_display(self.players))

    def test_normalize_scores_padding(self):
        scoreboard.MAX_SCORE = 5
        input = [
            (1,0),
            (1,1),
            (1,1),
        ]
        expected = [
            (0,0), # should be padded
            (0,0),
            (1,0),
            (1,1),
            (1,1),
        ]
        self.assertEquals(expected, _normalize_scores(input, self.players))

    def test_normalize_scores_truncating(self):
        scoreboard.MAX_SCORE = 5
        input = [
            (1,0),
            (1,0),
            (1,0),
            (1,0),
            (1,0),
            (1,1),
            (1,1),
        ]
        expected = [
            (1,0),
            (1,0),
            (1,0),
            (1,1),
            (1,1),
        ]
        self.assertEquals(expected, _normalize_scores(input, self.players))

    def test_convert_to_bytes(self):
        input = [
            (1,0),
            (1,0),
            (1,0),
            (1,1),
            (1,1),
        ]
        expected = [
            chr(0B01110000),
            chr(0B01110000),
            chr(0B01110000),
            chr(0B01110111),
            chr(0B01110111),
        ]
        self.assertEquals(expected, _convert_to_bytes(input))

    def test_convert_to_bytes_multiple_columns(self):
        input = [
            (1, 0, 0, 1),
            (1, 0, 0, 1),
            (1, 1, 0, 1),
            (1, 1, 0, 1),
            (1, 1, 0, 1),
        ]
        expected = [
            chr(0B01110000) + chr(0B00000111),
            chr(0B01110000) + chr(0B00000111),
            chr(0B01110111) + chr(0B00000111),
            chr(0B01110111) + chr(0B00000111),
            chr(0B01110111) + chr(0B00000111),
        ]
        self.assertEquals(expected, _convert_to_bytes(input))
