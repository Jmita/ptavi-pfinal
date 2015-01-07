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


