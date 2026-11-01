# Week 11: Test, polish and present

**Block 4: Capstone** · 3 hours · Platform: GitHub Codespaces · The last session: capstone presentations

## By the end of this session students can

- Write automated tests with `unittest` and Flask's test client, including boundary, invalid-input and database-rule tests.
- Review their own project against a checklist and fix usability, accessibility and robustness problems.
- Write a README that lets a stranger run and understand the project.
- Explain (and, as a stretch goal, carry out) deploying a Flask app, and say what changes on a real server.
- Present and defend their project in three minutes, and answer questions about how it works.

## Session plan

*This week's timetable differs from the others: the second half is for presentations.*

| Time | Activity | File |
|------|----------|------|
| 0:00–0:15 | Warm-up: feature freeze check (below) | this page |
| 0:15–1:00 | Demo: testing, polish, README, deployment, presenting | [demo.md](demo.md) · code in [demo/](demo/) |
| 1:00–1:10 | Break | |
| 1:10–2:00 | Build time: tests, polish and README (4 challenges) | [challenges.md](challenges.md) · templates in [challenges/](challenges/) |
| 2:00–3:00 | **Presentations** (3 min + 2 min of questions each) | [challenges/presentation-planner.md](challenges/presentation-planner.md) |

**Homework / after the course:** [extra-practice.md](extra-practice.md)
**Quick reference for students:** [cheatsheet.pdf](cheatsheet.pdf)
**Deployment walkthrough:** [deploy-pythonanywhere.md](deploy-pythonanywhere.md)
**Instructor answers and marking sheet:** [Answers/](Answers/)

## Warm-up (15 min): feature freeze

1. Each student answers on paper: *Which of the "must have" items from the brief are done? Which are not?* Collect the list. This is what they will do in the next 100 minutes.
2. **Feature freeze:** no new features today. Today is for tests, fixes, polish and the README. A feature that is half finished is removed or hidden rather than left broken.
3. Show the **presentation order** (draw names) and the marking approach: the marking sheet is in [Answers/capstone-marking-sheet.md](Answers/capstone-marking-sheet.md) so students know what is looked for.

## Instructor notes

- **Presentations: running order.** With 12 students, 5 minutes each (3 + 2) fills 60 minutes. Larger classes: run two rooms or screens with a co-marker, or let half the class present in Week 11 and half in a short extra session. Set a visible timer; stop at 3:00 politely. Ask each student **one** question that needs them to look at the code: it proves understanding.
- **The live change.** Ask for a small change in the code ("make this field required", "change the limit from 28 to 14 days"). A student who wrote the code finds it in seconds; this is the best check of authorship.
- **Marking while listening.** Use the [marking sheet](Answers/capstone-marking-sheet.md) for the presentation and (separately, after the session) for the repository: plan, database, tests, code, Git history, README. Students are marked on the quality of their work against the brief, not against the model project.
- **Tests that pass vs tests that mean something.** Look for tests that would **fail** if the feature broke: a test that only checks `status_code == 200` on a page proves little. Ask: *"What bug would this test catch?"*
- **Deployment is optional.** Treat it as a bonus. If the free-plan or account rules prevent it, show a demo from your own account. Read the instructor note at the top of [deploy-pythonanywhere.md](deploy-pythonanywhere.md) and try the whole walkthrough yourself first.
- **Security reminder.** Remind students not to put real personal data in their project, nor passwords or secret keys in the repository. If they deployed, discuss what is public.
- **Finishing the course.** Collect the course feedback; give back the checkpoint quiz and mini-assessment marks; remind students to stop and delete their codespaces (their work stays safe in GitHub if pushed). Share the "where next" ideas in [extra-practice.md](extra-practice.md).
- **Pairs.** Each person presents the part they built, and the Git history is checked to see both contributed.
