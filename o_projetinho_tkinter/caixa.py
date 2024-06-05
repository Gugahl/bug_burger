from datetime import datetime
from utils import ler_estoque, escrever_estoque, ler_vendas, escrever_vendas

def registrar_venda(nome_produto, quantidade, preco):
    vendas = ler_vendas("historico.txt")
    estoque = ler_estoque("estoque.txt")
    
    produto_estoque = None
    for item in estoque:
        if item["nome"] == nome_produto:
            produto_estoque = item
            break

    if not produto_estoque:
        return "Produto não encontrado no estoque!"

    if quantidade > produto_estoque["qtd"]:
        return "Quantidade insuficiente no estoque!"

    produto_estoque["qtd"] -= quantidade
    if produto_estoque["qtd"] == 0:
        estoque.remove(produto_estoque)
    escrever_estoque("estoque.txt", estoque)

    venda = {"data": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "produto": nome_produto, "qtd": quantidade, "preco": preco}
    vendas.append(venda)
    if len(vendas) > 12:
        vendas = [venda]
    escrever_vendas("historico.txt", vendas)

    return "Venda registrada com sucesso!"

def calcular_total_vendido():
    vendas = ler_vendas("historico.txt")
    total = sum(venda['qtd'] * venda['preco'] for venda in vendas)
    return total

def obter_historico_vendas():
    return ler_vendas("historico.txt")
