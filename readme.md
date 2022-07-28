# number_jokes is a module that generates number jokes
Number joke: a sequence of numbers that structurally mimics natural language jokes

# Module Structure  
number_jokes contains multiple diferent classes each of which generates a diferent type of number joke.

# Number Joke Classes

## 1. GardenPathPolynomials

FUNCTIONALITY
- generate a fully random joke
- generate a punchline given a setup

JOKE PART FUNCTIONALITY
- generate a function given starting_points
    - starting points can be randomly generated given a length
    - or entered as a parameter
- generate starting_points given a function
    - function can be randomly generated given a highest term
    - or entered as a parameter
- generate ending_points given joke_part length and starting_points/function

setup: [`starting_points`,`ending_points`]
punchline: [`setup`][`starting_points`,`ending_points`]

setup_coefs:
punchline_coefs:

setup_fn_str:
punchline_fn_str:

setup_fn:
punchline_fn:

starting_points:
    - can be entered as a parameter
    - else:
        - generated based on setup_function

ending_points:
    - generated using: 
        -`starting_points`
        -`joke_part_function`
        -`joke_part_length`

