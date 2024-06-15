import os
import csv
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Define as dimensões da janela
altura = 720
largura = 1280
historico_movimentacoes = []

# Função para adicionar um produto ao estoque
def adicionar_produto(estoque, nome_arquivo, entry_nome, entry_qtd, entry_preco):
    nome = entry_nome.get().upper()
    qtd = entry_qtd.get()
    preco = entry_preco.get()

    # Verificar se o nome é válido
    if not nome:
        messagebox.showerror("ERRO!", "O NOME DO PRODUTO NÃO PODE SER VAZIO!")
        return
    for c in nome:
        tem_letra = False
        if c.isalnum():
            tem_letra = True
            break
    if not tem_letra:
        messagebox.showerror("ERRO!", "O NOME DO PRODUTO NÃO PODE CONTER SOMENTE ESPAÇOS OU CARACTERES ESPECIAIS!")
        return
    if not nome.replace(" ", "").isalnum():
        messagebox.showerror("ERRO!", "O NOME DO PRODUTO NÃO PODE CONTER CARACTERES ESPECIAIS!")
        return
    if nome.isnumeric():
        messagebox.showerror("ERRO!", "O NOME DO PRODUTO NÃO PODE SER COMPOSTO APENAS DE NÚMEROS!")
        return
    if nome[0].isdigit():
        messagebox.showerror("ERRO!", "O NOME DO PRODUTO NÃO PODE COMEÇAR COM UM NÚMERO!")
        return

    # Verificar se a quantidade é válida
    if not qtd.isnumeric() or int(qtd) <= 0:
        messagebox.showerror("ERRO!", "POR FAVOR INSIRA SOMENTE NÚMEROS INTEIROS E POSITIVOS!!!!")
        return
    qtd = int(qtd)

    # Verificar se o preço é válido
    preco = preco.replace(",", ".")
    if not preco.replace(".", "", 1).isdigit() or float(preco) <= 0:
        messagebox.showerror("ERRO!", "POR FAVOR INSIRA SOMENTE VALORES NUMÉRICOS E ACIMA DE ZERO!")
        return
    preco = float(preco)

    # Criar o dicionário do produto
    produto = {"nome": nome, "qtd": qtd, "preco": preco}

    historico_movimentacoes = []

    # Atualizar estoque
    if len(estoque) == 0:
        estoque.append(produto)
    else:
        existe = False
        for i in estoque:
            if i["nome"] == produto["nome"]:
                existe = True
                i["qtd"] += produto["qtd"]
                i["preco"] = produto["preco"]
                break
        if not existe:
            estoque.append(produto)

    # Registrar movimentação no histórico
    historico_movimentacoes.append({
        "tipo": "entrada",
        "produto": produto["nome"],
        "quantidade": produto["qtd"],
        "preco_unitario": produto["preco"]
    })

    # Escrever o estoque atualizado no arquivo
    escrever_estoque(nome_arquivo, estoque)
    messagebox.showinfo("SUCESSO!", f"{produto['qtd']} UNIDADES DE '{produto['nome']}' DE PREÇO 'R${produto['preco']}' FORAM ADICIONADAS AO ESTOQUE")
    entry_nome.delete(0, END)
    entry_qtd.delete(0, END)
    entry_preco.delete(0, END)

# Função para remover um produto do estoque
def remover_produto(estoque, nome_arquivo, entry_nome):
    nome = entry_nome.get().upper()

    # Verificar se o estoque está vazio
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

# Função para obter e exibir o estoque
def obter_estoque(estoque):
    if len(estoque) == 0:
        messagebox.showinfo("Informação", "ESTOQUE VAZIO...")
    else:
        estoque_str = "PRODUTO\t\tESTOQUE\t\tPREÇO\n"
        for i in estoque:
            estoque_str += f"{i['nome']}\t\t{i['qtd']}\t\tR${i['preco']}\n"
        messagebox.showinfo("Estoque", estoque_str)

# Função para ler o estoque de um arquivo CSV
def ler_estoque(nome_arquivo):
    estoque = []
    arquivo = open(nome_arquivo, 'r')
    leitor_csv = csv.DictReader(arquivo)
    for linha in leitor_csv:
        estoque.append({"nome": linha['nome'], "qtd": int(linha['qtd']), "preco": float(linha['preco'])})
    arquivo.close()
    return estoque if estoque else []

# Função para escrever o estoque em um arquivo CSV
def escrever_estoque(nome_arquivo, estoque):
    arquivo = open(nome_arquivo, 'w', newline='')
    cabecalho = ['nome', 'qtd', 'preco']
    escritor_csv = csv.DictWriter(arquivo, fieldnames=cabecalho)
    escritor_csv.writeheader()
    for item in estoque:
        escritor_csv.writerow(item)
    arquivo.close()

def organizar_estoque(frame, estoque):
    frame_estoque = Frame(frame, bd=8, bg='#E8E8E8', highlightbackground='#363636', highlightthickness=3)
    frame_estoque.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    if len(estoque) == 0:
        Label(frame_estoque, text="ESTOQUE VAZIO...", bg='#E8E8E8').place(relx=0.15, rely=0.05, relwidth=0.7, relheight=0.1)
    else:
        # Cabeçalhos da tabela
        Label(frame_estoque, text="PRODUTO", bg='#E8E8E8').place(relx=0.05, rely=0.05, relwidth=0.45, relheight=0.05)
        Label(frame_estoque, text="ESTOQUE", bg='#E8E8E8').place(relx=0.50, rely=0.05, relwidth=0.20, relheight=0.05)
        Label(frame_estoque, text="PREÇO", bg='#E8E8E8').place(relx=0.70, rely=0.05, relwidth=0.25, relheight=0.05)

        for i, produto in enumerate(estoque):
            # Exibe cada valor na sua posição correspondente
            Label(frame_estoque, text=produto['nome'], bg='#E8E8E8').place(relx=0.05, rely=0.1 + i*0.05, relwidth=0.45, relheight=0.05)
            Label(frame_estoque, text=produto['qtd'], bg='#E8E8E8').place(relx=0.50, rely=0.1 + i*0.05, relwidth=0.20, relheight=0.05)
            Label(frame_estoque, text=f"R${produto['preco']:.2f}", bg='#E8E8E8').place(relx=0.70, rely=0.1 + i*0.05, relwidth=0.25, relheight=0.05)

    # Botão para voltar ao menu anterior
    Button(frame_estoque, text="Voltar ao menu anterior", command=frame_estoque.destroy, bg='#363636', fg='white').place(relx=0.35, rely=0.88, relwidth=0.3, relheight=0.1)

# Função para acessar e gerenciar o estoque
def acessar_estoque(application):
    nome_arquivo = "estoque.csv"
    estoque = ler_estoque(nome_arquivo)
    
    class EstoqueApp:
        def __init__(self, root):
            self.root = root
            self.estoque = ler_estoque(nome_arquivo)
            self.nome_arquivo = nome_arquivo
            self.criar_frames()
            self.objetos_frame1()

        def criar_frames(self):
            self.frame1 = Frame(self.root, bd=8, bg='#E8E8E8',
                                highlightbackground='#363636', highlightthickness=3)
            self.frame1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

        def objetos_frame1(self):
            Label(self.frame1, text="Estoque", font=('Arial', 30), bg='#E8E8E8', fg='#363636').place(relx=0.35, rely=0.05, relwidth=0.3, relheight=0.1)
            
            self.bt_adicionar = Button(self.frame1, text="Adicionar produto", command=self.form_adicionar_produto, bg='#363636', fg='white')
            self.bt_adicionar.place(relx=0.35, rely=0.20, relwidth=0.3, relheight=0.1)
            self.bt_adicionar.config(font=('Arial', 12))
            
            self.bt_remover = Button(self.frame1, text='Remover produto', command=self.form_remover_produto, bg='#363636', fg='white')
            self.bt_remover.place(relx=0.35, rely=0.35, relwidth=0.3, relheight=0.1)
            self.bt_remover.config(font=('Arial', 12))
            
            self.bt_ver_estoque = Button(self.frame1, text='Ver estoque', command=self.ver_estoque, bg='#363636', fg='white')
            self.bt_ver_estoque.place(relx=0.35, rely=0.50, relwidth=0.3, relheight=0.1)
            self.bt_ver_estoque.config(font=('Arial', 12))
            
            self.bt_sair = Button(self.frame1, text='Voltar ao menu principal', command=self.voltar_menu_principal, bg='#363636', fg='white')
            self.bt_sair.place(relx=0.35, rely=0.65, relwidth=0.3, relheight=0.1)
            self.bt_sair.config(font=('Arial', 12))

        def form_adicionar_produto(self):
            self.frame_adicionar = Frame(self.frame1, bd=8, bg='#E8E8E8', highlightbackground='#363636', highlightthickness=3)
            self.frame_adicionar.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

            Label(self.frame_adicionar, text="Nome do Produto", bg='#E8E8E8', fg='#363636').place(relx=0.15, rely=0.05, relwidth=0.2, relheight=0.05)
            self.entry_nome = Entry(self.frame_adicionar)
            self.entry_nome.place(relx=0.35, rely=0.05, relwidth=0.5, relheight=0.05)
            
            Label(self.frame_adicionar, text="Quantidade", bg='#E8E8E8', fg='#363636').place(relx=0.15, rely=0.15, relwidth=0.2, relheight=0.05)
            self.entry_qtd = Entry(self.frame_adicionar)
            self.entry_qtd.place(relx=0.35, rely=0.15, relwidth=0.5, relheight=0.05)
            
            Label(self.frame_adicionar, text="Preço", bg='#E8E8E8', fg='#363636').place(relx=0.15, rely=0.25, relwidth=0.2, relheight=0.05)
            self.entry_preco = Entry(self.frame_adicionar)
            self.entry_preco.place(relx=0.35, rely=0.25, relwidth=0.5, relheight=0.05)
            
            self.bt_confirmar = Button(self.frame_adicionar, text="Confirmar", command=lambda: adicionar_produto(self.estoque, self.nome_arquivo, self.entry_nome, self.entry_qtd, self.entry_preco), bg='#363636', fg='white')
            self.bt_confirmar.place(relx=0.35, rely=0.35, relwidth=0.3, relheight=0.1)
            self.bt_confirmar.config(font=('Arial', 12))
            
            Button(self.frame_adicionar, text="Voltar ao menu anterior", command=self.frame_adicionar.destroy, bg='#363636', fg='white').place(relx=0.02, rely=0.88, relwidth=0.3, relheight=0.1)
            
            Button(self.frame_adicionar, text="Limpar campos", command=self.limpar_campos_adicionar, bg='#363636', fg='white').place(relx=0.35, rely=0.88, relwidth=0.3, relheight=0.1)
            
            Button(self.frame_adicionar, text="Gerar PDF", command=self.gerar_pdf, bg='#363636', fg='white').place(relx=0.68, rely=0.88, relwidth=0.3, relheight=0.1)

        def form_remover_produto(self):
            self.frame_remover = Frame(self.frame1, bd=8, bg='#E8E8E8', highlightbackground='#363636', highlightthickness=3)
            self.frame_remover.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
            
            Label(self.frame_remover, text="Nome do Produto", bg='#E8E8E8', fg='#363636').place(relx=0.15, relwidth=0.2, rely=0.05, relheight=0.05)
            self.entry_nome = Entry(self.frame_remover)
            self.entry_nome.place(relx=0.35, rely=0.05, relwidth=0.5, relheight=0.05)
            
            Button(self.frame_remover, text="Confirmar", command=lambda: remover_produto(self.estoque, self.nome_arquivo, self.entry_nome), bg='#363636', fg='white').place(relx=0.35, rely=0.15, relwidth=0.3, relheight=0.1)
            
            Button(self.frame_remover, text="Limpar campos", command=self.limpar_campos_remover, bg='#363636', fg='white').place(relx=0.35, rely=0.88, relwidth=0.3, relheight=0.1)

            Button(self.frame_remover, text="Voltar ao menu anterior", command=self.frame_remover.destroy, bg='#363636', fg='white').place(relx=0.02, rely=0.88, relwidth=0.3, relheight=0.1)

        def ver_estoque(self):
            organizar_estoque(self.frame1, self.estoque)

        def voltar_menu_principal(self):
            self.frame1.place_forget()  # Oculta o frame atual
            application.frame_atual.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)  # Mostra o frame anterior

        def limpar_campos_adicionar(self):
            self.entry_nome.delete(0, END)
            self.entry_qtd.delete(0, END)
            self.entry_preco.delete(0, END)

        def limpar_campos_remover(self):
            self.entry_nome.delete(0, END)

        def gerar_pdf(self):
            messagebox.showinfo("Gerar PDF", "Lógica para gerar PDF ainda não implementada! (Somente na próxima atualização)")

    EstoqueApp(application.root)

# Classe principal do aplicativo
class MainApp:
    def __init__(self, root):
        self.root = root
        self.tela()
        self.frames()
        self.objetos_frame1()

    def tela(self):
        self.altura = altura
        self.largura = largura
        self.root.title("Gerenciamento de Estoque")
        self.root.configure(background='#363636')
        self.root.geometry(f"{self.largura}x{self.altura}")
        self.root.resizable(True, True)

    def frames(self):
        self.frame1 = Frame(self.root, bd=8, bg='#E8E8E8',
                            highlightbackground='#363636', highlightthickness=3)
        self.frame1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    def objetos_frame1(self):
        self.bt_acessar_estoque = Button(self.frame1, text="Acessar Estoque", command=lambda: acessar_estoque(self), bg='#363636', fg='white')
        self.bt_acessar_estoque.place(relx=0.35, rely=0.40, relwidth=0.3, relheight=0.1)
        self.bt_acessar_estoque.config(font=('Arial', 12))
        self.bt_sair = Button(self.frame1, text='Sair', command=self.root.destroy, bg='#363636', fg='white')
        self.bt_sair.place(relx=0.35, rely=0.55, relwidth=0.3, relheight=0.1)
        self.bt_sair.config(font=('Arial', 12))

# Exemplo de chamada à função principal
if __name__ == "__main__":
    root = Tk()
    app = MainApp(root)
    root.mainloop()
