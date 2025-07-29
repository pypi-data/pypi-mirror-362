# uvlpy
A light package for constraint solving by levereging uv's dependency resolver

## Example
Example of some basic code to show the features would be:
```py
from uvlpy.uvlpy import System

sys = System()
a, b, c = sys.make_vars([0, 1], [2, 3, 4], list(range(0,9)))
a.val_constr(1, b == 2)
c.constr(b > 1)
sys.constr(a > 0, c < 9, b.to_constr())
print(sys.execute(a, b, c))
```
Where we:
- Create 3 variables with given possible values
- Constrain `a = 1` to require `b = 2`
- Constrain all values of `c` to require `b > 1`
- Constrain the result to require a positive `a`, `c < 9`, and to include `b`
- After execution the output is e.g. [1, 2, 8], a and b can only be 1 and 2, but c can be any of its possible values

You can see the `sudoku_example.py` for a sudoku solver, 
which uses lists directly instead of destructuring them into variables like here.

## Install
You can build it locally with `uv build` and use the wheel as you see fit.

Note that `uv` being installed and visible on PATH is required for this library to function.

## Why
Can be done. 

`uvlpy` uses `uv`'s solver, which should be reliable. The performance is not great, but sufficient.

However, note that the library creates a lot temporary files and packages to utilize `uv`, and as such, should be used with care and within reason.
