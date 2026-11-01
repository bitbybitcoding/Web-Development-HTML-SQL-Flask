# Project name

One sentence: what it is and who it is for.

## The problem

Two or three sentences. Who has the problem, and how do they cope now?

## Features

| Page | URL | What it does |
|------|-----|--------------|
|      |     |              |

## How to run it

```bash
pip install -r requirements.txt
flask --app app init-db       # creates the database from schema.sql and seed.sql (deletes existing data)
flask --app app run --debug
```

Run the tests: `python3 -m unittest discover -s tests -v`

## Database design

Insert your ER diagram (a Mermaid block or an image), then a table for each table of the database:

| Table | Purpose | Key columns |
|-------|---------|-------------|
|       |         |             |

One short paragraph on **normalisation**: show that the tables are in 3NF (nothing repeated, nothing calculable stored) and the rules the database enforces (`NOT NULL`, `UNIQUE`, `CHECK`, `FOREIGN KEY`).

## Design decisions

Two or three bullets about choices you made and **why** (what you considered and rejected).

## Testing

How many tests, what they cover, and how to run them. Mention one bug the tests caught, if any did.

## Limitations and next steps

Honest list: what does not work yet, what you would add with more time.

## What I learned

Three or four sentences, in your own words and about **your** experience.

## Credits

Anything you used: course examples, documentation, a library, a person who helped you test.
