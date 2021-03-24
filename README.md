# bowling-exercise

Code is written and tested in Python 3.8

The API is defined in bowling.py.

One may use either the object directly, or the functional API which wraps over the object API to avoid mutation of the same object.

The API provides functions to create a scorecard, upon which the rest of the API acts; "throw", i.e. record pins being knocked by rolling the ball; get the total score so far; get the score for a given frame number (1-indexed), and to see if the scorecard is complete.

Tests are in test_bowling.py and may be run by invoking `python -m unittest` from the project root directory. (Or by running `python test_bowling.py`).

Effort was made to keep the code readable. It is not "optimized" much.
