#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler

import time
import sys
import socket
import SocketServer

#Obtenemos el tiempo
def localtime():
    timme = time.strftime("%Y%m%d%H%M%S", time.localtime())
    fich.write(str(timme) + " ")

class LeerxmlProxy(ContentHandler):
	#Inicializamos el diccionario
    def __init__(self):
        self.dicc = {}
	#Recogemos los datos
    def startElement(self, name, attrs):
        if name == "server":
            self.dicc["name_server"] = attrs.get("name", "")
            self.dicc["ip_server"] = attrs.get("ip", "")
            self.dicc["puerto_server"] = attrs.get("puerto", "")
        if name == "database":
            self.dicc["path_database"] = attrs.get("path", "")
            self.dicc["passwdpath_database"] = attrs.get("passwdpath", "")
        if name == "log":
            self.dicc["path_log"] = attrs.get("path", "")

    def get_tags(self):
        return self.dicc

class EchoHandler(SocketServer.DatagramRequestHandler):

    def handle(self):
		#Proceso de register en proxy
        def RecibeREGISTER(self, dicc, info):
            separar = info[1].split(":")
            dicc[str(separar[1])] = int(separar[2])
            fich = open(str(data["path_log"]), "a")
            self.wfile.write("SIP/2.0 200 OK\r\n")
            localtime()
            fich.write("Sent to" + data["ip_server"] + ":" +\
 			str(data["puerto_server"]) + ": REGISTER " + str(separar[1])\
			+ ":" + data["puerto_server"] + " SIP/2.0" + "\r\n")
        #Proceso de Invite en proxy
        def RecibeINVITE(self, dicc, info1, info):
            separar = info1[1].split(":")
            my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            SERVER = "127.0.0.1"
            if str(separar[1]) in dicc:
                PORT = dicc[str(separar[1])]
                my_socket.connect((SERVER, PORT))
                my_socket.send(str(info))
                fich.write("Sent to 127.0.0.1:" + str(data["puerto_server"])\
 				+ ": INVITE " + str(separar[1]) + " SIP/2.0" + "\r\n")
            else:
                self.wfile.write("SIP/2.0 404 User Not Found\r\n")
                fich.write("Sent to 127.0.0.1:" + str(data["puerto_server"])\
 				+ ": " + "SIP/2.0 400 Bad Request\r\n")
                fich.close()
            try:
                Respuesta = my_socket.recv(1024)
                self.wfile.write(Respuesta)
            except:
                self.wfile.write("SIP/2.0 404 User Not Found\r\n")
                fich.write("Sent to 127.0.0.1:" + str(data["puerto_server"])\
 				+ ": " + "SIP/2.0 400 Bad Request\r\n")
                fich.close()
                sys.exit()    

