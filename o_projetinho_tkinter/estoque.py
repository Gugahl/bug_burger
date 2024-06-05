from utils import ler_estoque, escrever_estoque

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
                produto = {"nome" : None, "qtd" : None}
                produto["nome"] = input("Insira o nome do produto a ser adicionado: ").upper()
                while True:
                    produto["qtd"] = input("Insira a quantidade a ser adicionada ao estoque: ")
                    if not produto["qtd"].isnumeric():
                        print("POR FAVOR INSIRA SOMENTE NÚMEROS INTEIROS E POSITIVOS!!!!")
                    else:
                        produto["qtd"] = int(produto["qtd"])
                        break
                if len(estoque) == 0:
                    estoque.append(produto)   
                else:
                    existe = False
                    for i in estoque:
                        if i["nome"] == produto["nome"]:
                            existe = True
                            i["qtd"] += produto["qtd"]
                            break
                    if not existe:
                        estoque.append(produto)
                print(f"{produto['qtd']} UNIDADES DE '{produto['nome']}' FORAM ADICIONADAS AO ESTOQUE")
                escrever_estoque(nome_arquivo, estoque)
                input("Aperte enter para voltar...")
            case "2":
                if len(estoque) == 0:
                    print("NÃO HÁ NENHUM PRODUTO NO SEU ESTOQUE!")
                    input("Aperte enter para voltar...")
                else:
                    nome = input("Digite o nome do produto a ser removido: ")
                    nome = nome.upper()
                    for i in estoque:
                        if i.get('nome') == nome:
                            estoque.remove(i)
                            print("PRODUTO REMOVIDO COM SUCESSO!")
                            escrever_estoque(nome_arquivo, estoque)
                            input("Aperte enter para voltar...")
                            break
                    else:
                        print(f"ERRO! NÃO HÁ PRODUTO CHAMADO '{nome}' NO ESTOQUE")
                        input("Aperte enter para voltar...")
            case "3":
                if len(estoque) == 0:
                    print("ESTOQUE VAZIO...")
                    input("Aperte enter para voltar...")
                else:
                    print("PRODUTO\t\tESTOQUE")
                    for i in estoque:
                        print(f"{i['nome']}\t\t{i['qtd']}")
                    input("Aperte enter para voltar...")
            case "4":
                break
            case other:
                print("\033[31mCOMANDO INVÁLIDO!\033[m")

# Exemplo de chamada à função principal
if __name__ == "__main__":
    acessar_estoque()
