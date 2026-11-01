# Week 10: Capstone: plan and build

**Block 4: Capstone** · 3 hours · Platform: GitHub Codespaces · **Includes the Week 10 mini-assessment (20% of the course)**

## By the end of this session students can

- Turn an idea into **user stories**, a **minimum viable product (MVP)** and a list of stretch goals.
- Design a normalised database (ER diagram, tables, keys, constraints) for their own project, and create it from `schema.sql` and `seed.sql`.
- Plan the pages and routes of an application, with the HTTP method and SQL for each.
- Start a project from the capstone template, and build the first **vertical slice**: a page that reads from the database, and a form that writes to it, with validation.
- Use Git to save their work: commits with clear messages, a feature branch, and `push` to GitHub.

## Session plan

| Time | Activity | File |
|------|----------|------|
| 0:00–0:15 | Warm-up: the capstone brief | [capstone-brief.md](capstone-brief.md) |
| 0:15–1:00 | Demo: from idea to first slice, and Git | [demo.md](demo.md) |
| 1:00–1:10 | Break | |
| 1:10–2:30 | Build time (4 challenges) | [challenges.md](challenges.md) · starter in [capstone-template/](capstone-template/) |
| 2:30–3:00 | **Mini-assessment** (30 minutes, individual) | [mini-assessment.md](mini-assessment.md) |

**Homework / extra practice:** [extra-practice.md](extra-practice.md), including exam-style written questions covering all three blocks
**Quick reference for students:** [cheatsheet.pdf](cheatsheet.pdf)
**Instructor answers:** [Answers/](Answers/)

## Warm-up (15 min): the capstone brief

1. Hand out or share [capstone-brief.md](capstone-brief.md). Walk through the *Must have* list and the marking table, then show the finished model project running (`Answers/model-capstone`: *"this is what a good result looks like; you must not copy this idea"*).
2. In pairs, students list **three problems at school or in their CCA that a small database app could solve**. Take two from the room and ask: *Who are the users? What are the two or three "things" (tables)?*
3. Remind them of today's timetable: the **mini-assessment is the last 30 minutes**; build time therefore ends at 2:30.

## Instructor notes

- **Approve plans early.** The most valuable ten minutes this week are spent checking `PLAN.md` files at the start of the build time. Use the checklist in the [Answers](Answers/README.md). Common problems: a single table (no relationships), a project far too large, a many-to-many relationship without a junction table, and an idea that needs logins or payments. Steer these towards an MVP; **logins are out of scope** (a stretch goal at most, and only with guidance).
- **Pairs.** Allow pairs (see the brief for the extra requirements). They should share the project through GitHub; the partner opens it in their own codespace by cloning it. Use separate branches. Plan 10 minutes of help with `git pull`, merges and conflicts in Week 11.
- **Where the code lives.** Students copy [capstone-template/](capstone-template/) into `my-work/capstone/` (see its README). `my-work/` is part of this repository. For the capstone they should either commit it here (simplest) or create their own repository and push there. Decide before the session, and tell them.
- **Mini-assessment.** Individual, closed notes, 30 minutes, paper. Mark with [the guide](Answers/mini-assessment-answers.md). Because this repository is public, **treat the paper as open to students who look ahead**: change the numbers and names (for example `kit` becomes `costume`, `loan` becomes `booking`, 7 days becomes 3 days) and write the updated mark scheme; the structure and the marks stay the same. For a stricter setting, keep an instructor-only copy of `Answers/` elsewhere and delete it from the version students open.
- **Time check.** If students want more build time, run the mini-assessment at the start of Week 11 instead; the syllabus weighting is unchanged.
- **Reminder:** stop and delete old codespaces. Capstone projects are often left open overnight.
- **Do not use `Answers/model-capstone` as a project idea in the room.** It is the instructor's reference, and a model for the tests and README that students will write in Week 11.
