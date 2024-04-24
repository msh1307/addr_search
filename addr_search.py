import gdb
import struct

def cut(s):
    x = '0x'
    for i in s[s.find('0x')+2:]:
        if 0x30<=ord(i)<=0x39 or ord('a')<=ord(i)<=ord('f'):
            x += i
        else:
            break
    return x

inf = gdb.selected_inferior()
range_ = []
print("addr start: ",end='')
addr = input()
res = gdb.execute(f"xinfo {addr}",to_string=True)
if addr.startswith("0x"):
    addr = int(addr,16)
else:
    addr = int(addr)
range_.append(addr)
print("addr end: ",end='')
addr = input()
res = gdb.execute(f"xinfo {addr}",to_string=True)
if addr.startswith("0x"):
    addr = int(addr,16)
else:
    addr = int(addr)
range_.append(addr)
print("base address: ",end='')
addr = input()
res = gdb.execute(f"xinfo {addr}",to_string=True)
if addr.startswith("0x"):
    addr = int(addr,16)
else:
    addr = int(addr)
if range_[0] < range_[1]:
    # res = res[res.find('Containing mapping:')+20:res.find('Offset')]
    # res = res.split()
    # res = res[res.index('End')+5:]
    # # print(res)
    # x = []
    # for i in range(len(res)):
    #     if '0x' in res[i]:
    #         x.append(i)
    # assert x != -1
    # addr_st = int(cut(res[x[0]]),16)
    # addr_end = int(cut(res[x[1]]),16)
    sz = range_[1] - range_[0]
    print(f"size: {hex(sz)}")
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
    it = 0
    mem = b''
    while True:
        if it >= sz:
            print('break')
            break
        try:
            tmp = inf.read_memory(range_[0]+it, 0x1000)
        except:
            tmp = b'\x00'*0x1000
            # it &= 0xfffffffffffff000
        mem += tmp
        it += len(tmp)

    memory = [0 for _ in range(sz//8)]
    for i in range(sz//8):
        memory[i] = (struct.unpack("<Q",mem[8*i:8*i+8]))[0]
    for i,j in enumerate(memory):
        if j >= tar_st and j<= tar_end:
            print(f"\n{hex(i*8 + range_[0])} | {hex(j)} -- offset : {hex((i*8 + range_[0]) - addr)}",end='')
    print()
