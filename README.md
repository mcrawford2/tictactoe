# What does this project do?
This is a Tic-Tac-Toe web app with two playable options. In my proposal, I mentioned adding different game modes. I ended up only creating with the basic version of tic tac toe, but did expand the terminal version to also be a Flask app. tictactoe.py is the file for the terminal game for two human players on the same machine. It handles input validation, win/draw detection, and prompts to replay.app.py + index.html + JS/CSS are for the Flask web version. Tis is a browser version of the same game, although more visually appealing. The Flask backend has a REST API (/api/state, /api/move, /api/new-game, /api/player-names) that stores game state in memory server side. The frontend renders the board, handles clicks, and uses fetch to sync with the server. Similar to the terminal version, both players share the same browser tab/session. 

# How do I run it?
Terminal version:
1. run tictactoe.py

Flask version: 
1. run pip install flask
2. run python flask.app.py
3. open http://127.0.0.1:5000 in your browser. #not working????
