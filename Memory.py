from abc import abstractmethod
class Memory:
    
    def __init__(self, tam):
        self.tamanho = tam

    def capacidade(self):
        return self.tamanho

    def verifica_endereco(self, ender):
        if (ender < 0) or (ender >= self.tamanho):
            raise EnderecoInvalido(ender)
    
    @abstractmethod
    def read(self, ender):
      pass
    
    @abstractmethod
    def write(self, ender, val):
      pass
    
# Exceção (erro)
class EnderecoInvalido(Exception):
    def __init__(self, ender):
        self.ender = ender
        
    def __str__(self):
        return str(self.ender)