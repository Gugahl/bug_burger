from tkinter import *
from estoque import acessar_estoque  # Importa a função acessar_estoque do módulo estoque
from caixa import acessar_caixa  # Importa a função acessar_caixa do módulo caixa

altura = 720
largura = 1280

# Classe principal da aplicação
class Application:
    def __init__(self, root):
        self.root = root
        self.tela()  # Configura a janela principal
        self.frame_atual = None  # Inicializa o frame atual como None
        self.mostrar_menu_principal()  # Mostra o menu principal na inicialização

    # Configuração da janela principal
    def tela(self):
        self.altura = altura
        self.largura = largura
        self.root.title("Gerenciamento de Restaurante")
        self.root.configure(background='#363636')
        self.root.geometry(f"{self.largura}x{self.altura}")
        self.root.resizable(True, True)

    # Mostra o menu principal
    def mostrar_menu_principal(self):
        self.frame_atual = Frame(self.root, bd=8, bg='#BEBEBE', highlightbackground='black', highlightthickness=3)
        self.frame_atual.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

        Label(self.frame_atual, text="Restaurante", font=('arialblack', 30), bg='#BEBEBE').place(relx=0.35, rely=0.05, relwidth=0.3, relheight=0.1)
        
        # Botão para acessar o caixa
        Button(self.frame_atual, text="Acessar caixa", command=self.mostrar_caixa, bg='#C0C0C0').place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.1)
        
        # Botão para acessar o estoque
        Button(self.frame_atual, text="Acessar estoque", command=self.mostrar_estoque, bg='#C0C0C0').place(relx=0.35, rely=0.35, relwidth=0.3, relheight=0.1)
        
        # Botão para sair do programa
        Button(self.frame_atual, text="Sair", command=self.root.destroy, bg='#C0C0C0').place(relx=0.35, rely=0.5, relwidth=0.3, relheight=0.1)

    # Função para mostrar a tela de acesso ao estoque
    def mostrar_estoque(self):
        acessar_estoque(self)

    # Função para mostrar a tela de acesso ao caixa
    def mostrar_caixa(self):
        acessar_caixa(self)

# Função principal para iniciar a aplicação
def main():
    root = Tk()  # Cria a janela principal
    Application(root)  # Inicializa a aplicação
    root.mainloop()  # Loop principal da aplicação

# Verifica se o módulo está sendo executado como script principal
if __name__ == "__main__":
    main()  # Chama a função main para iniciar a aplicação
