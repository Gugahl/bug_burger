import os
from tkinter import *
from tkinter import messagebox

altura = 720
largura = 1280

def adicionar_produto(estoque, nome_arquivo, entry_nome, entry_qtd, entry_preco):
    nome = entry_nome.get().upper()
    qtd = entry_qtd.get()

    if not qtd.isnumeric() or int(qtd) <= 0:
        messagebox.showerror("ERRO!", "POR FAVOR INSIRA SOMENTE NÚMEROS INTEIROS E POSITIVOS!!!!")
        return
    qtd = int(qtd)

    preco = entry_preco.get()

    if not preco.isdigit() or float(preco) <= 0:
        messagebox.showerror("EERO!","POR FAVOR INSIRA SOMENTE VALORES NUMÉRICOS E ACIMA DE ZERO!!!!")
        return
    preco = float(preco)
    
    produto = {"nome": nome, "qtd": qtd, "preco": preco}

    if len(estoque) == 0:
        estoque.append(produto)
        messagebox.showinfo("SUCESSO!", f"{produto['qtd']} UNIDADES DE '{produto['nome']}' FORAM ADICIONADAS AO ESTOQUE")
    else:
        existe = False
        for i in estoque:
            if i["nome"] == produto["nome"]:
                existe = True
                i["qtd"] += produto["qtd"]
                break
        if not existe:
            estoque.append(produto)
            messagebox.showinfo("SUCESSO!", f"{produto['qtd']} UNIDADES DE '{produto['nome']}' FORAM ADICIONADAS AO ESTOQUE")

    escrever_estoque(nome_arquivo, estoque)
    entry_nome.delete(0, END)
    entry_qtd.delete(0, END)

def remover_produto(estoque, nome_arquivo, entry_nome):
    nome = entry_nome.get().upper()

    if len(estoque) == 0:
        messagebox.showinfo("ERRO!", "NÃO HÁ NENHUM PRODUTO NO SEU ESTOQUE!")
    else:
        existe = False
        for i in estoque:
            if i.get('nome') == nome:
                existe = True
                estoque.remove(i)
                messagebox.showinfo("SUCESSO!", "PRODUTO REMOVIDO COM SUCESSO!")
                escrever_estoque(nome_arquivo, estoque)
                entry_nome.delete(0, END)
                return
        if not existe:
            messagebox.showerror("ERRO!", f"ERRO! NÃO HÁ PRODUTO CHAMADO '{nome}' NO ESTOQUE")

def obter_estoque(estoque):
    if len(estoque) == 0:
        messagebox.showinfo("Informação", "ESTOQUE VAZIO...")
    else:
        estoque_str = "PRODUTO\t\tESTOQUE\n"
        for i in estoque:
            estoque_str += f"{i['nome']}\t\t{i['qtd']}\t\t{i['preco']}\n"
        messagebox.showinfo("Estoque", estoque_str)

def ler_estoque(nome_arquivo):
    estoque = []
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, 'r') as arquivo:
            for linha in arquivo:
                nome, qtd = linha.strip().split(',')
                estoque.append({"nome": nome, "qtd": int(qtd)})
    return estoque

def escrever_estoque(nome_arquivo, estoque):
    with open(nome_arquivo, 'w') as arquivo:
        for item in estoque:
            arquivo.write(f"{item['nome']},{item['qtd']}\n")

def acessar_estoque(root=None):
    nome_arquivo = "estoque.txt"
    estoque = ler_estoque(nome_arquivo)
    root = Tk()
    
    class Application:
        def __init__(self):
            self.root = root
            self.estoque = estoque
            self.nome_arquivo = nome_arquivo
            self.tela()
            self.frames()
            self.objetos_frame1()
            root.mainloop()

        def tela(self):
            self.altura = altura
            self.largura = largura
            self.root.title("Gerenciamento de Estoque")
            self.root.configure(background='#363636')
            self.root.geometry(f"{self.largura}x{self.altura}")
            self.root.resizable(True, True)

        def frames(self):
            self.frame1 = Frame(self.root, bd=8, bg='#BEBEBE',
                                highlightbackground='black', highlightthickness=3)
            self.frame1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

        def objetos_frame1(self):
            # Label Estoque
            Label(self.frame1, text="Estoque", font=('arialblack', 30), bg='#BEBEBE').place(relx=0.35, rely=0.05, relwidth=0.3, relheight=0.1)

            # Botão adicionar produto
            self.bt_adicionar = Button(self.frame1, text="Adicionar produto", command=self.form_adicionar_produto, bg='#C0C0C0')
            self.bt_adicionar.place(relx=0.35, rely=0.20, relwidth=0.3, relheight=0.1)

            # Botão remover produto
            self.bt_remover = Button(self.frame1, text='Remover produto', command=self.form_remover_produto, bg='#C0C0C0')
            self.bt_remover.place(relx=0.35, rely=0.35, relwidth=0.3, relheight=0.1)

            # Botão ver estoque
            self.bt_ver_estoque = Button(self.frame1, text='Ver estoque', command=lambda: obter_estoque(self.estoque), bg='#C0C0C0')
            self.bt_ver_estoque.place(relx=0.35, rely=0.50, relwidth=0.3, relheight=0.1)

            # Botão voltar para o menu principal
            self.bt_sair = Button(self.frame1, text='Voltar ao menu principal', command=root.destroy, bg='#C0C0C0')
            self.bt_sair.place(relx=0.35, rely=0.65, relwidth=0.3, relheight=0.1)

        def form_adicionar_produto(self):
            frame_adicionar = Frame(self.frame1, bd=8, bg='#BEBEBE', highlightbackground='black', highlightthickness=3)
            frame_adicionar.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
            
            # Campo para o nome do produto
            Label(frame_adicionar, text="Nome do Produto", bg='#BEBEBE').place(relx=0.15, rely=0.05, relwidth=0.2, relheight=0.05)
            entry_nome = Entry(frame_adicionar)
            entry_nome.place(relx=0.35, rely=0.05, relwidth=0.5, relheight=0.05)

            # Campo para a quantidade do produto
            Label(frame_adicionar, text="Quantidade", bg='#BEBEBE').place(relx=0.15, rely=0.15, relwidth=0.2, relheight=0.05)
            entry_qtd = Entry(frame_adicionar)
            entry_qtd.place(relx=0.35, rely=0.15, relwidth=0.5, relheight=0.05)

            # Botão confirmar adicionar
            self.bt_confirmar = Button(frame_adicionar, text="Confirmar", command=lambda: adicionar_produto(self.estoque, self.nome_arquivo, entry_nome, entry_qtd), bg='#C0C0C0')
            self.bt_confirmar.place(relx=0.35, rely=0.25, relwidth=0.3, relheight=0.1)

            # Botão voltar ao menu anterior
            Button(frame_adicionar, text="Voltar ao menu anterior", command=frame_adicionar.destroy, bg='#C0C0C0').place(relx=0.02, rely=0.88, relwidth=0.3, relheight=0.1)

        def form_remover_produto(self):
            frame_remover = Frame(self.frame1, bd=8, bg='#BEBEBE', highlightbackground='black', highlightthickness=3)
            frame_remover.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
            
            Label(frame_remover, text="Nome do Produto", bg='#BEBEBE').place(relx=0.15, rely=0.05, relwidth=0.2, relheight=0.05)
            entry_nome = Entry(frame_remover)
            entry_nome.place(relx=0.35, rely=0.05, relwidth=0.5, relheight=0.05)

            # Botão confirmar remover
            Button(frame_remover, text="Confirmar", command=lambda: remover_produto(self.estoque, self.nome_arquivo, entry_nome), bg='#C0C0C0').place(relx=0.35, rely=0.15, relwidth=0.3, relheight=0.1)
            
            # Botão voltar ao menu anterior
            Button(frame_remover, text="Voltar ao menu anterior", command=frame_remover.destroy, bg='#C0C0C0').place(relx=0.02, rely=0.88, relwidth=0.3, relheight=0.1)
    
    app = Application()
    root.mainloop()

# Exemplo de chamada à função principal
if __name__ == "__main__":
    acessar_estoque(None)
