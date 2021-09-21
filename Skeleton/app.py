from flask import Flask, render_template, request, redirect, jsonify
from json import dump
from Gameboard import Gameboard
import db


app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

game = Gameboard()

'''
Implement '/' endpoint
Method Type: GET
return: template player1_connect.html and status = "Pick a Color."
Initial Webpage where gameboard is initialized
'''


@app.route('/', methods=['GET'])
def player1_connect():
    global game
    game = Gameboard()
    return render_template('player1_connect.html', status = "Pick a Color.")




'''
Helper function that sends to all boards don't modify
'''


@app.route('/autoUpdate', methods=['GET'])
def updateAllBoards():
    try:
        return jsonify(move = game.board, winner = game.game_result,
                       color = game.player1)
    except Exception:
        return jsonify(move = "")


'''
Implement '/p1Color' endpoint
Method Type: GET
return: template player1_connect.html and status = <Color picked>
Assign player1 their color
'''


@app.route('/p1Color', methods=['GET'])
def player1_config():
    player1_color = request.args.get('color')
    game.player1 = player1_color
    return render_template('player1_connect.html', status = game.player1)


'''
Implement '/p2Join' endpoint
Method Type: GET
return: template p2Join.html and status = <Color picked> or Error
if P1 didn't pick color first

Assign player2 their color
'''


@app.route('/p2Join', methods=['GET'])
def p2Join():
    if game.player1 == "":
        return "Player 1 does not pick color!", 400

    if game.player1 == "red":
        game.player2 = "yellow"
    else:
        game.player2 = "red"

    return render_template("p2Join.html", status = game.player2)

'''
Helper for move
'''

def check_if_connected():
    return (game.player1 == "" or game.player2 == "")

def check_turn(player):
    return (game.current_turn == player)

def check_valid_move(move):
    column = int(move[3]) - 1
    for i in range(0, 6):
        if game.board[i][column] == 0:
            return True

    return False

def place_move(move, color):
    column = int(move[3]) - 1
    for i in range(5, -1, -1):
        if game.board[i][column] == 0:
            game.board[i][column] = color
            game.remaining_moves -= 1
            return (i, column)

def check_position_in_board(row, column):
    if row < 0 or column < 0:
        return False
    if row > 5 or column > 6:
        return False
    return True

def check_if_win(color):

    directions = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]
    for row in range(0, 6):
        for column in range(0,7):
            if game.board[row][column] == color:
                for direction in directions:
                    dr, dc = direction
                    count = 0
                    for i in range(1,4):
                        if not check_position_in_board(row + dr * i, column + dc * i):
                            break
                        if game.board[row + dr * i][column + dc * i] == color:
                            count += 1;
                    if count == 3:
                        return True

    return False


'''
Implement '/move1' endpoint
Method Type: POST
return: jsonify (move=<CurrentBoard>,
invalid=True or False, winner = <currWinner>)
If move is valid --> invalid = False else invalid = True
If invalid == True, also return reason= <Why Move is Invalid>

Process Player 1's move
'''




@app.route('/move1', methods=['POST'])
def p1_move():
    if game.game_result != "":
        return jsonify(move = game.board, invalid = True, reason = "We have a winnder!", winner = game_result)
    if game.remaining_moves == 0:
        return jsonify(move = game.board, invalid = True, reason = "No Move Available", winner = "")
    if check_if_connected():
        return jsonify(move = game.board, invalid = True, reason = "Some Player are not connected", winner = "")

    if not check_turn("p1"):
        return jsonify(move = game.board, invalid = True, reason = "It is not your turn yet", winner = "")

    move = request.json['column']

    if not check_valid_move(move):
        return jsonify(move = game.board, invalid = True, reason = "Invalid Move", winner = "")

    position = place_move(move, game.player1)

    game.current_turn = "p2"

    if check_if_win(game.player1):
        game.game_result = "p1"
        return jsonify(move = game.board, invalid = True, reason = "We have a winnder!", winner = game_result)

    return jsonify(move = game.board, invalid = False, winner = "")

'''
Same as '/move1' but instead proccess Player 2
'''


@app.route('/move2', methods=['POST'])
def p2_move():
    if game.game_result != "":
        return jsonify(move = game.board, invalid = True, reason = "We have a winnder!", winner = game_result)
    if game.remaining_moves == 0:
        return jsonify(move = game.board, invalid = True, reason = "No Move Available", winner = "")
    if check_if_connected():
        return jsonify(move = game.board, invalid = True, reason = "Some Player are not connected", winner = "")

    if not check_turn("p2"):
        return jsonify(move = game.board, invalid = True, reason = "It is not your turn yet", winner = "")

    move = request.json['column']

    if not check_valid_move(move):
        return jsonify(move = game.board, invalid = True, reason = "Invalid Move", winner = "")

    place_move(move, game.player2)

    game.current_turn = "p1"

    if check_if_win(game.player2):
        game.game_result = "p2"
        return jsonify(move = game.board, invalid = True, reason = "We have a winnder!", winner = game_result)
    
    return jsonify(move = game.board, invalid = False, winner = "")





if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
