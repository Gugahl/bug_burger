from tkinter import *
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
        self.root.configure(background='#363636')
        self.root.geometry(f"{self.largura}x{self.altura}")
        self.root.resizable(True, True)

    def mostrar_menu_principal(self):
        self.frame_atual = Frame(self.root, bd=8, bg='#BEBEBE', highlightbackground='black', highlightthickness=3)
        self.frame_atual.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

        Label(self.frame_atual, text="Restaurante", font=('arialblack', 30), bg='#BEBEBE').place(relx=0.35, rely=0.05, relwidth=0.3, relheight=0.1)
        
        Button(self.frame_atual, text="Acessar caixa", command=self.mostrar_caixa, bg='#C0C0C0').place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.1)
        
        Button(self.frame_atual, text="Acessar estoque", command=self.mostrar_estoque, bg='#C0C0C0').place(relx=0.35, rely=0.35, relwidth=0.3, relheight=0.1)
        
        Button(self.frame_atual, text="Sair", command=self.root.destroy, bg='#C0C0C0').place(relx=0.35, rely=0.5, relwidth=0.3, relheight=0.1)

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
