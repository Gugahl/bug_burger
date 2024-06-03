from estoque import acessar_estoque
from caixa import acessar_caixa

def main():
    while True:
        print("Selecione a ação:")
        print("1. Acessar Caixa")
        print("2. Estoque")
        print("3. Sair")

        opcao = input("Opção: ")

        match opcao:
            case "1":
                acessar_caixa()
            case "2":
                acessar_estoque()
            case "3":
                break
            case other:
                print("OPÇÃO INVÁLIDA!")
                
if __name__ == "__main__":
    main()
