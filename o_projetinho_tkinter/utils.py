import os

# Função para ler o estoque do arquivo
def ler_estoque(nome_arquivo):
    estoque = []
    if os.path.exists(nome_arquivo):
        arquivo = open(nome_arquivo, 'r')
        for linha in arquivo:
            nome, qtd = linha.strip().split(',')
            estoque.append({"nome": nome, "qtd": int(qtd)})
        arquivo.close()
    return estoque

# Função para escrever o estoque no arquivo
def escrever_estoque(nome_arquivo, estoque):
    arquivo = open(nome_arquivo, 'w')
    for item in estoque:
        arquivo.write(f"{item['nome']},{item['qtd']}\n")
    arquivo.close()

# Função para ler o histórico de vendas do arquivo
def ler_vendas(nome_arquivo):
    vendas = []
    if os.path.exists(nome_arquivo):
        arquivo = open(nome_arquivo, 'r')
        for linha in arquivo:
            data, produto, qtd, preco = linha.strip().split(',')
            vendas.append({"data": data, "produto": produto, "qtd": int(qtd), "preco": float(preco)})
        arquivo.close()
    return vendas

# Função para escrever o histórico de vendas no arquivo
def escrever_vendas(nome_arquivo, vendas):
    arquivo = open(nome_arquivo, 'w')
    for venda in vendas:
        arquivo.write(f"{venda['data']},{venda['produto']},{venda['qtd']},{venda['preco']}\n")
    arquivo.close()
