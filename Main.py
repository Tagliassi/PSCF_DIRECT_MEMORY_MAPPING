import sys

from CPU import CPU
from IO import IO
from Memory import EnderecoInvalido
from RAM import RAM
from Cache import Cache

class Main:
    try:
        io = IO()
        ram = RAM(12)   # 4K de RAM (2**12)
        cache = Cache(7, 4, ram) # total cache = 128 (2**7), cacheline = 16 (2**4)
        cpu = CPU(cache, io)

        inicio = 0;
        ram.write(inicio, 110)
        ram.write(inicio+1, 130)
        cpu.run(inicio)
    except EnderecoInvalido as e:
        print("Endereco inválido:", e.ender, file=sys.stderr)