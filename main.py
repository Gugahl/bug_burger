from estoque import acessar_estoque
from caixa import acessar_caixa

def main():
    while True:
        print("Selecione a ação:")
        print("1. Acessar Caixa")
        print("2. Estoque")
        print("3. Sair")

        opcao = input("Opção: ")

        if opcao == "1":
            acessar_caixa()
        elif opcao == "2":
            acessar_estoque()
        elif opcao == "3":
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
