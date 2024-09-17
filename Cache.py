import math

from Memory import Memory

# Classe que representa uma linha da cache
class CacheLine:
    def __init__(self, tamanho_linha):
        # 'tag' identifica qual bloco da RAM está associado a essa linha de cache.
        self.tag = None  
        # Bit de modificação (dirty bit): 0 significa que os dados estão intactos, 1 significa que foram alterados.
        self.modificado = 0  
        # 'data' armazena os dados reais na linha de cache, iniciada com zeros.
        self.data = [0] * tamanho_linha  

# Classe que implementa uma cache simples com mapeamento direto
class CacheSimples(Memory):
    def __init__(self, capacidade_cache, tamanho_linha, ram):
        # Inicializa a classe base Memoria com a capacidade da cache
        super().__init__(capacidade_cache)
        # Define a capacidade da cache (em bytes)
        self.capacidade_cache = capacidade_cache  
        # Define o tamanho de cada linha da cache (em bytes)
        self.tamanho_linha = tamanho_linha  
        # Referência para a memória principal (RAM)
        self.ram = ram  
        # Cria um conjunto de linhas de cache, baseado na capacidade da cache e no tamanho de cada linha
        self.cache = [CacheLine(tamanho_linha) for _ in range(capacidade_cache // tamanho_linha)]

    # Método responsável por calcular os valores w, r, t e s a partir de um endereço
    def calcular_wrt(self, endereco):
        # 'w_bits' é o número de bits necessários para representar o deslocamento dentro de uma linha de cache
        w_bits = int(math.log2(self.tamanho_linha))
        # 'r_bits' é o número de bits necessários para identificar o índice da linha de cache
        r_bits = int(math.log2(self.capacidade_cache // self.tamanho_linha))
        # 't_bits' são os bits restantes que formam o tag (identificação do bloco na RAM)
        t_bits = max(endereco.bit_length() - (w_bits + r_bits), 0)
        
        # 'w' é o deslocamento (offset) dentro da linha de cache
        w = endereco & ((1 << w_bits) - 1)
        # 'r' é o índice da linha de cache
        r = (endereco >> w_bits) & ((1 << r_bits) - 1)
        # 't' é o tag, que identifica qual bloco da RAM está armazenado na cache
        t = (endereco >> (w_bits + r_bits)) & ((1 << t_bits) - 1)
        # 's' é o endereço real na RAM, calculado a partir de 't' e 'r'
        s = (t << r) | r
        
        # Retorna os valores w (offset), r (índice da cache), t (tag) e s (endereço RAM)
        return w, r, t, s

    # Método responsável pela leitura de dados da cache
    def read(self, endereco):
        # Calcula os valores w, r, t e s a partir do endereço
        w, r, t, s = self.calcular_wrt(endereco)
        # Acessa a linha de cache com índice 'r'
        cache_line = self.cache[r]
        
        # Verifica se o bloco de memória na cache é o que está sendo solicitado (compara a tag)
        if cache_line.tag == t:  # Hit: dado já está na cache
            return cache_line.data[w]  # Retorna o dado diretamente da cache
        else:  # Miss: dado não está na cache
            print(f"MISS: {endereco} -> L{r}")
            # Se a linha de cache foi modificada, escreve os dados de volta na RAM
            if cache_line.modificado != 0:
                self.CacheParaRAM(cache_line, r)
            # Carrega o bloco correto da RAM para a cache
            self.RAMParaCache(s, t, r)
            # Após carregar, retorna o dado da cache
            return cache_line.data[w]

    # Método responsável por escrever dados na cache
    def write(self, endereco, valor):
        # Calcula os valores w, r, t e s a partir do endereço
        w, r, t, s = self.calcular_wrt(endereco)
        # Acessa a linha de cache com índice 'r'
        cache_line = self.cache[r]
        
        # Verifica se o bloco de memória correspondente já está na cache
        if cache_line.tag == t:  # Hit: o bloco já está na cache
            cache_line.data[w] = valor  # Atualiza o valor na cache
            cache_line.modificado = 1  # Marca a linha como modificada
        else:  # Miss: o bloco não está na cache
            print(f"MISS: {endereco} -> L{r}")
            # Se a linha de cache foi modificada, escreve os dados de volta na RAM
            if cache_line.modificado != 0:
                self.CacheParaRAM(cache_line, r)
            # Carrega o bloco correto da RAM para a cache
            self.RAMParaCache(s, t, r)
            # Após carregar, escreve o novo valor na cache
            cache_line.data[w] = valor
            # Atualiza a tag para refletir o novo bloco carregado
            cache_line.tag = t
            # Marca a linha como modificada
            cache_line.modificado = 1

    # Método que escreve os dados de uma linha de cache modificada de volta na RAM
    def CacheParaRAM(self, cache_line, s):
        # Apenas escreve na RAM se a linha tiver sido modificada (dirty bit)
        if cache_line.modificado:
            # Calcula o endereço na RAM a partir de 's'
            index_ram = s * (self.capacidade_cache // self.tamanho_linha)
            # Para cada valor na linha de cache, escreve no local correspondente da RAM
            for w, valor in enumerate(cache_line.data):
                self.ram.write(index_ram + w, valor)
            # Após escrever, marca a linha de cache como não modificada
            cache_line.modificado = 0
    
    # Método que carrega um bloco de dados da RAM para a cache
    def RAMParaCache(self, s, t, r):
        # Acessa a linha de cache correspondente
        cache_line = self.cache[r]
        # Calcula o endereço inicial na RAM a partir de 's'
        index_ram = s * (self.capacidade_cache // self.tamanho_linha)
        # Para cada posição da linha, lê os dados da RAM e os carrega na cache
        for w in range(self.tamanho_linha):
            valor = self.ram.read(index_ram + w)
            cache_line.data[w] = valor
        # Atualiza o tag da linha de cache para refletir o bloco que foi carregado
        cache_line.tag = t
        # Marca a linha como não modificada
        cache_line.modificado = 0