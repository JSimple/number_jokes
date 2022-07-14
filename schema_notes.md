REQUIREMENTS

MVP:
- generate num jokes
- store them
- ratings for jokes

V2:
- user auth
- user specific ratings
- user favorated jokes
- jokes owned by users

V3:
- multiple joke types
- see who favorited your jokes
- post to social media


----

MODELS

Joke:
- Sequence
- Type

single model:
pros - easier to query

seperate models:
pros - you're not doing any joins so faster, 
cons - but doing more queries

easier in a databse to get less specific than more specific