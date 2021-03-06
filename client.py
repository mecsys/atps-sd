#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import xmlrpclib
from datetime import datetime

# Cria uma ligacao ao servidor XML-RPC

server = xmlrpclib.ServerProxy("http://127.0.0.1:5000/", allow_none=True)

# Tic Tac Toe

def drawBoard():
    # This function prints out the board that it was passed.

    # "board" is a list of 10 strings representing the board (ignore index 0)
    aux = int(server.getPartida())
    if ( aux  == 3):
        return
    else:
        print('Partida Nr %d' % (aux + 1))
        board =  server.drawBoard()
        print('   |   |')
        print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
        print('   |   |')

def inputPlayerLetter():
    # Let's the player type which letter they want to be.
    # Returns a list with the player's letter as the first item, and the computer's letter as the second.
    letter = ''
    while not (letter == 'X' or letter == 'O'):
        print('Voce Deseja Ser X ou O?')
        letter = raw_input().upper()

    # the first element in the tuple is the player's letter, the second is the computer's letter.
    return server.setPlayersLetter(letter)

def whoGoesFirst():
    # Randomly choose the player who goes first.
    return server.whoGoesFirst()

def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    drawBoard()
    server.resetGame()
    print('Voce Deseja Jogar Novamente? (sim ou nao)')
    return raw_input().lower().startswith('s')

def makeMove(letter, move):
    #board[move] = letter
    
    # Tratamento de erro (Marshalling error).
    # Ainda nao sei ao certo qual erro esta tratando,
    # retirado de um exemplo do pydoc 2.7
    try:
        server.makeMove(letter, move)
    except xmlrpclib.Fault, err:
#        print "Uma falha ocorreu"
#        print "Falha erro: %d" % err.faultCode
#        print "Falha string: %s" % err.faultString
        pass

def isWinner(le):
    # Given a board and a player's letter, this function returns True if that player has won.
    # We use bo instead of board and le instead of letter so we don't have to type as much.
        aux = server.isWinner(le)
        return aux

def getBoardCopy(board):
    # Make a duplicate of the board list and return it the duplicate.
    dupeBoard = []

    for i in board:
        dupeBoard.append(i)

    return dupeBoard

def isSpaceFree(board, move):
    # Return true if the passed move is free on the passed board.
    return board[move] == ' '

def getPlayerMove():
    # Let the player type in his move.
    move = ' '
    board = server.drawBoard()

    while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
        print('Qual seu proximo movimento? (1-9)')
        move = raw_input()
    return int(move)

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

def getComputerMove():
    # Given a board and the computer's letter, determine where to move and return that move.
    return server.getComputerMove()


def isBoardFull():
    # Return True if every space on the board has been taken. Otherwise return False.
    return server.isBoardFull()

def main():
        print('Bem-Vindo Ao Jogo Da Velha!')
        print("") 
        while True:
            # Reset the board
	    theBoard = []
	    theBoard = server.getBoard()
            playerLetter, computerLetter = inputPlayerLetter()
            turn = server.whoGoesFirst()
            print('O ' + turn + ' joga primeiro.')
            gameIsPlaying = True
        
            while gameIsPlaying:
                if turn == 'player':
                    # Player's turn.
                    print("")
                    drawBoard()
                    print(server.getMsg())
                    move = getPlayerMove()
                    makeMove(playerLetter, move)
        
                    if isWinner(playerLetter):
                        drawBoard()
                        print('Muiti Bom! Voce Ganhou O Jogo!')
                        gameIsPlaying = False
                    else:
                        if isBoardFull():
                            drawBoard()
                            print('O Jogo Empatou!')
                            break
                        else:
                            turn = 'computer'
        
                else:
                   # Computer's turn.
                   move = getComputerMove()
                   makeMove(computerLetter, move)
        
                   if isWinner(computerLetter):
                       drawBoard()
                       print('O Computador Bateu Voce! Voce Perdeu.')
                       gameIsPlaying = False
                   else:
                       if isBoardFull():
                          drawBoard()
                          print('O Jogo Empatou!')
                          break
                       else:
                          turn = 'player'
        
            if not playAgain():
                break

if __name__ == "__main__":
        main()
	#Envia uma sequência de pedidos um a um
	#pedidoSimples(theBoard)
	#Envia uma sequência de pedidos como um só
	#pedidoMultiCall()
