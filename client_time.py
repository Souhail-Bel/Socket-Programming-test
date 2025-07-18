import sys
import socket
import traceback


host = "time.nist.gov"
port = 37


if __name__ == "__main__":
    
    try:
        with socket.socket() as s:
            s.connect((host, port))
            print("Connection established.")
            
            res = b""
            
            while True:
                buff = s.recv(4096)
                if not buff:
                    break
                res += buff

            print(res.decode("ISO-8859-1", errors='replace'))
            
    except:
        print(traceback.format_exc())
    
