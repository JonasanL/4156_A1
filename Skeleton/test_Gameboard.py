import unittest
from Gameboard import Gameboard

class Test_TestGameboard(unittest.TestCase):
    def test_check_if_connected(self):
        game = Gameboard()
        self.assertEqual(game.check_if_connected(), True)
        game.player1 = "red"
        self.assertEqual(game.check_if_connected(), True)
        game.player2 = "yellow"
        self.assertEqual(game.check_if_connected(), False)

    def test_check_turn(self):
        game = Gameboard()
        self.assertEqual(game.check_turn("p1"), True)
        self.assertEqual(game.check_turn("p2"), False)

    def test_check_valid_move(self):
        game = Gameboard()
        for i in range(5,-1, -1):
            self.assertEqual(game.check_valid_move("col1"), True)
            game.board[i][0] = "red"
        self.assertEqual(game.check_valid_move("col1"), False)