from dataclasses import dataclass, field
from itertools import chain, dropwhile, islice
from typing import List


@dataclass
class Frame:
    shots: List[int] = field(default_factory=list)

    @property
    def is_strike(self) -> bool:
        return self.shots and (self.shots[0] == 10)

    @property
    def is_spare(self) -> bool:
        return (
            (len(self.shots) >= 2)
            and (self.shots[0] != 10)
            and (sum(self.shots[:2]) == 10)
        )


@dataclass
class Scorecard:
    frames: "List[Frame]" = field(default_factory=lambda: [Frame() for _ in range(10)])

    def score_for_frame(self, frame_number: int) -> int:
        frame = self.frames[frame_number - 1]
        if not frame.shots:
            return 0
        elif frame.is_strike or frame.is_spare:
            # Score for a spare or strike is always the sum of three shots including
            # the ones for the spare or strike itself.
            shots_this_frame_onwards = chain(
                *(x.shots for x in self.frames[(frame_number - 1) :])
            )
            three_shots = islice(shots_this_frame_onwards, None, 3)
            return sum(three_shots)
        else:
            return sum(frame.shots)

    def throw(self, knocked: int):
        assert not self.is_complete, f"Game is already complete! Score: {self.total_score}"
        # This throw/shot will be scored in the current frame.
        # The current frame is the first one that isn't either a strike or already has 2 shots.
        eligible_frames = list(
            dropwhile(lambda x: x.is_strike or (len(x.shots) == 2), self.frames)
        )
        # if it is not complete and everything is either a strike or already has 2 shots
        # then current frame must be last frame.
        current_frame = eligible_frames[0] if eligible_frames else self.frames[-1]
        current_frame.shots.append(knocked)

    @property
    def total_score(self):
        return sum(self.score_for_frame(i) for i in range(1, 11))

    @property
    def is_complete(self) -> bool:
        final_frame = self.frames[-1]
        final_frame_shots = final_frame.shots
        if not final_frame_shots:
            return False
        if (final_frame.is_strike or final_frame.is_spare):
            if len(final_frame_shots) == 3:
                return True
            return False
        elif len(final_frame_shots) == 2:
            return True
        return False


## Functional API

def create_scorecard() -> Scorecard:
    return Scorecard()


def throw(scorecard: Scorecard, knocked: int) -> Scorecard:
    copied = Scorecard(frames=[Frame(x.shots.copy()) for x in scorecard.frames])
    copied.throw(knocked)
    return copied


def total_score(scorecard: Scorecard) -> int:
    return scorecard.total_score


def score_for_frame(scorecard: Scorecard, frame_number: int) -> int:
    return scorecard.score_for_frame(frame_number)


def is_complete(scorecard: Scorecard) -> bool:
    return scorecard.is_complete
