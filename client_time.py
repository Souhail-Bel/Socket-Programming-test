import sys
import socket
import traceback
# import struct


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
            # !: Network byte order, I: unsigned
            # t = struct.unpack('!I', res)[0]
            t = int.from_bytes(res, "big")
            print(t)
            
    except:
        print(traceback.format_exc())
    
