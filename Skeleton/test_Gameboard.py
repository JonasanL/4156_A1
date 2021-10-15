import unittest
from Gameboard import Gameboard


class Test_TestGameboard(unittest.TestCase):
    #TEsting
    #siodjao
    def test_happy_move(self):
        # Test case 1: Happy path for correct move
        game = Gameboard()
        game.player1 = "red"
        game.player2 = "yellow"

        game.player1_move("col1")
        self.assertEqual(game.board[5][0], "red")

    def test_invalid_turn(self):
        # Test case 2: Invalid move - not current turn
        game = Gameboard()
        game.player1 = "red"
        game.player2 = "yellow"

        game.player1_move("col1")
        self.assertEqual(game.board[5][0], "red")
        game.player1_move("col1")
        self.assertEqual(game.board[4][0], 0)

        game.player2_move("col1")
        self.assertEqual(game.board[4][0], "yellow")
        game.player2_move("col1")
        self.assertEqual(game.board[3][0], 0)

    def test_invalid_move_winner(self):
        # Test Case 3: Invalid move - winner already declared
        game = Gameboard()
        game.player1 = "red"
        game.player2 = "yellow"
        for i in range(3):
            game.board[5][i] = "red"

        game.player1_move("col4")
        game.player2_move("col5")
        self.assertEqual(game.board[5][4], 0)
        game.player2_move("col5")
        self.assertEqual(game.board[5][4], 0)

    def test_invalid_move_draw(self):
        # Test Case 4: Invalid move - draw (tie)
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
        game.remaining_moves = 1
        game.player1_move("col7")
        self.assertEqual(game.board[0][6], "red")

        self.assertEqual(
            game.player2_move("col7"),
            (game.board, True, "It is a draw. No Move Available", "")
            )
        self.assertEqual(
            game.player1_move("col7"),
            (game.board, True, "It is a draw. No Move Available", "")
            )

        self.assertEqual(game.board[0][6], "red")

    def test_invalid_move_column_full(self):
        # Test Case 5: Invalid move - current column is filled
        game = Gameboard()
        game.player1 = "red"
        game.player2 = "yellow"

        game.player1_move("col7")
        self.assertEqual(game.board[5][6], "red")
        game.player2_move("col7")
        self.assertEqual(game.board[4][6], "yellow")
        game.player1_move("col7")
        self.assertEqual(game.board[3][6], "red")
        game.player2_move("col7")
        self.assertEqual(game.board[2][6], "yellow")
        game.player1_move("col7")
        self.assertEqual(game.board[1][6], "red")
        game.player2_move("col7")
        self.assertEqual(game.board[0][6], "yellow")
        self.assertEqual(
            game.player1_move("col7"),
            (game.board, True, "Invalid Move", "")
            )
        self.assertEqual(game.board[0][6], "yellow")
        game.player1_move("col6")
        self.assertEqual(
            game.player2_move("col7"),
            (game.board, True, "Invalid Move", "")
            )

    def test_happy_move_winning_horizontal(self):
        # Test Case 6: Happy path for winning move in each of horizontal
        game = Gameboard()
        game.player1 = "red"
        game.player2 = "yellow"

        game.player1_move("col7")
        game.player2_move("col7")

        game.player1_move("col6")
        game.player2_move("col6")

        game.player1_move("col5")
        game.player2_move("col5")

        self.assertEqual(
            game.player1_move("col4"),
            (game.board, True, "We have a winner!", game.game_result)
            )

    def test_happy_move_winning_vertical(self):
        # Test Case 7: Happy path for winning move in each of vertical
        game = Gameboard()
        game.player1 = "red"
        game.player2 = "yellow"

        game.player1_move("col7")
        game.player2_move("col6")

        game.player1_move("col7")
        game.player2_move("col6")

        game.player1_move("col7")
        game.player2_move("col6")

        self.assertEqual(
            game.player1_move("col7"),
            (game.board, True, "We have a winner!", game.game_result)
            )

    def test_happy_move_winning_negdiagonal(self):
        # Test Case 8: winning move in each of negative slope diagonal
        game = Gameboard()
        game.player1 = "red"
        game.player2 = "yellow"

        game.player1_move("col7")
        game.player2_move("col6")

        game.player1_move("col6")
        game.player2_move("col5")

        game.player1_move("col4")
        game.player2_move("col5")

        game.player1_move("col5")
        game.player2_move("col4")

        game.player1_move("col4")
        game.player2_move("col3")

        self.assertEqual(
            game.player1_move("col4"),
            (game.board, True, "We have a winner!", game.game_result)
            )

    def test_happy_move_winning_posdiagonal(self):
        # Test Case 9: winning move in each of negative slope diagonal
        game = Gameboard()
        game.player1 = "red"
        game.player2 = "yellow"

        game.player1_move("col1")
        game.player2_move("col2")

        game.player1_move("col2")
        game.player2_move("col3")

        game.player1_move("col4")
        game.player2_move("col3")

        game.player1_move("col3")
        game.player2_move("col4")

        game.player1_move("col4")
        game.player2_move("col5")

        self.assertEqual(
            game.player1_move("col4"),
            (game.board, True, "We have a winner!", game.game_result)
            )
        self.assertEqual(
            game.player2_move("col4"),
            (game.board, True, "We have a winner!", game.game_result)
            )
        self.assertEqual(
            game.player1_move("col4"),
            (game.board, True, "We have a winner!", game.game_result)
            )

    def test_connection(self):
        # Test Case 10: Before each player connect no one can move
        game = Gameboard()
        self.assertEqual(
            game.player1_move("col4"),
            (game.board, True, "Some Player are not connected", "")
            )
        game.player1 = "red"
        self.assertEqual(
            game.player2_move("col4"),
            (game.board, True, "Some Player are not connected", "")
            )

    def test_check_if_connected(self):
        # Test Case 11: Test if both player are all connected or not
        game = Gameboard()
        self.assertEqual(game.check_if_connected(), True)
        game.player1 = "red"
        self.assertEqual(game.check_if_connected(), True)
        game.player2 = "yellow"
        self.assertEqual(game.check_if_connected(), False)

    def test_check_turn(self):
        # Test Case 12: Test when the game started, the turn start with p1
        game = Gameboard()
        self.assertEqual(game.check_turn("p1"), True)
        self.assertEqual(game.check_turn("p2"), False)

    def test_check_valid_move(self):
        # Test Case 13: it will not let you to keep adding when column is full
        game = Gameboard()
        for i in range(5, -1, -1):
            self.assertEqual(game.check_valid_move("col1"), True)
            game.board[i][0] = "red"
        self.assertEqual(game.check_valid_move("col1"), False)

    def test_position_in_board(self):
        # Test Case 14: Test if position is inbound within the board
        game = Gameboard()
        self.assertEqual(game.check_bound(2, 3), True)
        self.assertEqual(game.check_bound(8, 8), False)

    def test_happy_move_winning_horizontalp2(self):
        # Test Case 15: winning move in each of horizontal (P2)
        game = Gameboard()
        game.player1 = "red"
        game.player2 = "yellow"

        game.player1_move("col7")
        game.player2_move("col7")

        game.player1_move("col6")
        game.player2_move("col6")

        game.player1_move("col5")
        game.player2_move("col5")

        game.player1_move("col3")
        game.player2_move("col4")
        game.player1_move("col3")
        self.assertEqual(
            game.player2_move("col4"),
            (game.board, True, "We have a winner!", game.game_result)
            )
