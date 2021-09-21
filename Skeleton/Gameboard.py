import db

class Gameboard():
    def __init__(self):
        self.player1 = ""
        self.player2 = ""
        self.board = [[0 for x in range(7)] for y in range(6)]
        self.game_result = ""
        self.current_turn = 'p1'
        self.remaining_moves = 42
    




    '''
    Add Helper functions as needed to handle moves and update board and turns
    '''
    def check_if_connected(self):
        return (self.player1 == "" or self.player2 == "")

    def check_turn(self, player):
        return (self.current_turn == player)

    def check_valid_move(self, move):
        column = int(move[3]) - 1
        for i in range(0, 6):
            if self.board[i][column] == 0:
                return True

        return False

    def place_move(self, move, color):
        column = int(move[3]) - 1
        for i in range(5, -1, -1):
            if self.board[i][column] == 0:
                self.board[i][column] = color
                self.remaining_moves -= 1
                return (i, column)

    def check_position_in_board(self, row, column):
        if row < 0 or column < 0:
            return False
        if row > 5 or column > 6:
            return False
        return True

    def check_if_win(self, color):

        directions = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]
        for row in range(0, 6):
            for column in range(0,7):
                if self.board[row][column] == color:
                    for direction in directions:
                        dr, dc = direction
                        count = 0
                        for i in range(1,4):
                            if not self.check_position_in_board(row + dr * i, column + dc * i):
                                break
                            if self.board[row + dr * i][column + dc * i] == color:
                                count += 1;
                        if count == 3:
                            return True

        return False


    
