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

class EchoHandler(SocketServer.DatagramRequestHandler):

    def handle(self):
		#Creamos toda la cadena de datos relevantes a partir de lo recogido
		#en el diccionario
        def CreaSDP(data):
            SDP = "Content-Type: application/sdp" + "\r\n" + "\r\n" + "v=0\r\n"
            SDP = SDP  + "o=" +str(data["username"]) + " " + str(data["ip_server"]) + "\r\n"
            SDP = SDP + "s=MiSesion" + "\r\n" + "t=0" + "\r\n"
            SDP = SDP + "m=audio " + str(data["puerto_rtp"]) + " RTP"
            return SDP
		#Cuando recibimos un invite enviamos la siguiente info
		def RecibeINVITE(self):
            self.wfile.write("SIP/2.0 100 Trying" + "\r\n")
            self.wfile.write("SIP/2.0 180 Ring" + "\r\n")
            self.wfile.write("SIP/2.0 200 OK" + "\r\n")
            SDP = CreaSDP(data)
            self.wfile.write(SDP + "\r\n")


if __name__ == "__main__":
    cadena = sys.argv
#data: cadena de texto!!!!
#if len(entrada) != 4:
		#print "Usage: python uaserver.py "
		#sys.exit()
#	else:
	print "Listening..."
	SERVER = str(data["ip_server"])
    PORT = int(data["puerto_server"])
    serv = SocketServer.UDPServer((SERVER, PORT), EchoHandler)
    try:
        serv.serve_forever()
	except:
        print "Usage: python uaserver.py config"
        sys.exit()
