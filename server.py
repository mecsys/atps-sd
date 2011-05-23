# -*- coding: UTF-8 -*-
from SimpleXMLRPCServer import SimpleXMLRPCServer
from time import strftime
import random

class User (object):

	def __init__(self, username, password):
		self.__username = username
		self.__password = password
		self.__logged = False

	def getUsername(self):
		return self.__username

	def getPassword(self):
		return self.__password

	def session(self, state=None):
		if state != None:
			self.__logged = state
		return self.__logged

class Session (object):
	"""
	Fornece os funcionalidades básicas para um sistema
	de controlo de sessão.
	"""

	def __init__(self):
		"""
		Inicia um dicionário vazio que servirá com
		base de dados.
		"""
		self.__db = {}

	def login(self,username, password):
		"""
		Altera o estado da sessão para True.
		Args: username, password
		Return: True ou False
		"""
		user = self.__db[username]
		if user.getPassword == password:
			user.session(True)
		return user.session(True)

	def register(self,username, password):
		"""
		Insere um novo user na base de dados.
		Args: username, password
		Return: True ou False
		"""
		self.__db[username] = User(username, password)
		return self.__db.has_key(username)

	def logout(self,username):
		"""
		Altera o estado da sessão para False.
		Args: username
		Return: True ou False
		"""
		user = self.__db[username]
		return not user.session(False)

def currentTime():
	"""
	Permite obter a data e hora actual do servidor.
	Args: None
	Return: String com Data e hora
	Formato da Resposta: YYYY-mm-DD HH:MM:SS
	"""
	return strftime("%Y-%m-%d %H:%M:%S")

# Tic Tac Toe
class Tictactoe (object):
	"""
	Fornece os funcionalidades básicas para o jogo da
	velha.
	"""

	def __init__(self):
		"""
		Inicia uma lista vazia com 10 posicões que
                servirá com base de dados para o tabuleiro.
                Inicia referencia para jogadores.
		"""
		self.__theBoard = self.createBoard()
                self.playerLetter = " "
                self.computer = " "
                self.turn = " "
                print "Tic Tac Toe - Classe instanciada."

        def drawBoard(self):             
                """
                Retarna o tabuleiro para o cliente mostrar 
                na tela.
                """
                # This function prints out the board that it was passed.

                # "board" is a list of 10 strings representing the board (ignore index 0)
                return self.__theBoard

        def setPlayersLetter(self, letter):
                """
                O jogador escolha com qual letra jogar.
                """
                # Let's the player type which letter they want to be.
                # Returns a list with the player's letter as the first item, and the computer's letter as the second.

                # the first element in the tuple is the player's letter, the second is the computer's letter.
                if letter == 'X':
                        self.playerLetter, self.computerLetter = ['X', 'O']
                        return self.playerLetter, self.computerLetter
                else:
                        self.playerLetter, self.computerLetter =  ['O', 'X']
                        return self.playerLetter, self.computerLetter

        def whoGoesFirst(self):
                # Randomly choose the player who goes first.
                if random.randint(0, 1) == 0:
                        self.turn = 'computer'
                        return self.turn
                else:
                        self.turn = 'player' 
                        return self.turn

	def createBoard(self):
		self.Board = [' '] * 10
	        return self.Board 

	def getBoard(self):
		return self.__theBoard

	def makeMove(self,letter, move):
		self.__theBoard[move] = letter

        def isWinner(self, le):
            # Given a board and a player's letter, this function returns True if that player has won.
            # We use bo instead of board and le instead of letter so we don't have to type as much.

            bo = self.__theBoard

            return ((bo[7] == le and bo[8] == le and bo[9] == le) or # across the top
            (bo[4] == le and bo[5] == le and bo[6] == le) or # across the middle
            (bo[1] == le and bo[2] == le and bo[3] == le) or # across the bottom
            (bo[7] == le and bo[4] == le and bo[1] == le) or # down the left side
            (bo[8] == le and bo[5] == le and bo[2] == le) or # down the middle
            (bo[9] == le and bo[6] == le and bo[3] == le) or # down the right side
            (bo[7] == le and bo[5] == le and bo[3] == le) or # diagonal
            (bo[9] == le and bo[5] == le and bo[1] == le)) # diagonal

        def isTestWinner(self, bo, le):
            # Given a board and a player's letter, this function returns True if that player has won.
            # We use bo instead of board and le instead of letter so we don't have to type as much.
            return ((bo[7] == le and bo[8] == le and bo[9] == le) or # across the top
            (bo[4] == le and bo[5] == le and bo[6] == le) or # across the middle
            (bo[1] == le and bo[2] == le and bo[3] == le) or # across the bottom
            (bo[7] == le and bo[4] == le and bo[1] == le) or # down the left side
            (bo[8] == le and bo[5] == le and bo[2] == le) or # down the middle
            (bo[9] == le and bo[6] == le and bo[3] == le) or # down the right side
            (bo[7] == le and bo[5] == le and bo[3] == le) or # diagonal
            (bo[9] == le and bo[5] == le and bo[1] == le)) # diagonal

        def isBoardFull(self):
            # Return True if every space on the board has been taken. Otherwise return False.

            board = self.__theBoard

            for i in range(1, 10):
                if self.isSpaceFree(board, i):
                    return False
            return True

        def isSpaceFree(self, board, move):
            # Return true if the passed move is free on the passed board.
            return board[move] == ' '
    
        def resetGame(self):
            self.__theBoard = self.createBoard()
            return True

        def getBoardCopy(self):
            # Make a duplicate of the board list and return it the duplicate.
            dupeBoard = []
        
            for i in self.__theBoard:
                dupeBoard.append(i)
        
            return dupeBoard

        def chooseRandomMoveFromList(board, movesList):
            # Returns a valid move from the passed list on the passed board.
            # Returns None if there is no valid move.
            possibleMoves = []
            for i in movesList:
                if isSpaceFree(board, i):
                    possibleMoves.append(i)
        
            if len(possibleMoves) != 0:
                return random.choice(possibleMoves)
            else:
                return None

        def getComputerMove(board, computerLetter):
            # Given a board and the computer's letter, determine where to move and return that move.
            if computerLetter == 'X':
                playerLetter = 'O'
            else:
                playerLetter = 'X'
        
            # Here is our algorithm for our Tic Tac Toe AI:
            # First, check if we can win in the next move
            for i in range(1, 10):
                copy = self.getBoardCopy()
                if self.isSpaceFree(copy, i):
                    self.makeMove(computerLetter, i)
                    if self.isTestWinner(copy, computerLetter):
                        return i
        
            # Check if the player could win on his next move, and block them.
            for i in range(1, 10):
                copy = self.getBoardCopy()
                if self.isSpaceFree(copy, i):
                    self.makeMove(copy, playerLetter, i)
                    if self.isTestWinner(copy, playerLetter):
                        return i
        
            # Try to take one of the corners, if they are free.
            move = self.chooseRandomMoveFromList(self.__theBoard, [1, 3, 7, 9])
            if move != None:
                return move
        
            # Try to take the center, if it is free.
            if self.isSpaceFree(board, 5):
                return 5
        
            # Move on one of the sides.
            return self.chooseRandomMoveFromList(self.theboard, [2, 4, 6, 8])
    





def main(addr="10.1.1.2",port=5000):
	#Cria um servidor XML-RPC no endereço e port definido.
	server = SimpleXMLRPCServer((addr,port))
	#Permite aos clientes fazer introspecção ao servidor
	server.register_introspection_functions()
	#Permite aos clientes fazerem vários pedidos como um só
	server.register_multicall_functions()
	#Regista um objecto Session, o mapeamento dos métodos é automático
	server.register_instance(Session())
	server.register_instance(Tictactoe())
	#Regista a funcão currentTime no servidor com o nome time
	server.register_function(currentTime,"time")
	#Regista a funcão drawBoard no servidor com o nome draw
	#Inicia o servidor XML-RCP em loop infinito
	server.serve_forever()

        # ESTA PARTE DO CODIGO NAO RODA  
        print('Welcome to Tic Tac Toe!')

        while True:
            # Reset the board
            theBoard = [' '] * 10
            playerLetter, computerLetter = inputPlayerLetter()
            turn = whoGoesFirst()
            print('The ' + turn + ' will go first.')
            gameIsPlaying = True

            while gameIsPlaying:
                if turn == 'player':
                    # Player's turn.
                    drawBoard(theBoard)
                    move = getPlayerMove(theBoard)
                    makeMove(theBoard, playerLetter, move)
        
                    if isWinner(theBoard, playerLetter):
                        drawBoard(theBoard)
                        print('Hooray! You have won the game!')
                        gameIsPlaying = False
                    else:
                        if isBoardFull(theBoard):
                            drawBoard(theBoard)
                            print('The game is a tie!')
                            break
                        else:
                            turn = 'computer'
        
                else:
                    # Computer's turn.
                    move = getComputerMove(theBoard, computerLetter)
                    makeMove(theBoard, computerLetter, move)
        
                    if isWinner(theBoard, computerLetter):
                        drawBoard(theBoard)
                        print('The computer has beaten you! You lose.')
                        gameIsPlaying = False
                    else:
                        if isBoardFull(theBoard):
                            drawBoard(theBoard)
                            print('The game is a tie!')
                            break
                        else:
                            turn = 'player'

            if not playAgain():
                break

if __name__ == "__main__":
	main()
