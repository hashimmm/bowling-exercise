import bowling
import unittest
from hypothesis import example, given, strategies as st
from itertools import chain

strike_st = lambda: st.just([10])
spare_st = lambda: st.one_of(
    list(map(lambda x: st.just(list(x)), zip(range(10), range(10, 0, -1))))
)

@st.composite
def normal_st(draw):
    first_shot = draw(st.integers(0, 9))
    second_shot = draw(st.integers(0, 9 - first_shot))
    return [first_shot, second_shot]

frame_st = lambda: st.one_of(strike_st(), spare_st(), normal_st())

tenth_frame_st = lambda: st.one_of(
    normal_st(),
    st.builds(lambda x, y: x + [y], spare_st(), st.integers(0, 10)),
    st.builds(lambda x, y: [10, x, y], st.integers(0, 10), st.integers(0, 10)),
)

def combine_shots(first_9, tenth):
    return list(chain.from_iterable([*first_9, tenth]))

all_shots_st = lambda: st.builds(combine_shots, st.lists(frame_st(), min_size=9, max_size=9), tenth_frame_st())


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
            self.assertEqual(
                bowling.score_for_frame(scorecard, frame_number), test_score
            )
        self.assertEqual(bowling.total_score(scorecard), 168)

    # THIS TEST CAN EFFECTIVELY REPLACE ALL THE OTHERS EXCEPT THE ONES THAT CHECK TOTAL SCORE
    @given(all_shots_st())
    def test_properties_shots(self, shots):
        scorecard = bowling.create_scorecard()
        for score in shots:
            scorecard = bowling.throw(scorecard, score)
        self.assertTrue(scorecard.is_complete)
        self.assertEqual(len(scorecard.frames), 10)
        for frame in scorecard.frames[:-1]:
            assert frame.shots
            if frame.shots[0] == 10:
                self.assertEqual(len(frame.shots), 1)
            else:
                self.assertEqual(len(frame.shots), 2)
                assert sum(frame.shots) <= 10
        last_frame = scorecard.frames[-1]
        assert len(last_frame.shots) >= 2
        for shot in last_frame.shots:
            assert shot <= 10
        if last_frame.shots[0] == 10:
            self.assertEqual(len(last_frame.shots), 3)
        elif (last_frame.shots[0] + last_frame.shots[1]) == 10:
            self.assertEqual(len(last_frame.shots), 3)
        else:
            self.assertEqual(len(last_frame.shots), 2)
        # TODO: SOME TEST FOR TOTAL SCORE



if __name__ == "__main__":
    unittest.main()
