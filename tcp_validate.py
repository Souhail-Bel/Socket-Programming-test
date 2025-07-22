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
    
    Z = b'\x00'
    PTCL = b'\x06'
    
    ret = src_IP + dst_IP + Z + PTCL + TCP_length.to_bytes(2, "big")
    
    return ret


def compute_checksum(pseudo_header: bytes, TCP_data: bytes) -> int:
    
    return 0


if __name__ == "__main__":
    
    # The TCP data used here are from Beej's Guide
    # https://github.com/beejjorgensen/bgnet0/tree/main/source/exercises/tcpcksum
    
    # IP_addrs            = []
    # IP_pseudo_headers   = []
    
    # TCP_data            = []
    # TCP_data_cksum_zero = []
    # TCP_length          = []
    
    TCP_checksum_start  = 16
    TCP_checksum_end    = 18 # [CHECKSUM[
    # TCP_checksums       = []
    
    for i in range(10):
        
        # Get IP addresses
        src_dst = get_addrs(f"tcp_addrs_{i}.txt")
        IP_addr = split_addrs_src_dst(src_dst)
        
        # Get TCP data
        TCP_data = get_tcp_data(f"tcp_data_{i}.dat")
        TCP_length = len(TCP_data)
        
        # Get checksum from TCP data and zero it
        TCP_checksum = int.from_bytes(TCP_data[TCP_checksum_start:TCP_checksum_end], "big")
        
        TCP_cksum_zero = TCP_data[:TCP_checksum_start] + b'\x00\x00' + TCP_data[TCP_checksum_end:]
        if TCP_length%2:
            TCP_cksum_zero += b'\x00'
        
    
        # Build IP pseudo headers
        IP_pseudo_header = build_pseudo_header(IP_addr[0], IP_addr[1], TCP_length)
