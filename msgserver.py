# Author:      Di?genes Ternero RA: 0800006
# Author:      Isaac Mechi  RA: 0813506479
# Author:      Fausto Vieira Ferreira RA: 0808160863
# Author:      Rafael Jos? dos Santos   RA: 0834851
#!/usr/bin/python
# -*- encoding: utf8 -*-
# servidor echo
#
# esse codigo implementa um servidor echo: toda mensagem enviada pelo
# cliente deve ser retornada.
#
# Protocolo:
# - se a mensagem for 'sair', o servidor mata a conex?o e o cliente termina
# - se a mensagem for 'desligar', o servidor terminar? e o cliente tamb?m
#
# Passo 2 (Equipe)
# Desenvolva o módulo denominado com Servidor. Esse módulo deve apresentar algumas
# funcionalidades, como:
# a) Processo que aguarda a comunicação do outro processo (Jogador);
# b) Processo que controla o início de cada jogo (Rodada), lembrando que o jogo é
# formado por três rodadas;
# c) Processo de quando o jogador pode realizar sua jogada. Vale lembrar que esse
# processo é alternado, ou seja, um jogador de cada vez;
# d) Processo de verificação do jogo para apresentar quem ganhou ou se deu empate
# (ou “deu velha”);
# e) Processo de reinicializar o jogo com o mesmo jogador ou com outro jogador.



from socket import *
import Queue, threading, time, random

class Serve(threading.Thread):
    def __init__(self,sock_cliente,cliente):
        threading.Thread.__init__(self)
        self.sock_cliente = sock_cliente
        self.cliente = cliente

    def run(self):
        global filaCliente
        conectado = False

        msg = self.sock_cliente.recv(64)
        x = msg.split(None,1)
        nomeCliente = x[1]

        if x[0] == "HELLO":
            conectado = True
            print "%s se conectou!" %nomeCliente.strip()
            msg = "OK\n"
            self.sock_cliente.send(msg)
        else:
            self.cliente.send("erro no protocolo")
            self.sock_cliente.close()

        while conectado:
            msg = self.sock_cliente.recv(64)
            x = msg.split(None,1)
            if len(msg) < 1:
                print "Mensagem recebida vazia. Cliente saiu sem avisar, fechando."
            else:
                if x[0] == "MSG":
                    print "Enviando mensagem de "+nomeCliente
                    msg = nomeCliente.strip()+" "+ x[1].strip()
                    filaCliente.put(msg)

                if msg == "SAIR\n":
                    print nomeCliente+" -> %s:%d desconectou" % (self.cliente[0], self.cliente[1])
                    # fecha a conex?o no socket do cliente e sai do 'while conectado'
                    self.sock_cliente.close()
                    conectado = False

class Monitor(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)

        def run(self):
            global tGlobal
            global filaCliente

            while True:
                time.sleep(1)
                msg = filaCliente.get()
                listaThread = threading.enumerate()

                for T in listaThread:
                    if isinstance(T,Serve):
                        T.sock_cliente.send(msg)


ip = "" # IP do servidor. String vazia significa ouvir em todas as interfaces
porta = 5000 # porta que o servidor ficar? ouvindo

sock = socket(AF_INET, SOCK_STREAM) # cria um socket TCP
sock.bind((ip, porta)) # reserver o IP e porta no sistema operacional

print "MSGSERVER ouvindo na porta %d..." % porta

sock.listen(5) # come?a a ouvir e aguardar por conex?es

filaCliente = Queue.Queue(100) # fila de mensagem de clientes

Monitor().start()
servidor = True
while servidor:
        # o servidor fica parado aqui, aguardando por uma conex?o de um cliente
        sock_cliente, cliente = sock.accept()
        # quando uma conex?o chega, o m?todo accept() retorna um objeto 'socket' que
        # aponta para conex?o com o cliente e uma lista com o IP e porta do cliente
        print "IP:porta do cliente: %s:%d" % (cliente[0], cliente[1])
        Serve(sock_cliente,cliente).start()

# Tic Tac Toe

import random

def drawBoard(board):
    # This function prints out the board that it was passed.

    # "board" is a list of 10 strings representing the board (ignore index 0)
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
        print('Do you want to be X or O?')
        letter = input().upper()

    # the first element in the tuple is the player's letter, the second is the computer's letter.
    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

def whoGoesFirst():
    # Randomly choose the player who goes first.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

def makeMove(board, letter, move):
    board[move] = letter

def isWinner(bo, le):
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

def getBoardCopy(board):
    # Make a duplicate of the board list and return it the duplicate.
    dupeBoard = []

    for i in board:
        dupeBoard.append(i)

    return dupeBoard

def isSpaceFree(board, move):
    # Return true if the passed move is free on the passed board.
    return board[move] == ' '

def getPlayerMove(board):
    # Let the player type in his move.
    move = ' '
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
        print('What is your next move? (1-9)')
        move = input()
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

def getComputerMove(board, computerLetter):
    # Given a board and the computer's letter, determine where to move and return that move.
    if computerLetter == 'X':
        playerLetter = 'O'
    else:
        playerLetter = 'X'

    # Here is our algorithm for our Tic Tac Toe AI:
    # First, check if we can win in the next move
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, computerLetter, i)
            if isWinner(copy, computerLetter):
                return i

    # Check if the player could win on his next move, and block them.
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, playerLetter, i)
            if isWinner(copy, playerLetter):
                return i

    # Try to take one of the corners, if they are free.
    move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if move != None:
        return move

    # Try to take the center, if it is free.
    if isSpaceFree(board, 5):
        return 5

    # Move on one of the sides.
    return chooseRandomMoveFromList(board, [2, 4, 6, 8])

def isBoardFull(board):
    # Return True if every space on the board has been taken. Otherwise return False.
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True


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
