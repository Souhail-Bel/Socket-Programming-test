import sys
import socket

msg = "10-4, networking is awesome."

response = "HTTP/1.1 200 OK\r\n"
response += "Content-Type: text/plain\r\n"
response += f"Content-Length: {len(msg)}\r\n"
response += "Connection: close\r\n"
response += "\r\n"
response += msg

response = response.encode("ISO-8859-1")

port = 28333

if __name__ == "__main__":
    
    # Usage:
    # server.py [PORT]
    
    if(len(sys.argv) > 1):
        port = sys.argv[1]
        
        
    s = socket.socket()
    
    # Prevent address already in use error on bind()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    s.bind(('', port))
    
    s.listen()
    
    new_conn = s.accept()
    new_sock = new_conn[0]
    
    s.close()
    