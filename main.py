from tkinter import *
from estoque import *
from caixa import *

altura = 720
largura = 1280
historico_movimentacoes = []

# Define functions for handling stock and sales, similar to the previously provided code

class Application:
    def __init__(self, root):
        self.root = root
        self.tela()
        self.frame_main = Frame(root)
        self.frame_caixa = Frame(root)
        self.frame_estoque = Frame(root)
        self.mostrar_menu_principal()

    def tela(self):
        self.root.title("Gerenciamento de Restaurante")
        self.root.configure(background='#2E2E2E')
        self.root.geometry(f"{largura}x{altura}")
        self.root.resizable(True, True)

    def mostrar_menu_principal(self):
        self.frame_main = Frame(self.root, bd=8, bg='#D5D5D5', highlightbackground='black', highlightthickness=2)
        self.frame_main.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

        Label(self.frame_main, text="BugBurger", font=('Helvetica', 36, 'bold'), bg='#D5D5D5').place(relx=0.35, rely=0.05, relwidth=0.3, relheight=0.1)
        
        # Estilizando os botões
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 18), padding=10)
        style.map('TButton', background=[('active', '#BEBEBE')])

        ttk.Button(self.frame_main, text="Acessar caixa", command=self.mostrar_caixa).place(relx=0.35, rely=0.25, relwidth=0.3, relheight=0.1)
        ttk.Button(self.frame_main, text="Acessar estoque", command=self.mostrar_estoque).place(relx=0.35, rely=0.4, relwidth=0.3, relheight=0.1)
        ttk.Button(self.frame_main, text="Sair", command=self.root.destroy).place(relx=0.35, rely=0.55, relwidth=0.3, relheight=0.1)

    def mostrar_estoque(self):
        self.frame_main.place_forget()
        self.frame_estoque = Frame(self.root, bd=8, bg='#E8E8E8', highlightbackground='#363636', highlightthickness=3)
        self.frame_estoque.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
        
        Label(self.frame_estoque, text="Estoque", font=('Arial', 30), bg='#E8E8E8', fg='#363636').place(relx=0.35, rely=0.05, relwidth=0.3, relheight=0.1)
        
        self.bt_adicionar = Button(self.frame_estoque, text="Adicionar produto", command=lambda: form_adicionar_produto(self), bg='#363636', fg='white')
        self.bt_adicionar.place(relx=0.35, rely=0.20, relwidth=0.3, relheight=0.1)
        self.bt_adicionar.config(font=('Arial', 12))
        
        self.bt_remover = Button(self.frame_estoque, text='Remover produto', command=lambda: form_remover_produto(self), bg='#363636', fg='white')
        self.bt_remover.place(relx=0.35, rely=0.35, relwidth=0.3, relheight=0.1)
        self.bt_remover.config(font=('Arial', 12))
        
        self.bt_ver_estoque = Button(self.frame_estoque, text='Ver estoque', command=lambda: ver_estoque(self), bg='#363636', fg='white')
        self.bt_ver_estoque.place(relx=0.35, rely=0.50, relwidth=0.3, relheight=0.1)
        self.bt_ver_estoque.config(font=('Arial', 12))
        
        self.bt_sair = Button(self.frame_estoque, text='Voltar ao menu principal', command=lambda: self.voltar_menu_principal(self.frame_estoque), bg='#363636', fg='white')
        self.bt_sair.place(relx=0.35, rely=0.65, relwidth=0.3, relheight=0.1)
        self.bt_sair.config(font=('Arial', 12))

    def mostrar_caixa(self):
        self.frame_main.place_forget()
        nome_arquivo_vendas = 'historico.csv'
        vendas = ler_vendas(nome_arquivo_vendas)
        
        self.frame_caixa = Frame(self.root, bd=8, bg='#E8E8E8', highlightbackground='#363636', highlightthickness=3)
        self.frame_caixa.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

        Label(self.frame_caixa, text="Caixa", font=('Arial Black', 30), bg='#E8E8E8').place(relx=0.35, rely=0.05, relwidth=0.3, relheight=0.1)

        self.bt_caixa = Button(self.frame_caixa, text="Registrar Venda", command=lambda: form_registrar_venda(self, nome_arquivo_vendas), bg='#363636', fg='white')
        self.bt_caixa.place(relx=0.35, rely=0.20, relwidth=0.3, relheight=0.1)

        self.bt_historico = Button(self.frame_caixa, text='Ver Histórico de Vendas', command=lambda: historico_vendas(self.frame_caixa, vendas), bg='#363636', fg='white')
        self.bt_historico.place(relx=0.35, rely=0.35, relwidth=0.3, relheight=0.1)
        
        self.bt_grafico = Button(self.frame_caixa, text='Ver Gráficos', command=lambda: exibir_graficos(self.frame_caixa, vendas), bg='#363636', fg='white')
        self.bt_grafico.place(relx=0.35, rely=0.50, relwidth=0.3, relheight=0.1)

        self.bt_sair = Button(self.frame_caixa, text='Voltar ao Menu Principal', command=lambda: self.voltar_menu_principal(self.frame_caixa), bg='#363636', fg='white')
        self.bt_sair.place(relx=0.35, rely=0.65, relwidth=0.3, relheight=0.1)

    def voltar_menu_principal(self, frame_atual):
        frame_atual.place_forget()
        self.mostrar_menu_principal()

def main():
    root = Tk()
    Application(root)
    root.mainloop()

if __name__ == "__main__":
    main()
