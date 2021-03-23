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
        elif frame.is_strike:
            shots_this_frame_onwards = chain(
                *(x.shots for x in self.frames[(frame_number - 1) :])
            )
            next_two_shots = islice(shots_this_frame_onwards, 1, 3)
            return 10 + sum(next_two_shots)
        elif frame.is_spare:
            shots_this_frame_onwards = chain(
                *(x.shots for x in self.frames[(frame_number - 1) :])
            )
            next_one_shot = islice(shots_this_frame_onwards, 1, 2)
            return 10 + sum(next_one_shot)
        else:
            return sum(frame.shots)

    def throw(self, knocked: int):
        assert not self.is_complete, f"Game is already complete! Score: {self.total_score}"
        eligible_frames = list(
            dropwhile(lambda x: x.is_strike or (len(x.rolls) == 2), self.frames)
        )
        # if it is not complete and everything is either a strike or already has 2 rolls
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
        if (final_frame.is_strike or final_frame.is_spare) and len(
            final_frame_shots
        ) == 3:
            return True
        elif len(final_frame_shots) == 2:
            return True
        return False
