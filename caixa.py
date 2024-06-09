import os
from datetime import datetime
from tkinter import *
from tkinter import messagebox
from estoque import ler_estoque, escrever_estoque

altura = 720
largura = 1280

# Função para ler o histórico de vendas do arquivo
def ler_vendas(nome_arquivo):
    vendas = []
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, 'r') as arquivo:
            for linha in arquivo:
                data, produto, qtd, preco = linha.strip().split(',')
                vendas.append({"data": data, "produto": produto, "qtd": int(qtd), "preco": float(preco)})
    return vendas

# Função para escrever o histórico de vendas no arquivo
def escrever_vendas(nome_arquivo, vendas):
    with open(nome_arquivo, 'w') as arquivo:
        for venda in vendas:
            arquivo.write(f"{venda['data']},{venda['produto']},{venda['qtd']},{venda['preco']}\n")

def registrar_venda(vendas, estoque, nome_arquivo_vendas, entry_produto, entry_qtd, entry_preco):
    venda = {"data": None, "produto": None, "qtd": None, "preco": 0}
    venda["data"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    venda["produto"] = entry_produto.get().upper()

    # Verifica se o produto está no estoque
    produto_estoque = next((item for item in estoque if item["nome"] == venda["produto"]), None)
    if not produto_estoque:
        messagebox.showerror("Erro", "PRODUTO NÃO ENCONTRADO NO ESTOQUE!")
        return

    # Verifica se a quantidade inserida é um valor numérico inteiro e positivo
    qtd = entry_qtd.get()
    if not qtd.isnumeric() or int(qtd) <= 0:
        messagebox.showerror("Erro", "POR FAVOR INSIRA SOMENTE NÚMEROS, QUE SEJAM INTEIROS E POSITIVOS!!!!")
        return
    venda["qtd"] = int(qtd)

    # Verifica se há quantidade suficiente no estoque
    if venda["qtd"] > produto_estoque["qtd"]:
        messagebox.showerror("Erro", "QUANTIDADE INSUFICIENTE NO ESTOQUE!")
        return

    # Adciona o preço do produto
    float(venda["preco"]) += produto_estoque["preco"]

    # Atualiza a quantidade no estoque
    produto_estoque["qtd"] -= venda["qtd"]
    if produto_estoque["qtd"] == 0:
        estoque.remove(produto_estoque)
    escrever_estoque("estoque.txt", estoque)

    # Adiciona a venda ao histórico
    vendas.append(venda)
    if len(vendas) > 12:
        vendas = [venda]
    escrever_vendas(nome_arquivo_vendas, vendas)

    messagebox.showinfo("Sucesso", "VENDA REGISTRADA COM SUCESSO!")
    entry_produto.delete(0, END)
    entry_qtd.delete(0, END)
    entry_preco.delete(0, END)

def historico_vendas(frame, vendas):
    frame_historico = Frame(frame, bd=8, bg='#BEBEBE', highlightbackground='black', highlightthickness=3)
    frame_historico.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    if len(vendas) == 0:
        Label(frame_historico, text="NENHUMA VENDA REGISTRADA...", bg='#BEBEBE').place(relx=0.15, rely=0.05, relwidth=0.7, relheight=0.1)
    else:
        historico = "DATA\t\t\tPRODUTO\t\tQTD\tPREÇO UNITÁRIO\n"
        for venda in vendas:
            historico += f"{venda['data']}\t{venda['produto']}\t\t{venda['qtd']}\t{venda['preco']}\n"
        Label(frame_historico, text=historico, bg='#BEBEBE').place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.7)

    Button(frame_historico, text="Voltar ao menu anterior", command=frame_historico.destroy, bg='#C0C0C0').place(relx=0.02, rely=0.88, relwidth=0.3, relheight=0.1)

def calcular_total_vendido(frame, vendas):
    frame_total = Frame(frame, bd=8, bg='#BEBEBE', highlightbackground='black', highlightthickness=3)
    frame_total.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    total = sum(venda['qtd'] * venda['preco'] for venda in vendas)
    Label(frame_total, text=f"O TOTAL VENDIDO É: R${total:.2f}", bg='#BEBEBE').place(relx=0.15, rely=0.05, relwidth=0.7, relheight=0.1)

    Button(frame_total, text="Voltar ao menu anterior", command=frame_total.destroy, bg='#C0C0C0').place(relx=0.02, rely=0.88, relwidth=0.3, relheight=0.1)

def acessar_caixa(root):
    nome_arquivo_vendas = 'historico.txt'
    vendas = ler_vendas(nome_arquivo_vendas)
    estoque = ler_estoque("estoque.txt")

    class Application:
        def __init__(self, root):
            self.root = root
            self.vendas = vendas
            self.estoque = estoque
            self.nome_arquivo_vendas = nome_arquivo_vendas
            self.tela()
            self.frames()
            self.objetos_frame1()

        def tela(self):
            self.altura = altura
            self.largura = largura
            self.root.title("Caixa")
            self.root.configure(background='#363636')
            self.root.geometry(f"{self.largura}x{self.altura}")
            self.root.resizable(True, True)

        def frames(self):
            self.frame1 = Frame(self.root, bd=8, bg='#BEBEBE',
                                highlightbackground='black', highlightthickness=3)
            self.frame1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

        def objetos_frame1(self):
            Label(self.frame1, text="Caixa", font=('arialblack', 30), bg='#BEBEBE').place(relx=0.35, rely=0.05, relwidth=0.3, relheight=0.1)

            self.bt_caixa = Button(self.frame1, text="Registrar venda", command=self.form_registrar_venda, bg='#C0C0C0')
            self.bt_caixa.place(relx=0.35, rely=0.20, relwidth=0.3, relheight=0.1)

            self.bt_historico = Button(self.frame1, text='Ver histórico de vendas', command=lambda: historico_vendas(self.frame1, self.vendas), bg='#C0C0C0')
            self.bt_historico.place(relx=0.35, rely=0.35, relwidth=0.3, relheight=0.1)

            self.bt_total = Button(self.frame1, text='Calcular total vendido', command=lambda: calcular_total_vendido(self.frame1, self.vendas), bg='#C0C0C0')
            self.bt_total.place(relx=0.35, rely=0.50, relwidth=0.3, relheight=0.1)

            self.bt_sair = Button(self.frame1, text='Voltar ao menu principal', command=root.destroy, bg='#C0C0C0')
            self.bt_sair.place(relx=0.35, rely=0.65, relwidth=0.3, relheight=0.1)

        def form_registrar_venda(self):
            frame_registrar = Frame(self.frame1, bd=8, bg='#BEBEBE', highlightbackground='black', highlightthickness=3)
            frame_registrar.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

            Label(frame_registrar, text="Nome do Produto", bg='#BEBEBE').place(relx=0.15, rely=0.05, relwidth=0.2, relheight=0.05)
            entry_produto = Entry(frame_registrar)
            entry_produto.place(relx=0.35, rely=0.05, relwidth=0.5, relheight=0.05)

            Label(frame_registrar, text="Quantidade", bg='#BEBEBE').place(relx=0.15, rely=0.15, relwidth=0.2, relheight=0.05)
            entry_qtd = Entry(frame_registrar)
            entry_qtd.place(relx=0.35, rely=0.15, relwidth=0.5, relheight=0.05)

            Label(frame_registrar, text="Preço Unitário", bg='#BEBEBE').place(relx=0.15, rely=0.25, relwidth=0.2, relheight=0.05)
            entry_preco = Entry(frame_registrar)
            entry_preco.place(relx=0.35, rely=0.25, relwidth=0.5, relheight=0.05)

            bt_confirmar = Button(frame_registrar, text="Confirmar", command=lambda: registrar_venda(self.vendas, self.estoque, self.nome_arquivo_vendas, entry_produto, entry_qtd, entry_preco), bg='#C0C0C0')
            bt_confirmar.place(relx=0.35, rely=0.35, relwidth=0.3, relheight=0.1)

            bt_voltar = Button(frame_registrar, text="Voltar ao menu anterior", command=frame_registrar.destroy, bg='#C0C0C0')
            bt_voltar.place(relx=0.02, rely=0.88, relwidth=0.3, relheight=0.1)

    root = Tk()
    app = Application(root)
    root.mainloop()

# Exemplo de chamada à função principal
if __name__ == "__main__":
    acessar_caixa(None)
