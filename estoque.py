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

# Função para acessar o estoque
def acessar_estoque():
    nome_arquivo = "estoque.txt"
    estoque = ler_estoque(nome_arquivo)
    while True:
        print("""\nO que você deseja fazer:
1) Adicionar produto
2) Remover produto
3) Ver estoque
4) Voltar ao menu principal""")
        escolha = input()
        match escolha:
            case "1":
                # Dicionário para guardar o nome e a quantidade dos produtos a serem armazenados
                produto = {"nome" : None, "qtd" : None}
                produto["nome"] = input("Insira o nome do produto a ser adicionado: ").upper()
                # Verifica se a quantidade inserida é um valor numérico inteiro e positivo
                while True:
                    produto["qtd"] = input("Insira a quantidade a ser adicionada ao estoque: ")
                    if not produto["qtd"].isnumeric():
                        print("POR FAVOR INSIRA SOMENTE NÚMEROS INTEIROS E POSITIVOS!!!!")
                    else:
                        produto["qtd"] = int(produto["qtd"])
                        break
                # Verifica se o estoque está vazio
                if len(estoque) == 0:
                    estoque.append(produto)   
                else:
                    existe = False
                    # Verifica se já existem produtos desse tipo no estoque
                    for i in estoque:
                        if i["nome"] == produto["nome"]:
                            existe = True
                            # Adiciona produtos extras se já existir produtos do tipo mencionado
                            i["qtd"] += produto["qtd"]
                            break
                    if not existe:
                        # Adiciona o tipo de produto ao estoque se não houver nenhum desse tipo
                        estoque.append(produto)
                print(f"{produto['qtd']} UNIDADES DE '{produto['nome']}' FORAM ADICIONADAS AO ESTOQUE")
                escrever_estoque(nome_arquivo, estoque)  # Escreve estoque atualizado no arquivo
                input("Aperte enter para voltar...")
            case "2":
                # Verifica se o estoque está vazio
                if len(estoque) == 0:
                    print("NÃO HÁ NENHUM PRODUTO NO SEU ESTOQUE!")
                    input("Aperte enter para voltar...")
                else:
                    nome = input("Digite o nome do produto a ser removido: ")
                    nome = nome.upper()
                    # Verifica se o produto existe
                    for i in estoque:
                        if i.get('nome') == nome:
                            estoque.remove(i)
                            print("PRODUTO REMOVIDO COM SUCESSO!")
                            escrever_estoque(nome_arquivo, estoque)  # Escreve estoque atualizado no arquivo
                            input("Aperte enter para voltar...")
                            break
                    else:
                        print(f"ERRO! NÃO HÁ PRODUTO CHAMADO '{nome}' NO ESTOQUE")
                        input("Aperte enter para voltar...")
            case "3":
                # Verifica se o estoque está vazio
                if len(estoque) == 0:
                    print("ESTOQUE VAZIO...")
                    input("Aperte enter para voltar...")
                else:
                    # Mostra uma tabela contendo os produtos e suas quantidades no estoque
                    print("PRODUTO\t\tESTOQUE")
                    for i in estoque:
                        print(f"{i['nome']}\t\t{i['qtd']}")
                    input("Aperte enter para voltar...")
            case "4":
                # Volta para o menu principal
                break
            case other:
                print("\033[31mCOMANDO INVÁLIDO!\033[m")

# Exemplo de chamada à função principal
if __name__ == "__main__":
    acessar_estoque()
