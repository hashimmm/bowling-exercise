import bowling
import unittest


class BowlingTestCase(unittest.TestCase):
    def test_create_scorecard(self):
        scorecard = bowling.create_scorecard()
        assert isinstance(scorecard, bowling.Scorecard)
    
    def test_frame_filling_strikes_spares(self):
        scorecard = bowling.create_scorecard()
        scorecard.throw(1)
        self.assertEqual(scorecard.frames[0], bowling.Frame(shots=[1]))
        scorecard.throw(2)
        self.assertEqual(scorecard.frames[0], bowling.Frame(shots=[1, 2]))
        scorecard.throw(3)
        self.assertEqual(scorecard.frames[0], bowling.Frame(shots=[1, 2]))
        self.assertEqual(scorecard.frames[1], bowling.Frame(shots=[3]))
        scorecard.throw(7)
        scorecard.throw(10)
        scorecard.throw(5)
        self.assertEqual(scorecard.frames[1], bowling.Frame(shots=[3, 7]))
        self.assertTrue(scorecard.frames[1].is_spare)
        self.assertFalse(scorecard.frames[1].is_strike)
        self.assertEqual(scorecard.frames[2], bowling.Frame(shots=[10]))
        self.assertTrue(scorecard.frames[2].is_strike)
        self.assertFalse(scorecard.frames[2].is_spare)
        self.assertEqual(scorecard.frames[3], bowling.Frame(shots=[5]))
        self.assertFalse(scorecard.frames[3].is_strike)
        self.assertFalse(scorecard.frames[3].is_spare)
    
    def test_final_frame(self):
        scorecard = bowling.create_scorecard()
        shots = [10, 7, 3, 7, 2, 9, 1, 10, 10, 10, 2, 3, 6, 4, 7, 2]
        for score in shots:
            scorecard.throw(score)
        self.assertTrue(scorecard.is_complete)

    def test_final_frame_spare(self):
        scorecard = bowling.create_scorecard()
        shots = [10, 7, 3, 7, 2, 9, 1, 10, 10, 10, 2, 3, 6, 4, 7, 3]
        for score in shots:
            scorecard.throw(score)
        self.assertFalse(scorecard.is_complete)
        scorecard.throw(3)
        self.assertTrue(scorecard.is_complete)

    def test_final_frame_spare(self):
        scorecard = bowling.create_scorecard()
        shots = [10, 7, 3, 7, 2, 9, 1, 10, 10, 10, 2, 3, 6, 4, 10]
        for score in shots:
            scorecard.throw(score)
        self.assertFalse(scorecard.is_complete)
        scorecard.throw(10)
        self.assertFalse(scorecard.is_complete)
        scorecard.throw(10)
        self.assertTrue(scorecard.is_complete)

    def test_game_functional_api(self):
        scorecard = bowling.create_scorecard()
        shots = [10, 7, 3, 7, 2, 9, 1, 10, 10, 10, 2, 3, 6, 4, 7, 3, 3]
        for score in shots:
            scorecard = bowling.throw(scorecard, score)
        self.assertTrue(scorecard.is_complete)
        self.assertRaises(AssertionError, lambda: bowling.throw(scorecard, 5))
        for idx, test_score in enumerate([20, 17, 9, 20, 30, 22, 15, 5, 17, 13]):
            frame_number = idx + 1
            self.assertEqual(bowling.score_for_frame(scorecard, frame_number), test_score)
        self.assertEqual(bowling.total_score(scorecard), 168)


if __name__ == "__main__":
    unittest.main()
