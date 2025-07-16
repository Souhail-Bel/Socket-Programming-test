import sys
import socket


host = "example.com"
port = 80


if __name__ == "__main__":
    
    # Usage:
    # client.py [HOST] [PORT]
    
    if(len(sys.argv) > 1):
        host = sys.argv[1]
        if(len(sys.argv) > 2):
            port = int(sys.argv[2])
    
    request = "GET / HTTP/1.1\r\n"
    request += f"Host: {host}\r\n"
    request += "Connection: close\r\n"
    request += "\r\n" # important empty line
    request = request.encode("ISO-8859-1")
    
    
    s = socket.socket()
    
    s.connect((host, port))
    
    # sendall() is used instead of send()
    # The latter might miss some bytes
    
    s.sendall(request)
    res = s.recv(4096).decode("ISO-8859-1")
    
    print(res)
    
    s.close()
