## Date: 2026-23-04

**What I asked AI to do:**
- asked AI to help create a plan
- asked AI to simplify code, to see if what was already written was too complicated and ty to understand other methods of making the game

**What I didn't understand in the generated code:**
- the plan is outputed was:
1. Represent the board as a 9-item list, with positions 1 to 9 mapped to grid spaces.
2. Write a draw_board() function that prints the grid in a readable 3x3 layout.
3. Write a get_move() function that asks the current player for input and rejects invalid or occupied squares.
4. Write check_winner() and check_draw() using the 8 standard winning combinations.
5. Write the main loop that alternates X and O, updates the board, redraws it, and stops when someone wins or the board fills up.
6. Only after that, add extra modes and then consider Flask if you still want a visual version.
- having this plan made making the program seem a lot less daunting, and more easily understandable

- when I asked AI to simplify code, it changed the code in a way that was more confusing to understand. Variable/parameter names were shortened to letter names that less directly matched what they were for, and the sequence of events in each function seemed out of order. 

**What I learned:**
- having the plan AI created made making the program seem a lot less daunting, and more easily understandable
- after asking AI to simplify the code I had and reading through it, I decided to undo changes and keep the original code. This reenforced that AI may have beneficial capabilities a lot of the time, but it is important to always know what changes it makes to your code.


## Date: 2026-24-04

**What I asked AI to do:**
- asked AI where in the code to add "play again" at the end of the game
- asked AI to help with creating the get_player_name() function, specifically the parameters
- asked AI to help update any instances of Player X and PLayer O to be user inputted names

**What I didn't understand in the generated code:**
- i didn't understand why symbol was the parameter for get_player_name()

**What I learned:**
- asking where to add the code reenforces my learning the order of code writting
- symbol is just a label for the player mark, not the actual player name which gets inputted


## Date: 2026-25-04

**What I asked AI to do:**
- asked AI for help with understanding how the project should be structered when introducing Flask
- asked AI what should be imported for Flask and this game
- asked AI how to open the Flask app html, because I remember last time I used Flask I did it incorrectly through opening Live Server

**What I didn't understand in the generated code:**
- i don't understand why some files, such as index.html, need to be seperated into different folders
- to open FLask app, I did pip install flask and then tried starting the app through the terminal, but that did not work

**What I learned:**
- folders are needed because flask searches specifically inside a folder named templates/ if you call render_template("index.html")
- i imported Flask, jsonify, render_template, request, from Flask.
    - Flask: the core class to create the app
    - jsonify: converts a Python dict or list into a proper JSON HTTP response, mainly useful for APIs
    - render_template: the function that finds the HTML file in the templates/ folder and returns it as a response
    - request: gives access to incoming data from the browser

## Date: 2026-25-04

**What I asked AI to do:**
- asked AI to help fix flask errors
- asked AI to remove a specific line from index.html
- asked AI to incorporate the player name input into the Flask app

**What I didn't understand in the generated code:**
- the line from index.html I removed was "Flask+Javascript" that appeared on the screen. I did not want to waste time trying to find the exact line, which is why I asked AI to do it for me.
- the option for players to add names 

**What I learned:**
- I removed the text "Flask+Javascript" from the screen because I didn't think that including it would benefit the user experience