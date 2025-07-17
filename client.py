import sys
import socket
import traceback


host = "example.com"
port = 80


if __name__ == "__main__":
    
    # Usage:
    # client.py [HOST] [PORT]
    
    if(len(sys.argv) > 1):
        host = sys.argv[1]
        if(len(sys.argv) > 2):
            port = int(sys.argv[2])
    
    request = "GET /index.html HTTP/1.1\r\n"
    request += f"Host: {host}\r\n"
    request += "Connection: close\r\n"
    request += "\r\n" # important empty line
    request = request.encode("ISO-8859-1")
    
    try:
        with socket.socket() as s:
            s.connect((host, port))
            print("Connection established.")

            # sendall() is used instead of send()
            # The latter might miss some bytes

            s.sendall(request)
            
            res = b""
            
            while True:
                buff = s.recv(4096)
                if not buff:
                    break
                res += buff

            print(res.decode("ISO-8859-1", errors='replace'))
            
    except:
        print(traceback.format_exc())
    
