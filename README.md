# Sudoku Solver & Game #

_*This repository contains sudoku solver, sudoku board creator and sudoku game (based in tkinter).*_

### Documentation ###
Simple Sudoku Solver [simple_sudoku_solver](https://rickfernandes.github.io/sudoku/docs/simple_sudoku_solver.html)

Sudoku Board Generator [sudoku_generator](https://rickfernandes.github.io/sudoku/docs/sudoku_generator.html)

Terminal Sudoku Solver [terminal_sudoku_solver](https://rickfernandes.github.io/sudoku/docs/terminal_sudoku_solver.html)

Sudoku Starter for `tk_sudoku_game` [sudoku_start](https://rickfernandes.github.io/sudoku/docs/sudoku_start.html)

Tkinter Sudoku Game[tk_sudoku_game](https://rickfernandes.github.io/sudoku/docs/tk_sudoku_game.html)

---

## Repository explanation ##
This repository has 3 code examples that use memoization. I advise to check them in the order below:

### Fibonacci ###
This code shows the time difference between 3 approaches for a recursive function:
1. Without memoization
2. With memoization using a dict
3. With memoization using a well establish Python module

### Bad Use Case ###
This code shows how an improper use of memoization might generate an undesired behaviour.
The main takeaway here is that you should **never** use memoization if a function potentially has different results for the same input.

### Exchange Rate ###
This code shows how memoization improves execution time when using a costly function (like a GET request). Another side advantage here is that if the API server is down
or times out, you will still have the [lru_cache](https://www.geeksforgeeks.org/python-functools-lru_cache/) from previous calls.

---
### Notes: ###
*All codes use Python3*
Modules used:

|Module|Attribute|
|:-----|:-----|
|functools|lru_cache|
|random|randint|
|time|perf_counter|
|requests|get|
|json|loads|
|datetime|*several*|