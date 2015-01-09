#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler

import sys
import SocketServer
import time
import os


class LeerUAxml(ContentHandler):
    #Inicializamos el diccionario
    def __init__(self):
        self.dicc = {}

    #Recogemos los datos
    def startElement(self, name, attrs):
        if name == "account":
            self.dicc["username"] = attrs.get("username", "")
            self.dicc["passwd"] = attrs.get("passwd", "")
        if name == "uaserver":
            self.dicc["ip_server"] = attrs.get("ip", "")
            self.dicc["puerto_server"] = attrs.get("puerto", "")
        if name == "rtpaudio":
            self.dicc["puerto_rtp"] = attrs.get("puerto", "")
        if name == "regproxy":
            self.dicc["ip_proxy"] = attrs.get("ip", "")
            self.dicc["puerto_proxy"] = attrs.get("puerto", "")
        if name == "log":
            self.dicc["path_log"] = attrs.get("path", "")
        if name == "audio":
            self.dicc["path_audio"] = attrs.get("path", "")

    def get_tags(self):
        return self.dicc


class EchoHandler(SocketServer.DatagramRequestHandler):
    def handle(self):
        #Creamos toda la cadena de datos relevantes a partir de lo recogido
        #en el diccionario
        def CreaSDP(data):
            SDP = "Content-Type: application/sdp" + "\r\n" + "\r\n" + "v=0\r\n"
            SDP = SDP + "o=" + str(data["username"]) + " "\
            + str(data["ip_server"]) + "\r\n"
            SDP = SDP + "s=MiSesion" + "\r\n" + "t=0" + "\r\n"
            SDP = SDP + "m=audio " + str(data["puerto_rtp"]) + " RTP"
            return SDP

    #Cuando recibimos peticion de invite enviamos la siguiente info
    def RecibeINVITE(self):
            self.wfile.write("SIP/2.0 100 Trying" + "\r\n")
            self.wfile.write("SIP/2.0 180 Ring" + "\r\n")
            self.wfile.write("SIP/2.0 200 OK" + "\r\n")
            SDP = CreaSDP(data)
            self.wfile.write(SDP + "\r\n")

    #Cuando recibimos peticion de ACK
    def RecibeACK(self):
        Shell = "./mp32rtp -i " + SERVER + " -p " \
        + str(data["puerto_rtp"]) + " < " + str(data["path_audio"])
        print "Vamos a ejecutar para el envio RTP: \r\n " + Shell
        os.system(Shell)
    #Leemos la linea, troceamos hasta encontrar la palabra importante
    #en este caso el SIP y el metodo
        line = self.rfile.read()
        info = line.split("\r\n")
        info1 = info[0].split(" ")
        SIP = info1[2]
        metod = info1[0]
        if SIP == "SIP/2.0":
            if metod == "INVITE":
                RecibeINVITE(self)
            elif metod == "ACK":
                RecibeACK(self)
            elif metod == "BYE":
                self.wfile.write("SIP/2.0 200 OK\r\n")
            else:
                self.wfile.write("SIP/2.0 405 Method Not Allowed\r\n")
        else:
            self.wfile.write("SIP/2.0 400 Bad Request\r\n")
            sys.exit()

if __name__ == "__main__":
    cadena = sys.argv
    infopuerto = []
    if len(cadena) != 2:
        print "Usage: python uaserver.py config"
        sys.exit()
    #Comprobamos los datos
    parser = make_parser()
    cHandler = LeerUAxml()
    parser.setContentHandler(cHandler)
    try:
        parser.parse(open(cadena[1]))
    except:
        print "Usage: python uaserver.py config"
        sys.exit()
    #Guardamos los los datos
    data = cHandler.get_tags()
    SERVER = str(data["ip_server"])
    PORT = int(data["puerto_server"])
    serv = SocketServer.UDPServer((SERVER, PORT), EchoHandler)
    print "Listening...\r\n"
    try:
        serv.serve_forever()
    except:
        print "Usage: python uaserver.py config"
        sys.exit()
