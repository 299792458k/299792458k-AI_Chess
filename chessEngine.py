from pygame.constants import BLENDMODE_ADD


class gameState():

	def __init__(self):
		#simulate the chess board
		self.board = [
						["bR","bN","bB","bQ","bK","bB","bN","bR"],
						["bp","bp","bp","bp","bp","bp","bp","bp"],
						["--","--","--","--","--","--","--","--"],
						["--","--","--","--","--","--","--","--"],
						["--","--","--","--","--","--","--","--"],
						["--","--","--","--","--","--","--","--"],
						["wp","wp","wp","wp","wp","wp","wp","wp"],
						["wR","wN","wB","wQ","wK","wB","wN","wR"],
					 ]
		self.moveLog = []
		self.whiteToMove = True
	# take a move as a parameter and execute it (not including castling, pawn promotion and en-passant)
	def makeMove(self, move):    # move is an object of Move()
		self.board[move.startRow][move.startCol] = "--"
		self.board[move.endRow][move.endCol] = move.pieceMoved
		self.moveLog.append(move)	#log the move so we can undo it later
		self.whiteToMove = not self.whiteToMove #swap player
	def undoMove(self):
		if len(self.moveLog)!=0:  # make sure there is a move to undo
			move = self.moveLog.pop()
			self.board[move.startRow][move.startCol] = move.pieceMoved
			self.board[move.endRow][move.endCol] = move.pieceCaptured
			self.whiteToMove = not self.whiteToMove   #swap players

	'''
	all moves considering checks
	'''
	def getValidMoves(self):
		return self.getAllPossibleMoves()
	'''
	all possible moves ( # considering checks)
	'''
	def getAllPossibleMoves(self):
		moves = [Move((6,4),(4,4),self.board)]   #why it doesn't work? 2 diff objects
		for r in range(len(self.board)):
			for c in range(len(self.board[r])):
				turn = self.board[r][c][0]	#to check whether the piece is 'w' or 'b'
				if (turn=='w' and self.whiteToMove) and (turn=='b' and not self.whiteToMove):
					piece = self.board[r][c][1] 
					if piece == 'p':
						self.getPawnMoves(r,c,moves)
					if piece == "R":
						self.getRookMoves(r,c,moves)
		return moves
	'''
	get all the pawn moves for the pawn located at row,col and add these moves to list moves
	'''					
	def getPawnMoves(self,r,c,moves):
		self
	def getRookMoves(self,r,c,moves):
		self

	
class Move():
	# make chess notation (instead of 0->7,0->7)
	# map keys to values 
	# key : value
	ranksToRows = {"1":7,"2":6,"3":5,"4":4,
				   "5":3,"6":2,"7":1,"8":0}
	rowsToRanks = {v: k for k, v in ranksToRows.items()} # cool way to make a reverse of dictionary
	filesToCols = {"a":0,"b":1,"c":2,"d":3,
				   "e":4,"f":5,"g":6,"h":7}
	colsToFiles = {v: k for k, v in filesToCols.items()}
	def __init__(self,startSq,endSq,board):
		self.startRow = startSq[0]
		self.startCol = startSq[1]
		self.endRow = endSq[0]
		self.endCol = endSq[1]
		self.pieceMoved = board[self.startRow][self.startCol]
		self.pieceCaptured = board[self.endRow][self.endCol]
		self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol  # to override the equals method
		print(self.moveID)

	'''
	overriding the equals method
	'''
	def __eq__(self, other) -> bool:
		if isinstance(other,Move):
			return self.moveID==other.moveID
		return False
	def getChessNotation(self):
		return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)
	
	def getRankFile(self,r,c):
		return self.colsToFiles[c] + self.rowsToRanks[r]





