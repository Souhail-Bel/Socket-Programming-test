import sys
import socket

msg = "<h1>Hello there!</h1>"
msg += "<h2>Lorem ipsum, there goes my sockets</h2>"

response = "HTTP/1.1 200 OK\r\n"
response += "Content-Type: text/html\r\n"
response += f"Content-Length: {len(msg)}\r\n"
response += "Connection: close\r\n"
response += "\r\n"
response += msg

response = response.encode("ISO-8859-1")

port = 28333
IP_addr = "192.168.1.144"

if __name__ == "__main__":
    
    # Usage:
    # server.py [PORT]
    
    if(len(sys.argv) > 1):
        port = int(sys.argv[1])
        
    
    try:
        with socket.socket() as s:
            # Prevent "address already in use" error on bind()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # use '' for localhost
            s.bind((IP_addr, port))
            print("Server address: ", IP_addr)
            
            s.listen()
            print(f"Listening on port {port}...")
            
            
            while True:
                new_sock, new_addr = s.accept()
                print("Client: ", new_addr)
                
                request = b""
                
                while True:
                    buff = new_sock.recv(4096)
                    if not buff:
                        break
                    
                    request += buff
                    
                    if b"\r\n\r\n" in request:
                        break

                request = request.decode("ISO-8859-1", errors='replace')
                print("REQUEST METHOD: ", request.split(' ')[0])
                print("REQUEST RECEIVED:")
                print(request)
                
                new_sock.sendall(response)
                print("Successfully responded.")
                
                new_sock.close()
                print("Client socket closed.")
    except Exception as e:
        print("Server failed!")
        print(e)
    
