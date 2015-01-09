#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler

import sys
import socket
import time
import os


#Obtenemos el tiempo
def localtime():
    timme = time.strftime("%Y%m%d%H%M%S", time.localtime())
    fich.write(str(timme) + " ")


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


#Creamos toda la cadena de datos relevantes a partir de lo recogido
#en el diccionario
def CreaSDP(data):
    SDP = "Content-Type: application/sdp" + "\r\n" + "\r\n" + "v=0\r\n"
    SDP = SDP + "o=" + str(data["username"]) + " "\
    + str(data["ip_server"]) + "\r\n"
    SDP = SDP + "s=MiSesión" + "\r\n" + "t=0" + "\r\n"
    SDP = SDP + "m=audio " + str(data["puerto_rtp"]) + " RTP"
    return SDP


#Procedimiento cuando recibimos respuesta REGISTER
def RegisterResp(data, fich):
    try:
        Respuesta = my_socket.recv(1024)
        print "Recibido: \r\n" + Respuesta
    except:
        print "Error: no server listening at " + SERVER + " port " + str(PORT)
        localtime()
        #Escribimos en el fichero el report de error no escucha
        fich.write(" Error: no server listening at " + data["ip_server"] \
        + "port " + data["puerto_server"] + "\r\n")
        sys.exit()
        my_socket.close()
    mess = Respuesta.split(" ")
    mess = mess[1]
    if mess == "200":
        localtime()
        #Escribimos en el fichero report de el 200 ok recibido
        fich.write("Received from " + data["ip_proxy"] \
        + str(data["puerto_proxy"]) + ":  200 OK" + "\r\n")
        localtime()
        fich.write("Finishing.\r\n")
        print "Recibido 200 OK"
    fich.close()
    sys.exit()
    my_socket.close()


#Procedimiento cuando recibimos un BYE
def ByeResp(data):
    try:
        Respuesta = my_socket.recv(1024)
    except:
        print "Error: no server listening at " + SERVER + " port " + str(PORT)
        sys.exit()
    mess = Respuesta.split(" ")
    mess = mess[1]
    if mess == "200":
        print "Recibido 200 OK"
    my_socket.close()
    sys.exit()
    my_socket.close()


def InviteResp(data):
    frase = "ACK sip:" + str(data["username"]) + " SIP/2.0"
    try:
        Respuesta = my_socket.recv(1024)
        print "Recibido: " + Respuesta
    except:
        print "Error: no server listening at " + SERVER + " port " + str(PORT)
        localtime()
        fich.write("Error: no server listening at " +\
        str(data["ip_server"]) + "port " + str(data["puerto_server"]) + "\r\n")
        sys.exit()
        my_socket.close()
        fich.close()
    if Respuesta == "SIP/2.0 404 User Not Found\r\n":
        print "llego"
        localtime()
        fich.write("Error: User not found " + str(data["ip_server"])\
        + "port " + str(data["puerto_server"]) + "\r\n")
        my_socket.close()
        fich.close()
        sys.exit()
    Respuesta = Respuesta.split("\r\n")
    for i in Respuesta:
        mess = i.split(" ")
        mess = mess[1]
        if mess == "200":
            localtime()
            fich.write("Received from " + data["ip_proxy"]\
            + str(data["puerto_proxy"]) \
            + ":  100 trying, 180 ring y 200 OK" + "\r\n")
            print "Enviamos ACK de la forma: " + frase
            localtime()
            fich.write("Sent to" + str(data["ip_proxy"]) + ":" \
            + str(data["puerto_proxy"]) + ": ACK " + str(data["username"])\
            + ":" + str(data["puerto_server"]) + " SIP/2.0" + "\r\n")
            my_socket.send(frase + "\r\n")
            infoPuerto = Respuesta[-1].split(" ")
            Shell = "./mp32rtp -i " + SERVER + " -p "\
            + data["puerto_rtp"] + " < " + str(data["path_audio"])
            print "Vamos a ejecutar para el envio RTP: \r\n " + Shell
            os.system(Shell)
            break
    sys.exit()

if __name__ == "__main__":
    cadena = sys.argv
    if len(cadena) < 4 or len(cadena) > 5:
        print "Usage: python uaclient.py config method option"
        sys.exit()
    # comprobamos los datos
    parser = make_parser()
    cHandler = LeerUAxml()
    parser.setContentHandler(cHandler)
    try:
        parser.parse(open(cadena[1]))
    except:
        print "Usage: python uaclient.py config method option"
        my_socket.close()
        sys.exit()
    #guardo los datos
    data = cHandler.get_tags()
    #Me conecto a el Server
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    SERVER = str(data["ip_proxy"])
    PORT = int(data["puerto_proxy"])
    try:
        my_socket.connect((SERVER, PORT))
    except:
        print("Usage: python cliente.py method receiver@IP:SIPport")
        my_socket.close()
        sys.exit()
    if cadena[2] == "REGISTER":
        frase = "REGISTER sip:" + str(data["username"])\
         + ":" + str(data["puerto_server"]) + " SIP/2.0" + "\r\n" \
        + "Expires: " + str(cadena[3])
        print frase
        #Creamos el txt:
        if str(cadena[3]) == "0":
            fich = open(str(data["path_log"]), "a")
        else:
            fich = open(str(data["path_log"]), "w")
            localtime()
            fich.write("Starting ...\r\n")
            localtime()
            fich.write("Sent to" + data["ip_proxy"] + ":" \
            + str(data["puerto_proxy"]) + ": REGISTER " + data["username"] \
            + ":" + data["puerto_server"] + " SIP/2.0" + "\r\n")
            my_socket.send(frase + "\r\n")
            RegisterResp(data, fich)
        #print "Enviando REGISTER de la forma:\r\n \r\n" + frase + "\r\n"
        #my_socket.send(frase + '\r\n')
    elif cadena[2] == "INVITE":
        fich = open(str(data["path_log"]), "a")
        frase = "INVITE sip:" + str(cadena[3]) + " SIP/2.0" + "\r\n"
        SDP = CrearSDP(data)
        frase = frase + SDP
        localtime()
        fich.write("Sent to " + str(data["ip_proxy"]) + ":"\
         + str(data["puerto_proxy"]) + ": INVITE " + str(cadena[3]) + "\r\n")
        my_socket.send(frase)
        InviteResp(data, fich)
        #print "Enviando REGISTER de la forma:\r\n \r\n" + frase + "\r\n"
        #my_socket.send(frase + '\r\n')
    elif cadena[2] == "BYE":
        fich = open(str(data["path_log"]), "a")
        frase = "BYE sip:" + str(cadena[3]) + " SIP/2.0" + "\r\n"
        my_socket.send(frase)
        localtime()
        fich.write("Sent to " + data["ip_proxy"] + ":"\
         + data["puerto_proxy"] + ": BYE " + str(cadena[3]) + "\r\n")
        try:
            Respuesta = my_socket.recv(1024)
            print "Recibido:" + Respuesta
            localtime()
            fich.write("Received from " + data["ip_proxy"]\
             + str(data["puerto_proxy"]) + ":  200 OK" + "\r\n")
        except:
            print "Error: no server listening at " + SERVER + \
            " port " + str(PORT)
            localtime()
            fich.write("Error: no server listening at " + \
            str(data["ip_server"]) + "port "\
            + str(data["puerto_server"]) + "\r\n")
            fich.close()
            my_socket.close()
            sys.exit()
    else:
        fich = open(str(data["path_log"]), "a")
        frase = str(cadena[2]) + " sip:" + str(cadena[3]) + " SIP/2.0" + "\r\n"
        my_socket.send(frase)
        try:
            Respuesta = my_socket.recv(1024)
            print "Recibido:" + Respuesta
            localtime()
            fich.write("Received from " + data["ip_proxy"]\
             + str(data["puerto_proxy"]) + ": " + str(Respuesta) + "\r\n")
        except:
            print "Error: no server listening at " + SERVER\
             + " port " + str(PORT)
            localtime()
            fich.write("Error: no server listening at " + \
            str(data["ip_server"]) + "port "\
            + str(data["puerto_server"]) + "\r\n")
            my_socket.close()
            sys.exit()
