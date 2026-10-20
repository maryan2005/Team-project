---
marp: true
theme: default
paginate: true
size: 16:9
footer: "Team Yellow · ASE420 · Sprint 1 Presentation"
style: |
  section {
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    background: linear-gradient(#F5C518, #F5C518) top / 100% 12px no-repeat, #FBFAF6;
    color: #161A23;
    font-size: 30px;
    padding: 50px 66px 64px;
  }
  section h1 {
    font-size: 48px;
    font-weight: 700;
    color: #161A23;
    margin: 0 0 26px 0;
    padding-bottom: 10px;
    border-bottom: 6px solid #F5C518;
    display: inline-block;
  }
  section h3 { color: #5B6475; font-weight: 500; font-size: 30px; margin: 8px 0; }
  section li { margin: 11px 0; line-height: 1.3; }
  section strong { color: #161A23; }
  section blockquote {
    margin: 18px 0 0 0;
    padding: 0 0 0 16px;
    border-left: 5px solid #F5C518;
    color: #5B6475;
    font-size: 21px;
    line-height: 1.35;
  }
  section blockquote p { margin: 0; }
  section::after { color: #5B6475; font-size: 18px; }
  footer { color: #5B6475; font-size: 17px; }
  table { font-size: 26px; border-collapse: collapse; width: 100%; margin: 0; }
  th { background: #161A23; color: #FFFFFF; padding: 9px 16px; text-align: left; font-weight: 600; }
  td { padding: 9px 16px; border-bottom: 1px solid #D9D4C5; vertical-align: top; background: transparent; }
  tr:nth-child(even) td { background: #F3F0E6; }
  img { border-radius: 8px; }
  section.cards ul { list-style: none; padding: 0; margin: 0; }
  section.cards li { background: #FFFFFF; border: 1px solid #E6E1D2; border-left: 8px solid #F5C518; border-radius: 10px; padding: 8px 20px; margin: 9px 0; box-shadow: 0 2px 8px rgba(22, 26, 35, 0.07); font-size: 25px; line-height: 1.25; }
  section p:has(> strong:only-child) { display: table; background: #161A23; padding: 8px 22px; border-radius: 999px; margin: 8px 0 2px; font-size: 25px; }
  section p:has(> strong:only-child) strong { color: #F5C518; }
  section.center p { text-align: center; }
  section.lead { background: #161A23; color: #F2F4F8; justify-content: center; }
  section.lead h1 { letter-spacing: -1px; }
  section.lead h1 { color: #F5C518; border-bottom: none; font-size: 80px; margin-bottom: 12px; }
  section.lead h3 { color: #C9D0DD; font-size: 34px; }
  section.lead p { font-size: 30px; color: #C9D0DD; }
  section.lead footer, section.lead::after { color: #8E97AA; }
  section.shots table { table-layout: fixed; font-size: 22px; margin-bottom: 26px; }
  section.big table { font-size: 38px; width: 78%; margin-bottom: 8px; }
  section.big th, section.big td { padding: 14px 24px; }
  section.shots th { text-align: center; }
  section.shots td { text-align: center; padding: 10px 6px; background: transparent; border-bottom: none; }
  section.shots tr:nth-child(even) td { background: transparent; }
---

<!-- _class: lead -->
<!-- _paginate: false -->

![bg right:34%](images/blocks_art.png)

# Team Yellow: Tetris

### Sprint 1 Presentation · ASE420 · 10/21

Eurydice Lunnemann · Daniel Than · Maryan Abdi

<!--
Intro: we took the one-file Tetris from class and rebuilt it as a game that is organized into classes and tested. Everything shown comes from the Dev branch of github.com/maryan2005/Team-project.
-->

---

<!-- _class: shots -->

# What we built

| Title menu | Gameplay | Pause menu | Game over |
|:-:|:-:|:-:|:-:|
| ![w:262](images/title.png) | ![w:262](images/play_level2.png) | ![w:262](images/pause.png) | ![w:262](images/gameover.png) |


Python and Pygame. The original game was one file full of global variables. It is now split into classes that we can test.

> Screenshots come from the Dev branch code. The gameplay board was staged with scripted drops to show a score and a level.

<!--
Walk through the four screens in order: title menu, gameplay with score and level, pause, then game over with the top 5. Say that the screenshots are rendered from the Dev code and the board was set up with scripted piece drops.
-->

---

<!-- _class: big -->

# Burndown (Sprint 1)

| Measure | Result |
|---|---|
| Features | **3 / 3** |
| Requirements | **15 / 15** |
| Implementation LoC | **1,134** |
| Tests | **62 passing** |


> LoC: non-blank lines in Code/ on Dev, not counting `old_builds` and empty `__init__` files. Tests: pytest on Dev, 62 passed. Feature and requirement counts come from the team plan.

<!--
CHECK before presenting: the feature and requirement counts come from the team plan on Canvas, and they are not in the GitHub repo, so I could not verify them. Eurydice's numbers (1/1 features, 7/7 requirements) plus Daniel's (3/3, 15/15) add up to more than the team totals shown here, so make sure the plan and these slides agree.
-->

---

<!-- _class: center -->

# Contributions at a glance

![w:1090](images/chart_contributions.png)

<!--
The split counted from the repo: 1,004 lines for Eurydice and 130 for Daniel, which adds up to 1,134. Tests: 22 and 40, which adds up to 62.
-->

---

<!-- _class: cards -->

# Eurydice Lunnemann: Movement + Skeleton

- **Code skeleton and architecture:** game engine, state classes, board, piece, and the UML
- **Movement:** timed soft drop, hard drop, and held-key repeat for left and right
- **Rotation:** wall kicks that follow the standard Tetris rotation rules
- **Lock delay:** a landed piece waits half a second before it locks
- **22 tests:** input handling, soft drop, lock delay, and wall kicks

**Features 1/1 · Requirements 7/7 · LoC 1,004 · Tests 22**

> Still to do from the README: hold piece, ghost piece, next-piece preview.

<!--
Counts for features and requirements come from the team plan. LoC and tests are counted from GitHub. The skeleton commit "new architecture" is listed under Sam Lunnemann on GitHub, which we are treating as Eurydice's account.
-->

---

<!-- _class: cards -->

# Daniel Than: Challenge + Scoring

- **Seven features:** score, level, fall speed, combo, lines cleared stats, difficulty presets, and a top 5 leaderboard
- **In the game:** drop scoring, a Level display, and a game over screen with the score and top 5
- **40 tests** for the score manager and the high score repository
- **4 pull requests** (#4 to #7) plus direct commits to Dev
- **Dropped:** the back-to-back bonus, because the game has no T-spin detection

**Features 3/3 · Requirements 15/15 · LoC 130 · Tests 40**

> Still to do: a menu option to choose the difficulty.

<!--
LoC is 130 lines in the current code, counted with git blame. Earlier I reported 138, which was lines added since pull request 4, so use 130 here to match the team total. Counts for features and requirements come from the team plan.
-->

---

# Score, levels, combos

![bg right:38% fit](images/play_level2_crop.png)

- Line clears score **100, 300, 500, 800** for 1 to 4 lines
- Soft drop scores 1 point a row, hard drop 2 points a row
- A **combo** adds 50 points for each earlier clear in a row
- A new **level every 10 lines**, and pieces fall faster each level
- The **top 5 scores** are saved between games

> Screenshot: three tetrises in a row is 12 lines, Level 2, and a score of 2,926.

<!--
This is Daniel's part on the screen. The Score and Level sit above the board. Fall speed goes from half a second per row at level 1 down to a limit of a tenth of a second.
-->

---

<!-- _class: cards -->

# Maryan Abdi: Team Lead + UI

- **Repository:** created it and wrote the README with each member's tasks
- **UI in the game today:** title menu, pause menu, game over screen, and a settings placeholder
- **Presentation:** uploaded the Project Plan presentation to the repo

**Features 0/0 · Requirements 0/0 · LoC 0 · Tests 0**

> Still to do from the README: settings menu, sound effects, theme and color selection, restart flow.

<!--
The UI screens in the code came from the skeleton, and the game over screen was extended in pull request 7.
-->

---

# Schedule (Sprint 1)

| Planned | Actual |
|---|---|
| Project setup | **Done** |
| Bug fixes | **Done** |
| Restructuring of base game | **Done**: one file with globals became classes |
| Rough implementation of new features | **Mostly done**: most features are in |

> Open on Dev: hold piece, ghost piece, next-piece preview, settings menu, sound, theme selection, and choosing the difficulty from a menu.

<!--
Most features are in, not all. The open items are the ones from the README that are still stubs or missing in the Dev code.
-->

---

<!-- _class: cards -->

# Software design ideas we applied

- **State pattern:** the engine switches between Title, Play, Pause, Game Over, and Settings states
- **Program to interfaces:** IScoreManager, IHighScoreRepository, and IInputHandler
- **No global variables:** the board, piece, and score live in classes (the original had Field, Score, and ShiftX as globals)
- **Settings in one place:** the point table, fall speeds, difficulty presets, and key bindings
- **Tests with fakes:** the leaderboard tests use an in-memory repository, so no test touches a file

<!--
Each of these answers one of the code smells that the original tetris_ver2.py file listed in its own comments: globals, magic numbers, and duplicated code.
-->

---

# Retrospective

**Successes**
- The code skeleton at the start gave everyone something to build on
- Learning to use AI greatly increased our productivity
- 62 passing tests and small pull requests

**Challenges**
- Keeping up consistent communication
- Learning new tools for the first time
- An interface change landed before its implementation and broke Dev for a short time. We fixed it and now run the tests before merging.

<!--
The first two successes and the first two challenges are from the original slides. The last success and challenge come from the Dev history.
-->

---

<!-- _class: cards -->

# Schedule (Sprint 2)

- **Finish the required features:** hold piece, ghost piece, next-piece preview, settings menu, sound, and theme selection
- **Wire up difficulty** in the menu, and decide about T-spins and the back-to-back bonus
- **Refine and refactor:** replace the placeholder docs, user manual, and weekly reports
- **Merge Dev into main**, which still holds the original scaffold
- **Prepare the final presentation**

<!--
Main still has the original scaffold and a presentation PDF, and the Sprint 1 code is on Dev. Merge before the final submission.
-->

---

<!-- _class: center -->

# Live demo

[![w:700](images/demo_thumb.png)](https://drive.google.com/file/d/17cyUDQMH_7X_svKMSN6m4o08EJKOvo-P/view)

Click the picture to open the team tech demo video.

<!--
Open the video from Google Drive before the presentation starts, so it is ready in a tab, and keep a downloaded copy as a backup. The Drive link: https://drive.google.com/file/d/17cyUDQMH_7X_svKMSN6m4o08EJKOvo-P/view
-->

---

<!-- _class: lead -->
<!-- _paginate: false -->

![bg left:34%](images/blocks_art.png)

# Thank you

### Questions?

`github.com/maryan2005/Team-project`

<!--
Be ready for: why the state pattern, how the leaderboard is saved, and why back-to-back was dropped.
-->
