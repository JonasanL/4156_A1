import unittest

import db
from Gameboard import Gameboard
import json


class Test_Testdbcase(unittest.TestCase):

    def test_empty_start(self):
        # Test empty start
        db.clear()
        db.clear()
        db.init_db()
        print(db.getMove())
        self.assertEqual(db.getMove(), None)
        db.clear()
        self.assertEqual(db.getMove(), None)

    def test_up_and_download(self):
        # Upload state to SQL then load it
        db.init_db()
        game = Gameboard()
        game.player1 = "red"
        game.player2 = "yellow"
        game.board = [
            ["red", "yellow", "red", "yellow", "red", "yellow", 0],
            ["red", "yellow", "red", "yellow", "red", "yellow", "red"],
            ["yellow", "red", "yellow", "red", "yellow", "red", "yellow"],
            ["red", "yellow", "red", "yellow", "red", "yellow", "red"],
            ["red", "yellow", "red", "yellow", "red", "yellow", "red"],
            ["red", "yellow", "red", "yellow", "red", "yellow", "red"]
        ]
        self.current_turn = 'p1'

        db.add_move(
            (
                game.current_turn,
                json.dumps(game.board),
                game.game_result,
                game.player1,
                game.player2,
                game.remaining_moves
                )
            )
        sql = db.getMove()
        sqlList = []
        for element in sql:
            sqlList.append(element)
        sqlList[1] = json.loads(sqlList[1])
        self.assertEqual(
            sqlList,
            [
                game.current_turn,
                game.board,
                game.game_result,
                game.player1,
                game.player2,
                game.remaining_moves
                ]
        )


if __name__ == '__main__':
    unittest.main()
