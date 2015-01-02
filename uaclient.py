#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler

import sys
import socket
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

	#Obtenemos el tiempo
	def localtime():
    timme = time.strftime("%Y%m%d%H%M%S", time.localtime())
    fich.write(str(timme) + " ")

	#Creamos toda la cadena de datos relevantes a partir de lo recogido
	#en el diccionario
	def CreaSDP(data):
	    SDP = "Content-Type: application/sdp" + "\r\n" + "\r\n" + "v=0\r\n"
	    SDP = SDP + "o=" + str(data["username"]) + " " + str(data["ip_server"]) + "\r\n"
	    SDP = SDP + "s=MiSesión" + "\r\n" + "t=0" + "\r\n"
	    SDP = SDP + "m=audio " + str(data["puerto_rtp"]) + " RTP"
	    return SDP
	
    try:
        my_socket.connect((SERVER, PORT))
    except:
        print("Usage: python cliente.py method receiver@IP:SIPport")
        my_socket.close()
        sys.exit()
