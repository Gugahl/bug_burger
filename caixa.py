from datetime import datetime
import os
from estoque import ler_estoque, escrever_estoque

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

# Função para acessar o caixa
def acessar_caixa():
    nome_arquivo_vendas = 'historico.txt'
    vendas = ler_vendas(nome_arquivo_vendas)
    estoque = ler_estoque("estoque.txt")  # Ler estoque antes de cada operação
    while True:
        print("""\nO que você deseja fazer:
1) Registrar venda
2) Ver histórico de vendas
3) Calcular total vendido
4) Voltar ao menu principal""")
        escolha = input()
        match escolha:
            case "1":
                # Dicionário para guardar os detalhes da venda
                venda = {"data": None, "produto": None, "qtd": None, "preco": None}
                venda["data"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                venda["produto"] = input("Insira o nome do produto vendido: ").upper()
                
                # Verifica se o produto está no estoque
                produto_estoque = None
                for item in estoque:
                    if item["nome"] == venda["produto"]:
                        produto_estoque = item
                        break
                
                if not produto_estoque:
                    print("PRODUTO NÃO ENCONTRADO NO ESTOQUE!")
                    input("Aperte enter para voltar...")
                    continue
                
                # Verifica se a quantidade inserida é um valor numérico inteiro e positivo
                while True:
                    venda["qtd"] = input("Insira a quantidade vendida: ")
                    if not venda["qtd"].isnumeric() or int(venda["qtd"]) <= 0:
                        print("POR FAVOR INSIRA SOMENTE NÚMEROS, QUE SEJAM INTEIROS E POSITIVOS!!!!")
                    else:
                        venda["qtd"] = int(venda["qtd"])
                        break
                
                # Verifica se há quantidade suficiente no estoque
                if venda["qtd"] > produto_estoque["qtd"]:
                    print("QUANTIDADE INSUFICIENTE NO ESTOQUE!")
                    input("Aperte enter para voltar...")
                    continue
                
                # Verifica se o preço inserido é um valor numérico positivo
                while True:
                    preco = input("Insira o preço unitário do produto vendido: ")
                    if preco.replace('.', '', 1).isdigit() and float(preco) > 0:
                        venda["preco"] = float(preco)
                        break
                    else:
                        print("POR FAVOR INSIRA SOMENTE NÚMEROS POSITIVOS!!!!")
                
                # Atualiza a quantidade no estoque
                produto_estoque["qtd"] -= venda["qtd"]
                # Remove o produto do estoque se a quantidade for zero
                if produto_estoque["qtd"] == 0:
                    estoque.remove(produto_estoque)
                escrever_estoque("estoque.txt", estoque)  # Escreve estoque atualizado
                
                # Adiciona a venda ao histórico
                vendas.append(venda)
                escrever_vendas(nome_arquivo_vendas, vendas)  # Escreve histórico atualizado
                print("VENDA REGISTRADA COM SUCESSO!")
                input("Aperte enter para voltar...")
            case "2":
                # Verifica se há vendas registradas
                if len(vendas) == 0:
                    print("NENHUMA VENDA REGISTRADA...")
                    input("Aperte enter para voltar...")
                else:
                    # Mostra uma tabela contendo o histórico de vendas
                    print("DATA\t\t\tPRODUTO\t\tQTD\tPREÇO UNITÁRIO")
                    for venda in vendas:
                        print(f"{venda['data']}\t{venda['produto']}\t{venda['qtd']}\t{venda['preco']}")
                    input("Aperte enter para voltar...")
            case "3":
                # Calcula o total vendido
                total = sum(venda['qtd'] * venda['preco'] for venda in vendas)
                print(f"O TOTAL VENDIDO É: R${total:.2f}")
                input("Aperte enter para voltar...")
            case "4":
                # Volta para o menu principal
                break
            case other:
                print("\033[31mCOMANDO INVÁLIDO!\033[m")

# Exemplo de chamada à função principal
if __name__ == "__main__":
    acessar_caixa()
