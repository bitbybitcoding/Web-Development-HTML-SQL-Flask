# Capstone project: assessment brief

**Weighting:** 40% of the course · **Started:** Week 10 · **Finished and presented:** Week 11 · **Work:** individually or in pairs (pairs build a larger project; see below)

Build a **database-driven web application** with Flask and SQLite that solves a real problem for real users.

## Choose a project

Pick one of these starting points, or propose your own to your instructor (it must meet the requirements below).

| Idea | Core tables (suggestion) |
|------|--------------------------|
| **Club kit loans** (see the model in [Answers/model-capstone](Answers/model-capstone/)): *do not copy this one* | category, kit, loan |
| **School canteen ordering:** stalls, dishes, orders and order lines | stall, dish, customer_order, order_line |
| **Tuition / lesson booking:** tutors, subjects, time slots and bookings | tutor, subject, slot, booking |
| **Sports league tracker:** teams, players, matches and results with a league table | team, player, match |
| **Event sign-up and attendance** for a club or CCA | event, member, signup |
| **Study planner:** subjects, tasks, deadlines and study sessions | subject, task, session |
| **Pet adoption centre:** animals, adopters, visits and adoptions | animal, adopter, visit |
| **Your own idea** | at least two related tables |

## Requirements

### Must have (to pass)

1. **Database:** at least **two related tables** with a primary key in each and a foreign key, designed in **3NF**, with constraints (`NOT NULL`, `UNIQUE`, `CHECK`, `FOREIGN KEY`, defaults where useful) and `PRAGMA foreign_keys = ON` for every connection.
2. **CRUD:** all four operations working for at least one table, with the user interface to match.
3. **Read features:** a list page, a detail page, a **search or filter** (GET form), and a **report page** that uses `GROUP BY`, an aggregate or a join.
4. **Validation:** every form is validated **on the server**, with a clear message beside the field, and keeps what the user typed.
5. **Security habits:** `?` placeholders in **every** query; data-changing actions only with POST; unknown ids give a 404 page; no secrets in the repository.
6. **Flask structure:** a base template, a static stylesheet, `url_for` for all links, POST then redirect, flash messages.
7. **Seed data:** realistic data so that every page has something to show (at least 8 rows in the main table).
8. **Tests (Week 11):** at least **8 automated tests** with `unittest`, covering reading, creating with valid and invalid data, and one database rule.
9. **README (Week 11):** what it is, how to run it, the ER diagram, and what each page does.
10. **Git:** a repository with a clear history of at least **10 commits** with meaningful messages, made over both weeks.

### To earn the top bands

- A feature that goes beyond the course (pagination, sorting, a status workflow, a chart drawn with HTML/CSS, a second report).
- Edge cases handled well (overbooking, duplicates, deleting something that is in use) with a friendly message.
- Polished, consistent, responsive design that works on an iPad.
- Code that is easy to read: small functions, clear names, comments explaining *why*.
- Deployed online (Week 11 walkthrough).

### Pairs

Pairs must add **two extra tables** (at least four in total) and the second person's work must be visible in the Git history (use separate branches and merge). Each partner presents their part.

## How it is marked (100 marks)

| Area | Marks | What the marker looks for |
|------|-------|---------------------------|
| Planning and design | 15 | `PLAN.md`; user stories; ER diagram; normalisation argument; route map |
| Database | 15 | Correct tables, keys, constraints, 3NF, realistic seed data |
| Functionality | 25 | CRUD, search/filter, report all work; the app does what the plan says |
| Robustness and security | 15 | Validation, placeholders, POST for changes, 404s, handling of duplicates and deletes |
| Testing | 10 | Number, variety and meaning of tests; they pass |
| Code quality and Git | 10 | Readable code, structure, commit history |
| Presentation and README | 10 | A clear 3-minute demo; README quality; honest reflection |

Marks are shown as a percentage of the 40% weighting.

## Milestones

| When | What |
|------|------|
| End of Week 10 | `PLAN.md` approved, database created from `schema.sql` and `seed.sql`, the list page and the add form work, first commits pushed |
| Between sessions (about 2 hours) | CRUD complete, search and report started |
| Start of Week 11 | Feature-complete, or a list of what is not |
| Week 11 | Tests, polish, README, deployment, 3-minute presentation |

## Academic honesty

You may use the course examples, the model project's patterns and online documentation. You must understand and be able to explain every line you submit. In the presentation you will be asked to change something small live. Copying another student's project, or code you cannot explain, will earn no marks for that part.
