"""
storing information about the current state of the game. annalize valid moves.
keep a log of the moves.
"""
class GameState():
    #The board is an 8x8 2d list. each element has 2 digits.
    #first char represents the color of the piece (b=black;w=white)
    #second char represents the type of piece (R=rook;N=knight;B=bishop;K=king;Q=queen;P=pawn)   
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves
                             ,'K': self.getKingMoves, 'Q': self.getQueenMoves, 'B': self.getBishopMoves}
        self.whiteToMove = True
        self.moveLog = []

    def makesMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)#log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove#swap players turn

    def undoMove(self):
        """
        Undo last move movement
        """
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        """
        All moves considering checks
        """
        return self.getAllPossibleMoves() #for now will not consider checks

    def getAllPossibleMoves(self):
        """
        All moves without considering checks
        """
        moves = []
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): #number of collumns in a certain row
                turn = self.board[r][c][0]
                
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        """
        Get all pawn moves for the piece located at row, col and add these moves to the list
        """
        if r>0 and self.whiteToMove:# when the changing pawns is implemented you can remove the row>0 verifications
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r-2, c), self.board))
            if r>0 and c>0 and self.board[r-1][c-1][0] == "b":
                moves.append(Move((r, c), (r-1, c-1), self.board))
            if r>0 and c<7 and self.board[r-1][c+1][0] == "b":
                moves.append(Move((r, c), (r-1, c+1), self.board))
        
        if r<7 and not self.whiteToMove:# when the changing pawns is implemented you can remove the row<7 verifications
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))#move 1 forward
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self.board))#move 2 forward

            if r<7 and c>0 and self.board[r+1][c-1][0] == "w":#Capture left diagonal
                moves.append(Move((r, c), (r+1, c-1), self.board))
            if r<7 and c<7 and self.board[r+1][c+1][0] == "w":#Capture right diagonal
                moves.append(Move((r, c), (r+1, c+1), self.board))

    def getRookMoves(self, r, c, moves):
        """
        Get all Rook moves for the piece located at row, col and add these moves to the list
        """
        i = 0
        while r+i < 7:
            i += 1
            if self.board[r][c][0] != self.board[r+i][c][0]:
                moves.append(Move((r, c), (r+i, c), self.board))
        i = 0
        while r-i > 0:
            i += 1
            if self.board[r][c][0] != self.board[r-i][c][0]:
                moves.append(Move((r, c), (r-i, c), self.board))
        i = 0
        while c+i < 7:
            i += 1
            if self.board[r][c][0] != self.board[r][c+i][0]:
                moves.append(Move((r, c), (r, c+i), self.board))
        i = 0
        while c-i > 0:
            i += 1
            if self.board[r][c][0] != self.board[r][c-i][0]:
                moves.append(Move((r, c), (r, c-i), self.board))

    def getBishopMoves(self, r, c, moves):
        """
        Get all Bishop moves for the piece located at row, col and add these moves to the list
        """
        i = 0
        n = 0
        while r+i < 7 and c+n < 7:
            i += 1
            n += 1
            if self.board[r][c][0] != self.board[r+i][c+n][0]:
                moves.append(Move((r, c), (r+i, c+n), self.board))
        i = 0
        n = 0
        while r-i > 0 and c+n < 7:
            i += 1
            n += 1
            if self.board[r][c][0] != self.board[r-i][c+n][0]:
                moves.append(Move((r, c), (r-i, c+n), self.board))
        i = 0
        n = 0
        while r+i < 7 and c-n > 0:
            i += 1
            n += 1
            if self.board[r][c][0] != self.board[r+i][c-n][0]:
                moves.append(Move((r, c), (r+i, c-n), self.board))
        i = 0
        n = 0
        while r-i > 0 and c-n > 0:
            i += 1
            n += 1
            if self.board[r][c][0] != self.board[r-i][c-n][0]:
                moves.append(Move((r, c), (r-i, c-n), self.board))

    def getKingMoves(self, r, c, moves):
        """
        Get all King moves for the piece located at row, col and add these moves to the list
        """
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if r+i in range(8) and c+j in range(8) and self.board[r+i][c+j][0] != self.board[r][c][0]:
                    moves.append(Move((r, c), (r+i, c+j), self.board))

    def getQueenMoves(self, r, c, moves):
        """
        Get all Queen moves for the piece located at row, col and add these moves to the list
        """
        i = 0
        n = 0
        while r+i < 7 and c+n < 7:
            i += 1
            n += 1
            if self.board[r][c][0] != self.board[r+i][c+n][0]:
                moves.append(Move((r, c), (r+i, c+n), self.board))
        i = 0
        n = 0
        while r-i > 0 and c+n < 7:
            i += 1
            n += 1
            if self.board[r][c][0] != self.board[r-i][c+n][0]:
                moves.append(Move((r, c), (r-i, c+n), self.board))
        i = 0
        n = 0
        while r+i < 7 and c-n > 0:
            i += 1
            n += 1
            if self.board[r][c][0] != self.board[r+i][c-n][0]:
                moves.append(Move((r, c), (r+i, c-n), self.board))
        i = 0
        n = 0
        while r-i > 0 and c-n > 0:
            i += 1
            n += 1
            if self.board[r][c][0] != self.board[r-i][c-n][0]:
                moves.append(Move((r, c), (r-i, c-n), self.board))

        i = 0
        while r+i < 7:
            i += 1
            if self.board[r][c][0] != self.board[r+i][c][0]:
                moves.append(Move((r, c), (r+i, c), self.board))
        i = 0
        while r-i > 0:
            i += 1
            if self.board[r][c][0] != self.board[r-i][c][0]:
                moves.append(Move((r, c), (r-i, c), self.board))
        i = 0
        while c+i < 7:
            i += 1
            if self.board[r][c][0] != self.board[r][c+i][0]:
                moves.append(Move((r, c), (r, c+i), self.board))
        i = 0
        while c-i > 0:
            i += 1
            if self.board[r][c][0] != self.board[r][c-i][0]:
                moves.append(Move((r, c), (r, c-i), self.board))
    
    def getKnightMoves(self, r, c, moves):
        """
        Get all Knight moves for the piece located at row, col and add these moves to the list
        """
        if r>1:
            if c>0:
                if self.board[r][c][0] != self.board[r-2][c-1][0]:
                    moves.append(Move((r, c), (r-2, c-1), self.board))
            if c<7:
                if self.board[r][c][0] != self.board[r-2][c+1][0]:
                    moves.append(Move((r, c), (r-2, c+1), self.board))
        if r<6:
            if c>0:
                if self.board[r][c][0] != self.board[r+2][c-1][0]:
                    moves.append(Move((r, c), (r+2, c-1), self.board))
            if c<7:
                if self.board[r][c][0] != self.board[r+2][c+1][0]:
                    moves.append(Move((r, c), (r+2, c+1), self.board))

        if c>1:
            if r>0:
                if self.board[r][c][0] != self.board[r-1][c-2][0]:
                    moves.append(Move((r, c), (r-1, c-2), self.board))
            if r<7:
                if self.board[r][c][0] != self.board[r+1][c-2][0]:
                    moves.append(Move((r, c), (r+1, c-2), self.board))
        if c<6:
            if r>0:
                if self.board[r][c][0] != self.board[r-1][c+2][0]:
                    moves.append(Move((r, c), (r-1, c+2), self.board))
            if r<7:
                if self.board[r][c][0] != self.board[r+1][c+2][0]:
                    moves.append(Move((r, c), (r+1, c+2), self.board))




class Move():
    #maps keys to values
    # key : value
    ranksToRows = {"1":7, "2":6, "3":5, "4":4,
                   "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a":0, "b":1, "c":2, "d":3, 
                   "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 +self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        """
        Overriding the equals method
        """
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        #You can add to make this like real chess notation
        #if self.board[move.startRow][move.startCol] == "--":
        #   return 0
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
