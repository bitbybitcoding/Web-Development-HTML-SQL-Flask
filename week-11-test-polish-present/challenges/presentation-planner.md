# Presentation planner (3 minutes + 2 minutes of questions)

Fill in the right-hand column in note form (not full sentences). Practise **aloud with a timer**.

| Part | Time | Plan |
|------|------|------|
| **1. The problem.** Who has it? Why does it matter? One sentence on how your app helps. | 30 s | |
| **2. Live demo.** Follow **one user story** from beginning to end. Include an error on purpose (bad data) and show the message. | 90 s | Story I will show: <br> Steps: <br> The error I will type: |
| **3. Under the hood.** Show: the ER diagram; one SQL query and what it does; one test. | 40 s | Query I will show: <br> Test I will show: |
| **4. Reflection.** The hardest bug you met, and what you would do next. | 20 s | |

## Before you present

- [ ] Server running, database reset to the seed data (`flask --app app init-db`)
- [ ] Tabs open: the page you start on, the ER diagram, the SQL file, the test file
- [ ] Zoom the browser so the back of the room can read it
- [ ] Notifications off; one backup plan if the app will not start (screenshots)

## Questions you might be asked

- Show me where the program stops someone entering a bad quantity. (Be ready to find it quickly.)
- What would happen if two people borrowed the last kit at the same moment?
- Why is this table in 3NF?
- Change this field to be required, live.
- What would you do next, and why that first?
