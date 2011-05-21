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


from socket import *
import Queue, threading, time

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
