#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from SimpleXMLRPCServer import SimpleXMLRPCServer
from time import strftime
import random

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
                Tictactoe.playerWin = 0
                Tictactoe.computerWin = 0
                print "Tic Tac Toe - Classe instanciada."

        def drawBoard(self):             
                """
                Retorna o tabuleiro para o cliente printar
                na tela.
                A lista theBoard contem 10 unidades (ignoramos indice 0).
                """
                return self.__theBoard

        def setPlayersLetter(self, letter):
                """
                O jogador escolhe com qual letra jogar, e retorna
                uma lista com a letra do jogador como primeiro item,
                e como segundo item a letra do computador.
                """
                if letter == 'X':
                        self.playerLetter, self.computerLetter = ['X', 'O']
                        return self.playerLetter, self.computerLetter
                else:
                        self.playerLetter, self.computerLetter =  ['O', 'X']
                        return self.playerLetter, self.computerLetter

        def whoGoesFirst(self):
                """
                Escolha aleatoriamente quem comeca primeiro.
                """
                if random.randint(0, 1) == 0:
                        self.turn = 'computer'
                        return self.turn
                else:
                        self.turn = 'player' 
                        return self.turn

	def createBoard(self):
                """
                Cria um tabuleiro (lista), e a retorna.
                """
		self.Board = [' '] * 10
	        return self.Board 

	def getBoard(self):
                """
                Retorna o tabuleiro (lista) principal que fica
                armazenado no servidor.
                """
		return self.__theBoard

	def makeMove(self,letter, move):
                """
                Executa o movimento dos jogadores na tabuleiro (lista)
                principal, que fica armazenado no servidor.
                """
		self.__theBoard[move] = letter

	def makeTestMove(self, board, letter, move):
                """
                Executa o movimento dos jogadores em uma copia do 
                tabuleiro (lista) principal, que fica armazenado no servidor.
                Metodo para funcionamento da IA (Inteligencia Artificial)
                que o servidor executa para atacar e se defender.
                """
		board[move] = letter

        def isWinner(self, le):
                """
                Checa em todas a 8 possibilidades de vitorio se algum jogador
                ganhou o jogo e retorna positivo (True) se sim, e nao (None)
                do contrario.
                """

                # Aponta (bo) para o tabuleiro (lista) principal.
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
                """
                Utiliza uma copia (bo) do tabuleiro (lista) principal, que esta
                armazenado no servidor, para checar todas a 8 possibilidades
                de vitoria. Se algum jogador ganhou o jogo retorna 
                positivo (True) e nao (None) do contrario.
                """
                return ((bo[7] == le and bo[8] == le and bo[9] == le) or # across the top
                (bo[4] == le and bo[5] == le and bo[6] == le) or # across the middle
                (bo[1] == le and bo[2] == le and bo[3] == le) or # across the bottom
                (bo[7] == le and bo[4] == le and bo[1] == le) or # down the left side
                (bo[8] == le and bo[5] == le and bo[2] == le) or # down the middle
                (bo[9] == le and bo[6] == le and bo[3] == le) or # down the right side
                (bo[7] == le and bo[5] == le and bo[3] == le) or # diagonal
                (bo[9] == le and bo[5] == le and bo[1] == le)) # diagonal

        def isBoardFull(self):
                """
                Checa se tabuleiro (lista) esta cheio. Indice de 1 ao 9, 
                indice 0 é ignorado.
                Retorna verdade (True) se ha algun espaco em branco no
                tabuleiro (lista).
                """
                board = self.__theBoard

                for i in range(1, 10):
                        if self.isSpaceFree(board, i):
                                return False
                return True

        def isSpaceFree(self, board, move):
                """
                Retorna verdade (True) se o movimento passado estiver livre
                no tabuleiro (lista) passado.
                """
                return board[move] == ' '
    
        def resetGame(self):
                """
                Reinicia o tabuleiro (lista) para iniciar um novo jogo.
                """
                self.__theBoard = self.createBoard()
                return True

        def getBoardCopy(self):
                """
                Faz uma copia do tabuleiro (lista) e a retorna.
                """
                dupeBoard = []
        
                for i in self.__theBoard:
                        dupeBoard.append(i)
        
                return dupeBoard

        def chooseRandomMoveFromList(self, board, movesList):
                """
                Retorna um movimento valido para o tabuleiro passado (lista).
                Retorna nao (None) se houver movimento valido.
                """
                possibleMoves = []
                for i in movesList:
                        if self.isSpaceFree(board, i):
                                possibleMoves.append(i)
        
                if len(possibleMoves) != 0:
                        return random.choice(possibleMoves)
                else:
                        return None

        def getComputerMove(self):
                """
                Determina onde o computador devera jogar.
                Utiliza um simples algoritmo de IA (Inteligencia Artificial)
                para escolher o melhor movimento, tanto no ataque,
                quanto na defesa.
                """
        
                # Aqui esta o algoritmo para nosso jogo da Velha AI:
                # Primeiro, checa se pode ganhar no proximo movimento, e vence. 
                for i in range(1, 10):
                        copy = self.getBoardCopy()
                        if self.isSpaceFree(copy, i):
                                self.makeTestMove(copy, self.computerLetter, i)
                                if self.isTestWinner(copy, self.computerLetter):
                                        return i
            
                # Checa se o jogador podera ganhar no seu proximo movimento, e
                # bloqueia ele.
                for i in range(1, 10):
                        copy = self.getBoardCopy()
                        if self.isSpaceFree(copy, i):
                                self.makeTestMove(copy, self.playerLetter, i)
                                if self.isTestWinner(copy, self.playerLetter):
                                        return i
        
                # Tenta obter um dos cantos, se estiverem livres.
                move = self.chooseRandomMoveFromList(self.__theBoard, [1, 3, 7, 9])
                if move != None:
                        return move
        
                # Tenta obter o centro, se estiver livre.
                if self.isSpaceFree(self.__theBoard, 5):
                        return 5
        
                # Move em um dos lados.
                return self.chooseRandomMoveFromList(self.__theboard, [2, 4, 6, 8])

def main(addr="127.0.0.1",port=5000):
        """
        Funcao pricipal do modulo Servidor. Inicializa o 
        XML-RPC, habilita a interacao do cliente e registra 
        o objeto jogo da Velha, para que o cliente possa invoca-lo.
        """
	#Cria um servidor XML-RPC no endereço e port definido.
	server = SimpleXMLRPCServer((addr,port))
	#Permite aos clientes fazer introspecção ao servidor
	server.register_introspection_functions()
	#Permite aos clientes fazerem vários pedidos como um só
	server.register_multicall_functions()
	#Regista um objecto Session, o mapeamento dos métodos é automático
	server.register_instance(Tictactoe())
	#Inicia o servidor XML-RCP em loop infinito
	server.serve_forever()

if __name__ == "__main__":
	main()
