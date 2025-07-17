import sys, os
import socket
import traceback

MIME = {
    ".txt"  : "text/plain",
    ".html" : "text/html",
    ".htm"  : "test/html",
    ".pdf"  : "application/pdf",
    ".xml"  : "application/xml",
    ".gif"  : "image/gif",
    ".bmp"  : "image/bmp",
    ".jpeg" : "image/jpeg"
}

def make_resp(request: bytes) -> bytes:
    file_name = request.split('\r\n')[0].split(' ')[1]
    
    # Response setup
    ext = os.path.splitext(file_name)[1]
    
    try:
        with open(file_name, 'rb') as f:
            msg = f.read()
    except:
        return "HTTP/1.1 404 NOT FOUND\r\n"
    
    response = "HTTP/1.1 200 OK\r\n"
    response += f"Content-Type: {MIME.get(ext, 'application/octet-stream')}\r\n"
    response += f"Content-Length: {len(msg)}\r\n"
    response += "Connection: close\r\n"
    response += "\r\n"
    
    
    response = response.encode("ISO-8859-1")
    response += msg
    
    return response

PORT = 28333
IP_addr = "192.168.1.144"

if __name__ == "__main__":
    
    
    
    # Usage:
    # server.py [PORT]
    
    if(len(sys.argv) > 1):
        PORT = int(sys.argv[1])
        
    
    try:
        with socket.socket() as s:
            # Prevent "address already in use" error on bind()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # use '' for localhost
            s.bind((IP_addr, PORT))
            print("Server address: ", IP_addr)
            
            s.listen()
            print(f"Listening on PORT {PORT}...")
            
            
            while True:
                new_sock, new_addr = s.accept()
                print("Client: ", new_addr)
                
                # Request reciver
                
                request = b""
                
                while True:
                    buff = new_sock.recv(4096)
                    if not buff:
                        break
                    
                    request += buff
                    
                    if b"\r\n\r\n" in request:
                        break

                requestDECODED = request.decode("ISO-8859-1", errors='replace')
                print("REQUEST METHOD: ", requestDECODED[:10].split(' ')[0])
                print("REQUEST RECEIVED:")
                print(requestDECODED)
                print("\r\n\r\n") # Visual purpose only
                
                response = make_resp(request)
                
                new_sock.sendall(response)
                print("Successfully responded.")
                
                new_sock.close()
                print("Client socket closed.")
    except:
        print("Server failed!")
        print(traceback.format_exec())
    
