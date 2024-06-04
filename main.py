from estoque import acessar_estoque
from caixa import acessar_caixa

def main():
    while True:
        print("\nSelecione a ação:")
        print("1. Acessar Caixa")
        print("2. Estoque")
        print("3. Sair")

        opcao = input("")

        match opcao:
            case "1":
                acessar_caixa()
            case "2":
                acessar_estoque()
            case "3":
                break
            case other:
                print("\033[31mOPÇÃO INVÁLIDA!\033[m Insira uma das opções válidas.")

if __name__ == "__main__":
    main()
