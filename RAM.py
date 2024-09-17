
from Memory import Memory


class RAM(Memory):
    def __init__(self, k):
        super().__init__(2**k)
        self.memoria = [0] * self.tamanho

    def read(self, ender):
        super().verifica_endereco(ender)
        return self.memoria[ender]

    def write(self, ender, val):
        super().verifica_endereco(ender)
        self.memoria[ender] = val