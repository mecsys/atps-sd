# -*- coding: UTF-8 -*-
import xmlrpclib
from datetime import datetime

#Cria uma ligação ao servidor XML-RCP
server = xmlrpclib.ServerProxy("http://localhost:5000/")

def pedidoSimples():
	#Pede ao servidor que execute o procedimento time
	print server.time()
	#Pede ao servidor que liste todos os procedimentos disponíveis
	print server.system.listMethods()
	#Retorna o pydoc associado ao método
	print server.system.methodHelp("time")
	#Envia os dados para o método junto com o pedido
	print server.register("magician","123")
	print server.login("magician","123")
	print server.logout("magician")

def pedidoMultiCall():
	#Gera um pedido MultiCall
	multirequest = xmlrpclib.MultiCall(server)
	#Adiciona ao pedido multi call os pedidos pretendidos
	multirequest.time()
	multirequest.register("magician","123")
	multirequest.login("magician","123")
	#Faz o pedido e aguarda a resposta que é um gerador
	result = multirequest()
	#Um a um extrai os dados da resposta do gerador
	for resp in result:
		print resp

if __name__ == "__main__":
	#Envia uma sequência de pedidos um a um
	pedidoSimples()
	#Envia uma sequência de pedidos como um só
	pedidoMultiCall()

