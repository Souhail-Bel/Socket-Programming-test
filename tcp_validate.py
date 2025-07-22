# TCP RFC 793


# TCP Header format

 # 0                   1                   2                   3   
 # 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |          Source Port          |       Destination Port        |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                        Sequence Number                        |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                    Acknowledgment Number                      |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |  Data |           |U|A|P|R|S|F|                               |
# | Offset| Reserved  |R|C|S|S|Y|I|            Window             |
# |       |           |G|K|H|T|N|N|                               |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |           Checksum            |         Urgent Pointer        |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                    Options                    |    Padding    |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                             data                              |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   

# IP Pseudo header

 # +--------+--------+--------+--------+
 # |           Source Address          |
 # +--------+--------+--------+--------+ 
 # |         Destination Address       |
 # +--------+--------+--------+--------+
 # |  zero  |  PTCL  |    TCP Length   |
 # +--------+--------+--------+--------+

   
   
TCP_DATA_DIR = "tcp_data/"

def get_addrs(file_name: str) -> list:
    
    ret = []
    with open(TCP_DATA_DIR + file_name, 'r') as f:
        ret = f.read().strip().split(' ')
    return ret

def convert_addr_to_bytes(IP_addr: str) -> bytes:
    
    res = b''
    
    for byte in IP_addr.split('.'):
        res += int(byte).to_bytes(1, "big")
    
    return res

def split_addrs_src_dst(src_dst: list) -> tuple:
    
    src_addr = convert_addr_to_bytes(src_dst[0])
    dst_addr = convert_addr_to_bytes(src_dst[1])
    
    return (src_addr, dst_addr)

def get_tcp_data(file_name: str) -> bytes:
    
    ret = b''
    with open(TCP_DATA_DIR + file_name, 'rb') as f:
        ret = f.read()
    
    return ret

def build_pseudo_header(src_IP: bytes, dst_IP: bytes, TCP_length: int) -> bytes:
    
    ret = b''
    
    Z = b'\0'
    PTCL = b'\6'
    
    ret = src_IP + dst_IP + Z + PTCL + TCP_length.to_bytes(2, "big")
    
    return ret

if __name__ == "__main__":
    
    # The TCP data used here are from Beej's Guide
    # https://github.com/beejjorgensen/bgnet0/tree/main/source/exercises/tcpcksum
    
    IP_addrs            = []
    IP_pseudo_headers   = []
    
    TCP_data            = []
    TCP_length          = []
    
    for i in range(10):
        src_dst = get_addrs(f"tcp_addrs_{i}.txt")
        IP_addrs.append(split_addrs_src_dst(src_dst))
        
        TCP_data_file = get_tcp_data(f"tcp_data_{i}.dat")
        TCP_data.append(TCP_data_file)
        TCP_length.append(len(TCP_data_file))
    
        IP_pseudo_headers.append(build_pseudo_header(IP_addrs[-1][0], IP_addrs[-1][1], TCP_length[-1]))
        
        print(IP_pseudo_headers[-1].hex())
