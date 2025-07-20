import sys
import socket
import traceback
# import struct
import time
from time import strftime, localtime


host = "time.nist.gov"
port = 37

# The time server returns number of seconds since 1900-01-01 while the Unix system has it since 1970-01-01, we just ought to account for that difference

# Time protocol, RFC 868
dt = 2208988800

DATE_FORMAT = "%Y-%m-%d, %H:%M:%S"


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
            # t = 3961996701 # For when the server fails
            t = int.from_bytes(res, "big")
            t_sys = int(time.time()) + dt
            
            print("===== TIME SINCE 1900-01-01 =====")
            print("NIST :", t, " seconds")
            print("SYS  :", t_sys, " seconds")
            
            print()
            
            print("=========== FORMATTED ===========")
            print("NIST :", strftime(DATE_FORMAT, localtime(t - dt)))
            print("SYS  :", strftime(DATE_FORMAT, localtime(t_sys - dt)))
            
    except:
        print(traceback.format_exc())
    
