from tkinter import *
from tkinter import ttk  # Importando ttk para estilos modernos
from estoque import acessar_estoque
from caixa import acessar_caixa

altura = 720
largura = 1280

class Application:
    def __init__(self, root):
        self.root = root
        self.tela()
        self.frame_atual = None
        self.mostrar_menu_principal()

    def tela(self):
        self.altura = altura
        self.largura = largura
        self.root.title("Gerenciamento de Restaurante")
        self.root.configure(background='#2E2E2E')
        self.root.geometry(f"{self.largura}x{self.altura}")
        self.root.resizable(True, True)

    def mostrar_menu_principal(self):
        self.frame_atual = Frame(self.root, bd=8, bg='#D5D5D5', highlightbackground='black', highlightthickness=2)
        self.frame_atual.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

        Label(self.frame_atual, text="Burgerburger", font=('Helvetica', 36, 'bold'), bg='#D5D5D5').place(relx=0.35, rely=0.05, relwidth=0.3, relheight=0.1)
        
        # Estilizando os botões
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 18), padding=10)
        style.map('TButton', background=[('active', '#BEBEBE')])

        ttk.Button(self.frame_atual, text="Acessar caixa", command=self.mostrar_caixa).place(relx=0.35, rely=0.25, relwidth=0.3, relheight=0.1)
        ttk.Button(self.frame_atual, text="Acessar estoque", command=self.mostrar_estoque).place(relx=0.35, rely=0.4, relwidth=0.3, relheight=0.1)
        ttk.Button(self.frame_atual, text="Sair", command=self.root.destroy).place(relx=0.35, rely=0.55, relwidth=0.3, relheight=0.1)

    def mostrar_estoque(self):
        acessar_estoque(self)

    def mostrar_caixa(self):
        acessar_caixa(self)

def main():
    root = Tk()
    Application(root)
    root.mainloop()

if __name__ == "__main__":
    main()
