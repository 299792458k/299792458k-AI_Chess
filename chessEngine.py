"""
THis class is responsible for storing all the information about the currennt state of the chess game. It will also be responsible for determining the vaid moves of thee current state. it will also keep a move log
"""
class GameState():
    def __init__(self):
        # board is an 8x8 2d list, each element of the list has character
        # b, w is color
        # -- : no piece
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'] ]
        self.moveFuntions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                             'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves }
        self.whiteToMove = True
        self.moveLog = []

    """
    Takes a Move as a parameter and executes it (this will not work for castling (nhap thanh), pawn promotion (phong Hau), and en-passsant" (tot an tot)
    """
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'  #di xong=> vi tri cu se rong
        self.board[move.endRow][move.endCol] = move.pieceMoved # Vi tri moi se thay bang quan di chuyen
        self.moveLog.append(move) # Luu tru cac o ma quan co da di => neu co undo thi di lai
        self.whiteToMove = not self.whiteToMove # Ket thuc nuoc di cua 1 ben nguoi choi

    """
    Undo the last move mode
    """
    def undoMove(self):
        if len(self.moveLog) != 0: # make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
    """
    Alll moves considering checks
    """
    def getValidMoves(self):
        return self.getAllPossibleMoves() #for now we will noy worry about check
    """
    All moves without considedring checks
    """
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #number of row
            for c in range(len(self.board[r])): #number of column
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    """
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)
                      #  print(moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)
                        """
                    self.moveFuntions[piece](r, c, moves) #calls the appropriate move function based on piece type
        return moves
    """
      Get all the pawn moves for the pawn located at row, col, and add these moves to the lis
      """
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c] == '--': #1 square on advanced
                moves.append(Move((r, c), (r-1, c), self.board))
                # Do con Tot Trang chi co the di len => Neu no o hang 6 thi chac chan la chua di => first move
                if r == 6 and self.board[r-2][c] == '--': #2 squares for first move
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0 and r > 0:
                if self.board[r-1][c-1][0] == 'b': #enemy piece to capture in the left
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7 and r > 0:
                if self.board[r-1][c+1][0] == 'b': #enemy piece to capture in right
                    moves.append(Move((r, c), (r-1, c+1), self.board))

        else: #black pawn move => chi di xuong
            if self.board[r+1][c] == '--': # 1 square on advanced
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == '--': #2 square on advanced
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0 and r < 7:
                if self.board[r+1][c-1][0] == 'w': #eenmy piece to capture in the left
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7 and r < 7:
                if self.board[r+1][c+1][0] == 'w': #enemy piece to capture in the right
                    moves.append(Move((r, c), (r+1, c+1), self.board))
       #pawn promotion later

    """
      Get all the rook moves for the Rook located at row, col and add these moves to the list
      """
    def getRookMoves(self, r, c, moves): # Tai 1 vi tri cua Xe => xet 7 o con lai theo hang, cot( 4 huong, 14 o)
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) #up, left, down, right
        if self.whiteToMove:
            enemyColor = 'b'
        else:
            enemyColor = 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7: #On board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--': # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #enemy piece vaid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: #friendly piece
                        break
                else: #off board
                    break


    """
          Get all the rook moves for the Knight located at row, col and add these moves to the list
          """
    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2),
                       (1, -2), (1, 2), (2, -1), (2, 1))
    #UPleft, UPright, upLEFT, upRIGHT,  downLEFT, downRIGHT, DOWNleft, DOWNright
        if self.whiteToMove:
            allyColor = 'w'
        else:
            allyColor = 'b'
        for a in knightMoves:
            endRow = r + a[0]
            endCol = c + a[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7: # On board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #(not ally piece <=> empty piece or enemy piece
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    """
          Get all the rook moves for the Bishop located at row, col and add these moves to the list
          """
    def getBishopMoves(self, r, c, moves, endRow=None): # Tuong, gan nhu xe, cung xet 4 huong
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) #(r,c)
                    #, (up-left), (up-right), (down-left), (down-right)
        if self.whiteToMove:
            enemyColor = 'b'
        else:
            enemyColor = 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7: # on boar
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: # bao gom ca dieu kien la enemy va empty
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: #friendly piece invalid (Co quan minh can => khong di duoc)
                        break
                else: #off board
                    break


    """
          Get all the Queen moves for the Queen located at row, col and add these moves to the list
          """
    def getQueenMoves(self, r, c, moves):
        # Queen = Rook + Bshop
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)

    """
          Get all the rook moves for the King located at row, col and add these moves to the list
          """
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        if self.whiteToMove:
            allyColor = 'w'
        else:
            allyColor = 'b'
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7: #ON board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # gap enemy or empty
                    moves.append(Move((r, c), (endRow, endCol), self.board))




class Move():
    # Map( dictionary) : keys to value => key : value

    ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4,
                   '5': 3, '6': 2, '7': 1, '8': 0}
    rowsToRanks = {v: u for u, v in ranksToRows.items()}
    filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                   'e': 4, 'f': 5, 'g': 6, 'h': 7}
    colsToFiles = {v: u for u, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol] #VI tri ban dau di chuyen => nguon
        self.pieceCaptured = board[self.endRow][self.endCol] # Vi tri se di chuyen toi => Dich
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        #=> Hash function : moveid
       # print(self.moveID)

    """
    Overriding the equals method
    """
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        # to make this like real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]