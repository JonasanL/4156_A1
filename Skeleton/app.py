from flask import Flask, render_template, request, jsonify
from Gameboard import Gameboard
import logging

app = Flask(__name__)

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
    return render_template('player1_connect.html', status="Pick a Color.")


'''
Helper function that sends to all boards don't modify
'''


@app.route('/autoUpdate', methods=['GET'])
def updateAllBoards():
    try:
        return jsonify(move=game.board, winner=game.game_result,
                       color=game.player1)
    except Exception:
        return jsonify(move="")


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
    return render_template('player1_connect.html', status=game.player1)


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

    return render_template("p2Join.html", status=game.player2)


@app.route('/move1', methods=['POST'])
def p1_move():
    move = request.json['column']

    info = game.player1_move(move)
    if len(info) < 4:
        return jsonify(
            move=info[0],
            invalid=info[1],
            winner=info[2]
            )

    return jsonify(
        move=info[0],
        invalid=info[1],
        reason=info[2],
        winner=info[3]
        )


'''
Same as '/move1' but instead proccess Player 2
'''


@app.route('/move2', methods=['POST'])
def p2_move():
    move = request.json['column']

    info = game.player2_move(move)
    if len(info) < 4:
        return jsonify(
            move=info[0],
            invalid=info[1],
            winner=info[2]
            )

    return jsonify(
        move=info[0],
        invalid=info[1],
        reason=info[2],
        winner=info[3]
        )


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
