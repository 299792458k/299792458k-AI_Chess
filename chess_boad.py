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






# # import package pygame
# import pygame

# def run():
# 	# with not resizable
# 	pygame.init()
# 	size = 640
# 	backgroundColor = (36,106,99)

# 	screen = pygame.display.set_mode((size+160,size))
# 	screen.fill(backgroundColor)
# 	# set title
# 	pygame.display.set_caption('Chess')

# 	#draw board
# 	for i in range (8):
# 		for j in range(8):
# 			if (i+j) % 2 == 0:
# 				pygame.draw.rect(screen, (240,240,240), [(i+1)*80,j*80,80,80])
# 			else:
# 				pygame.draw.rect(screen, (107,107,107), [(i+1)*80,j*80,80,80])

# 	# run window
# 	running = True
# 	while running:
# 		for event in pygame.event.get():
# 			if event.type == pygame.QUIT:
# 				running = False

# 		pygame.display.update()

# 	# quit pygame after closing window
# 	pygame.quit()

