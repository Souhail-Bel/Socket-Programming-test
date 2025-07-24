import sys
import socket
import traceback
# import struct
import time
from time import strftime, localtime

import tkinter as tk


t = 0

# Function to update the digital clock label
def tick():
    global t
    str_NIST_t = strftime(DATE_FORMAT, localtime(t - dt))
    str_SYS_t  = strftime(DATE_FORMAT, localtime(int(time.time())))
    NIST_clock.config(text=str_NIST_t)
    SYS_clock.config(text=str_SYS_t)
    t += 1
    NIST_clock.after(1000, tick)


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
            t = int.from_bytes(res, "big")
            t_sys = int(time.time()) + dt
            # t = t_sys # When the server fails us
            
            print("===== TIME SINCE 1900-01-01 =====")
            print("NIST :", t, " seconds")
            print("SYS  :", t_sys, " seconds")
            
            print()
            
            print("=========== FORMATTED ===========")
            print("NIST :", strftime(DATE_FORMAT, localtime(t - dt)))
            print("SYS  :", strftime(DATE_FORMAT, localtime(t_sys - dt)))
            
            root = tk.Tk()
            root.title("C L O C K")

            # NIST Clock
            tk.Label(root, font=('monospace', 40, 'bold'), text="NIST:").pack(pady=(20, 0))
            NIST_clock = tk.Label(root, font=('monospace', 40, 'bold'))
            NIST_clock.pack(pady=(0, 20))

            # SYS Clock
            tk.Label(root, font=('monospace', 40, 'bold'), text="SYS:").pack(pady=(20, 0))
            SYS_clock = tk.Label(root, font=('monospace', 40, 'bold'))
            SYS_clock.pack(pady=(0, 20))


            tick()
            root.mainloop()
            
    except:
        print(traceback.format_exc())
    
