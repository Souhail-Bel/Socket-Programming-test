import sys, os
import socket
import traceback

PATH = "./server/"

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


# Not found response

NOT_FOUND = "HTTP/1.1 404 Not Found\r\n"
NOT_FOUND += "Content-Type: text/plain\r\n"
NOT_FOUND += "Content-Length: 16\r\n"
NOT_FOUND += "Connection: close\r\n"
NOT_FOUND += "404 NOT FOUND :P"
NOT_FOUND = NOT_FOUND.encode("ISO-8859-1")

def make_resp(request: str) -> bytes:
    file_name = request.split('\r\n')[0].split(' ')[1][1:]
    
    # Response setup
    ext = os.path.splitext(file_name)[1]
    
    try:
        with open(PATH + file_name, 'rb') as f:
            msg = f.read()
    except Exception as e:
        print(e)
        return NOT_FOUND
    
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

                request = request.decode("ISO-8859-1", errors='replace')
                # print("REQUEST METHOD: ", request[:10].split(' ')[0])
                # print("REQUEST RECEIVED:")
                # print(request)
                # print("\r\n\r\n") # Visual purpose only
                
                response = make_resp(request)
                
                new_sock.sendall(response)
                print("Successfully responded.")
                
                new_sock.close()
                print("Client socket closed.")
    except:
        print("Server failed!")
        print(traceback.format_exc())
    
