# Team-project - Team Yellow

## Project Description

Our team is developing a Tetris game using **Python and Pygame**. Players can move, rotate, and drop Tetris blocks while trying to clear rows.

We are using ASE 420 software engineering concepts to improve the original Tetris code, including better organization, reducing global variables, and making the code easier to understand and test.

## Features and Requirements

* Display a Tetris game board.
* Create and display different Tetris blocks.
* Move blocks left and right.
* Move blocks down and drop them.
* Rotate blocks.
* Detect collisions.
* Clear completed rows.
* Track score and level.
* Detect game over.
* Test the game and fix bugs.

## Architecture

The game uses Python and Pygame. The board is represented with a two-dimensional list, and the Tetris blocks are represented using Python data structures.

The project will be separated into functions/classes for areas such as the board, blocks, movement, collision detection, scoring, and game flow.

## Team Responsibilities

Each of the 3 team members has **8 assigned tasks**. Team members will also help with testing, integration, GitHub, and documentation.

### Team Member 1 - Eurydice

* 8 assigned project tasks
1. next piece preview 
2. hold piece
3. ghost piece
4. Hard drop 
5. soft drop
6. wall kick / better rotation
7. Random piece generator
8. piece rotation improvements

### Team Member 2 - Daniel

* 8 assigned project tasks
1. score systems
2. level system
3. increasing fall speed
4. combo system
5. back - to back bonus
6. high score/leadership
7. lines cleared statics
8. Diffculty levels

* Testing and integration

### Team Member 3 - Maryan

* 8 assigned project tasks
1. start menu
2. pause / Resume
3. Game-Over screen
4. theme / color selection
5. sound effect 
6. setting menu
7. interagrate everyon's responsibility, not just yours:
8. Restart Game
## Tools

* Python
* Pygame
* VS Code
* Git/GitHub
* Python `venv`
* Markdown/Obsidian

## Project Links

* GitHub: https://github.com/maryan2005/Team-project
* Canvas: https://nku.instructure.com/courses/91834/modules/items/4231102
* Architecture: Add link when completed
* Design: Add link when completed


Create a playable Tetris board.
Display the board using Pygame.
Represent the board using Python data structures.
Display falling blocks on the board.
Detect when the game is over.
Block Movement

Requirements:

Move blocks left and right.
Move blocks downward.
Rotate blocks.
Drop blocks instantly using the spacebar.
Prevent blocks from moving outside the board.
Detect collisions with other blocks.
Line Clearing and Scoring
change user 

Requirements:

Detect when a row is completely filled.
Clear completed rows.
Move the remaining blocks downward.
Track the player's score.
Add a level system that increases the game's difficulty.
Game Interface

Requirements:

Display the Tetris board.
Display falling blocks in different colors.
Show the current score.
Display a game-over message.
Allow the player to close the game.
Data Model and Architecture
Board Representation

The game will use a two-dimensional Python list to represent the Tetris board. Each position on the board will store a value representing whether the space is empty or contains a block.

The board will have a height of 20 rows and a width of 10 columns.

Block Representation

The game will use different block shapes and rotations. Each block will have a position, color, type, and rotation.

The block shapes will be stored in Python data structures and used to display and move the blocks.

Software Architecture

The team will organize the project into separate functions and classes. Each part of the game will have a specific responsibility, such as handling movement, drawing the board, checking collisions, or managing the score.

We will also work on improving the original code by reducing unnecessary global variables, using immutable data where appropriate, and making functions easier to understand and test.

Tools
Python
Pygame
VS Code
Git and GitHub
Python virtual environment (venv)
Markdown/Obsidian for documentation
Team Members and Roles
Team Member 1

Responsibilities:

Work on the Tetris board.
Improve the board data structure.
Implement board initialization.
Work on drawing the board.
Improve the board display.
Help with collision detection.
Test board-related functions.
Document the board design.
Team Member 2

Responsibilities:

Work on Tetris block shapes.
Implement block movement.
Implement block rotation.
Improve block spawning.
Work on collision detection.
Implement block dropping.
Test movement and rotation.
Document the block system.
Team Member 3

Responsibilities:

Work on line clearing.
Implement the scoring system.
Improve the level system.
Work on game-over detection.
Improve the game interface.
Help with Pygame event handling.
Test the complete game.
Document the scoring and game flow.
Shared Team Responsibilities

All team members will work together on:

Designing the overall project.
Using Git and GitHub.
Refactoring the original code.
Testing the complete game.
Fixing bugs.
Reviewing each other's code.
Creating project documentation.
Preparing the final presentation.
Links to Documentation and Code
GitHub Repository: (https://github.com/maryan2005/Team-project)
Architecture Document: Add your architecture document link.
Design Document: Add your design document link.
Project Documentation: Add your documentation link.
Canvas link: https://nku.instructure.com/courses/91834/modules/items/4231102

