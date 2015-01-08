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
		info = self.rfile.read()
        try:
            info1 = info.split(" ")
        except IndexError:
            sys.exit()
        metod = info1[0]
		#Evaluamos segun el metodo recibido
        if metod == "REGISTER":
            fich = open(str(data["path_log"]), "a")
            localtime()
            fich.write("Received from 127.0.0.1" + ": " + info)
            RecibeREGISTER(self, dicc, info1)
        elif metod == "INVITE":
            fich = open(str(data["path_log"]), "a")
            localtime()
            fich.write("Received from 127.0.0.1" + ": " + info)
            RecibeINVITE(self, dicc, info1, info)
        elif metod == "ACK":
            fich = open(str(data["path_log"]), "a")
            localtime()
            fich.write("Received from 127.0.0.1" + ": " + info)
            my_socket.send(info)
        else:
            try:
                fich = open(str(data["path_log"]), "a")
                localtime()
                fich.write("Received from 127.0.0.1" + ": " + info)
                my_socket.send(info)
                localtime()
                fich.write("Sent to 127.0.0.1:" + str(data["puerto_server"])\
 				+ ": " + info)
                Respuesta = my_socket.recv(1024)
                Respuesta = my_socket.recv(1024)
                localtime()
                fich.write("Received from 127.0.0.1" + ": " + info)
                self.wfile.write(Respuesta)
                localtime()
                fich.write("Sent to 127.0.0.1:" + str(data["puerto_server"])\
 				+ ": " + Respuesta)
                fich.close()
            except:
                fich = open(str(data["path_log"]), "a")
                localtime()
                fich.write("Received from 127.0.0.1" + ": " + info)
                self.wfile.write("SIP/2.0 405 Method Not Allowed\r\n")
                fich.write("Sent to 127.0.0.1:" + str(data["puerto_server"])\
 				+ ": " + "SIP/2.0 405 Method Not Allowed\r\n")
                fich.close()

if __name__ == "__main__":
    dicc = {}
    cadena = sys.argv
    if len(cadena) != 2:
        print "Usage: python proxy_registrar.py config"
        sys.exit()
    #Comprobamos los datos
    parser = make_parser()
    cHandler = ReadxmlProxy()
    parser.setContentHandler(cHandler)
    try:
        parser.parse(open(cadena[1]))
    except:
        print "Usage: python proxy_registrar.py config"
        sys.exit()
    #Guardamos los datos
    data = cHandler.get_tags()
    fich = open(str(data["path_log"]), "w")
    localtime()
    fich.write("Starting ...\r\n")
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #Imprimimos los datos
    SERVER = str(data["ip_server"])
    PORT = int(data["puerto_server"])
    serv = SocketServer.UDPServer((SERVER, PORT), EchoHandler)
    print "Server " + str(data["name_server"]) + " listening at port "\
 	+ str(PORT) + "...\r\n"
    try:
        serv.serve_forever()
    except:
        print "Usage: python proxy_registrar.py config"
        sys.exit()   

