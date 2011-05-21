#-------------------------------------------------------------------------------
# Name:        client.py
# Purpose:     Cliente para uma aplicação cliente servidor de troca de mensagens
# instantâneas.
#
# Author:      Isaac Mechi
#
# Created:     15/11/2010
# Copyright:   (c) Isaac Mechi
# Licence:     <GPL>
# Passo 3 (Equipe)
# Desenvolva o segundo módulo denominado com Cliente, o qual deve apresentar:
# a) Processo identificação do outro jogador (Servidor);
# b) Processo de quando o jogador pode realizar sua jogada. Vale lembrar que esse
# processo é alternado, ou seja, um jogador de cada vez.
#-------------------------------------------------------------------------------
#!/usr/bin/env python
# -*- encoding: utf8 -*-
from socket import *
import sys, time, threading

# Nosso mainloop.
# Definido método main() para que o script fique mais familiar aos que
# já o conhecem de outras linguagem, tornando a leitura familiar.
def main():
    # Especifica servidor e porta para comunição.
    ip = "localhost"
    porta = 5000

    # Cria e instância um socket familia IPv4 utilizando protocolo TCP
    sock = socket(AF_INET,SOCK_STREAM)
    # Realiza conexão
    sock.connect((ip,porta))

    # Criado estrutura para escolha de login e confirmação de servidor,
    # caso haja algum problema na comunicação, possamos identificar logo no
    # início.

    # método raw lê uma string do teclado e a retorna, aceita uma string
    # como argumento, para interação com usuário.
    msg = raw_input("Digite Seu Nome: ")
    print
    print "Nome: %s" %msg
    msg = "HELLO %s\n" %msg
    # Esta sequência envia a mensagem, e logo após espera ate receber a uma
    # mensagem de resposta.
    sock.send(msg)
    msg = sock.recv(64)
    print msg

    # Cria e instância um objeto da classe Monitor(), passando como atributos
    # o socket de comunicação, e "True", utilizado para iniciar ou parar o
    # loop da thread Monitor
    monitor = Monitor(sock,True)

    # Se o servidor aceitar nosso pedido com um "OK\n", iniciamos o Monitor.
    # Se não retornamos um aviso e encerramos a aplicação.
    if msg == "OK\n":
        monitor.start()
    else:
        print "Falha Na Comunicacao!"
        print "encerrando cliente..."
        sys.exit()

    # Aqui esta o coração do mainloop, neste trecho enviamos as mensagens para
    # o servidor, mas só escutamos atravéz do método Monitor.
    while True:
        # método raw lê uma string do teclado e a retorna, aceita uma string
        # como argumento, para interaçãoo com usuário.
        msg = raw_input("Digite Sua Mensagem: ")
        print
        # Quebra de mainloop, checamos de usuário quer sair, se sim, enviamos
        # uma mensagem ao objeto monitor, instância da classe Monitor, parando
        # seu loop. Quebramos o while com um break, provocando o fim da aplicação.
        if msg == "SAIR" or msg == "sair":
            print "encerrando cliente..."
            monitor.conectado = False
            break
        msg = "MSG %s\n" %msg
        sock.send(msg)
        # Utilizado para sincronia entre enviar uma mensagem e receber mensagens.
        time.sleep(1)

    # Com o fim do mainloop, enviamos ao servidor pedido para desconectar,
    # aguardamos alguma mensagem, e encerramos o programa.
    sock.send("SAIR\n")
    msg = sock.recv(64)
    print msg
    sock.close()
    # Utilizado para feedback das mensagem de encerramento.
    time.sleep(5)
    sys.exit()

# Classe que monitora mensagem recebidos do servidor de comunicação. Básicamento
# só escuta e mostra mensagem na tela.
# Utiliza dos atributos: sock que um obeto socket, e conectado que é um
# interruptor paro o método run().
class Monitor(threading.Thread):
    def __init__(self,sock,conectado):
        threading.Thread.__init__(self)
        self.sock = sock
        self.conectado = conectado
        print "Iniciando Monitor()..."

    def run(self):
        while self.conectado:
            time.sleep(0.5)
            self.msg = self.sock.recv(64)
            print
            print self.msg
            print
        print "Encerrando Monitor()..."

# Utilizado para configurar, iniciar o método main.
if __name__ == '__main__':
    main()
