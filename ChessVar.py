# Author: Harmun Sandhu
# GitHub username: Harmun1
# Description: Class that represents a game of atomic chess, where the goal is to destroy the opponent's king.

class ChessVar:
    """Represents Chess Game object"""
    def __init__(self):
        """Takes board as a parameter, as well as turn and game state."""
        self.__board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        self.__turn = 'white'
        self.__game_state = 'UNFINISHED'

    def get_game_state(self):
        """Returns state of game"""
        return self.__game_state

    def make_move(self, from_square, to_square):
        """Returns move made based on unfinished game"""
        if self.__game_state != 'UNFINISHED':
            return False

        from_row, from_column = 8 - int(from_square[1]), ord(from_square[0]) - ord('a')
        to_row, to_column = 8 - int(to_square[1]), ord(to_square[0]) - ord('a')

        piece = self.__board[from_row][from_column]
        target = self.__board[to_row][to_column]

        if piece == ' ' or (self.__turn == 'white' and piece.islower()) or (self.__turn == 'black' and piece.isupper()):
            return False

        if not self.is_move_legal(piece, from_row, from_column, to_row, to_column):
            return False

        self.__board[from_row][from_column] = ' '

        if target != ' ':
            self.explode(to_row, to_column)
        else:
            self.__board[to_row][to_column] = piece

        if piece.lower() == 'k':
            self.__game_state = 'BLACK_WON' if self.__turn == 'white' else 'WHITE_WON'

        self.__turn = 'black' if self.__turn == 'white' else 'white'
        return True

    def is_move_legal(self, piece, from_row, from_column, to_row, to_column):
        """Checks if move is legal within game rules"""
        if piece.lower() == 'k' and self.__board[to_row][to_column] != ' ':
            return False
        return self.is_standard_chess_move(piece, from_row, from_column, to_row, to_column)

    def is_standard_chess_move(self, piece, from_row, from_column, to_row, to_column):
        """Checks if move is legal within standard chess rules"""
        if piece.lower() == 'p':
            direction = -1 if piece.isupper() else 1
            if from_column == to_column:
                if self.__board[to_row][to_column] != ' ':
                    return False
                if from_row + direction == to_row:
                    return True
                if (from_row == 1 and direction == 1 or from_row == 6 and direction == -1) and from_row + 2 * direction == to_row and self.__board[from_row + direction][from_column] == ' ':
                    return True
            elif abs(from_column - to_column) == 1 and from_row + direction == to_row and self.__board[to_row][to_column] != ' ':
                return True
            return False

        if piece.lower() == 'r':
            if from_row != to_row and from_column!= to_column:
                return False
            return self.is_path_clear(from_row, from_column, to_row, to_column)

        if piece.lower() == 'n':
            return abs(from_row - to_row) == 2 and abs(from_column - to_column) == 1 or abs(from_row - to_row) == 1 and abs(from_column - to_column) == 2

        if piece.lower() == 'b':
            if abs(from_row - to_row) != abs(from_column - to_column):
                return False
            return self.is_path_clear(from_row, from_column, to_row, to_column)

        if piece.lower() == 'q':
            if abs(from_row - to_row) == abs(from_column - to_column) or from_row == to_row or from_column == to_column:
                return self.is_path_clear(from_row, from_column, to_row, to_column)

        if piece.lower() == 'k':
            return abs(from_row - to_row) <= 1 and abs(from_column - to_column) <= 1

        return False

    def is_path_clear(self, from_row, from_column, to_row, to_column):
        """Checks if there are no pieces in object's path"""
        start_row = (to_row - from_row) // max(1, abs(to_row - from_row))
        start_column = (to_column - from_column) // max(1, abs(to_column - from_column))
        current_row, current_column = from_row + start_row, from_column + start_column
        while current_row != to_row or current_column != to_column:
            if self.__board[current_row][current_column] != ' ':
                return False
            current_row += start_row
            current_column += start_column
        return True

    def explode(self, row, column):
        """Returns explosion of piece"""
        for list in range(row - 1, row + 2):
            for numbers in range(column - 1, column + 2):
                if 0 <= list < 8 and 0 <= numbers < 8 and (list != row or numbers != column) and self.__board[list][numbers] != ' ':
                    if self.__board[list][numbers].lower() != 'p':
                        if self.__board[list][numbers].lower() == 'k':
                            self.__game_state = 'BLACK_WON' if self.__board[list][numbers].islower() else 'WHITE_WON'
                        self.__board[list][numbers] = ' '
        self.__board[row][column] = ' '

    def print_board(self):
        """Returns current state of board"""
        print('  a b c d e f g h')
        for list in range(8):
            print(8 - list, end=' ')
            for numbers in range(8):
                print(self.__board[list][numbers], end=' ')
            print(8 - list)
        print('  a b c d e f g h')

