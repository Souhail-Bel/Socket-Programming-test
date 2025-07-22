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

if __name__ == "__main__":
    IP_addrs = []   
    for i in range(10):
        src_dst = get_addrs(f"tcp_addrs_{i}.txt")
        # IP_addrs.append
        print(split_addrs_src_dst(src_dst))
    
    # IP_addr_0 = IP_addrs[0]
    
    # with open(TCP_DATA_DIR + f"tcp_data_{0}.dat", 'rb') as f:
        
