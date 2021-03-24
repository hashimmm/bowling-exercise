import bowling
import unittest


class BowlingTestCase(unittest.TestCase):
    def test_create_scorecard(self):
        scorecard = bowling.create_scorecard()
        assert isinstance(scorecard, bowling.Scorecard)

    def test_game(self):
        scorecard = bowling.create_scorecard()
        shots = [10, 7, 3, 7, 2, 9, 1, 10, 10, 10, 2, 3, 6, 4, 7, 3, 3]
        for score in shots:
            scorecard = bowling.throw(scorecard, score)
        assert scorecard.is_complete
        for idx, test_score in enumerate([20, 17, 9, 20, 30, 22, 15, 5, 17, 13]):
            frame_number = idx + 1
            assert bowling.score_for_frame(scorecard, frame_number) == test_score
        assert bowling.total_score(scorecard) == 168


if __name__ == "__main__":
    unittest.main()
