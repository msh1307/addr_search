import gdb
import struct
inf = gdb.selected_inferior()
print("addr : ",end='')
addr = input()
res = gdb.execute(f"xinfo {addr}",to_string=True)
if addr.startswith("0x"):
    addr = int(addr,16)
else:
    addr = int(addr)
if 'is not mapped' in res:
    print("invalid address")
else:
    res = res[res.find('Containing mapping:')+20:res.find('Offset')]
    res = res.split()
    addr_st = int(res[1],16)
    addr_end = int(res[2],16)
    print("target addr start: ",end='')
    tar_st = input()
    if tar_st.startswith("0x"):
        tar_st = int(tar_st,16)
    else:
        tar_st = int(tar_st)
    print("target addr end : ",end='')
    tar_end = input()
    if tar_end.startswith("0x"):
        tar_end = int(tar_end,16)
    else:
        tar_end = int(tar_end)
    mem = inf.read_memory(addr_st, addr_end-addr_st)
    memory = [0 for _ in range((addr_end-addr_st)//8)]
    for i in range((addr_end-addr_st)//8):
        memory[i] = (struct.unpack("<Q",mem[8*i:8*i+8]))[0]
    for i,j in enumerate(memory):
        if j >= tar_st and j<= tar_end:
            print(f"\n{hex(i*8 + addr_st)} : {hex(j)}")