from pegpy.frame import FrameDisplayPeggy
from pegpy.pbm import pbm_lines
import settings
from itertools import izip_longest
from time import sleep

COLUMN_SEGMENT = 0B0111
MAX_SCORE = 16
SCORE_DIVISOR = 4

def pairs(indexable, emptyvalue=0):
    i = 0
    while True:
        try:
            yield indexable[i], indexable[i + 1]
            i += 2
        except IndexError:
            try:
                yield indexable[i], emptyvalue
                break
            except IndexError:
                break

def _convert_to_bytes(score_rows):
    """Convert the display representation of the scores into bitmap
    array for presentation on the Peggy.
    """
    byte_rows = []
    for score_row in score_rows:
        bytes = ''
        for left_column, right_column in pairs(score_row):
            cols_byte = 0
            if left_column:
                cols_byte |= COLUMN_SEGMENT << 4
            if right_column:
                cols_byte |= COLUMN_SEGMENT
            bytes += chr(cols_byte)
        byte_rows.append(bytes)
    return byte_rows

def _normalize_scores(scores, players):
    """Pad or truncate scores to fit to the display medium.
    """
    highest_score = len(scores)
    if highest_score < MAX_SCORE:
        difference = MAX_SCORE - highest_score
        empty = tuple([0 for _ in range(len(players))])
        scores = [empty for _ in range(difference)] + scores
    elif highest_score > MAX_SCORE:
        scores = scores[-MAX_SCORE:]
    return scores

def _convert_for_display(players):
    """Create a list of ones to the length of the score, then
    combine lists to make a crude 2d representation.
    """
    scores = []
    for player in players:
        scores.append([1 for _ in range(player.current_score / SCORE_DIVISOR)])

    translated_scores = list(izip_longest(*scores, fillvalue=0))
    return list(reversed(translated_scores))


class PeggyScoreboard(object):
    def __init__(self):
        self.peggy = FrameDisplayPeggy(settings.PEGGY_DEVICE,
                                       settings.PEGGY_BAUD)
        self.base_image = pbm_lines(settings.BASE_SCOREBOARD_IMAGE)

    def update_scores(self, contest):
        scores = _convert_for_display(contest.players)
        scores = _normalize_scores(scores, contest.players)
        display_bytes = _convert_to_bytes(scores)
        self.peggy.fresh_frame(self.base_image)
        sleep(.1)
        self.peggy.additive_frame(display_bytes)

class PrintingScoreboard(object):
    def update_scores(self, contest):
        scores = _convert_for_display(contest.players)
        scores = _normalize_scores(scores, contest.players)

        for score_row in scores:
            output = ''
            for column in score_row:
                if column:
                    output += '  ####  '
                else:
                    output += '        '
            print output
        name_row = [player.name.center(8) for player in contest.players]
        print ''.join(name_row)
