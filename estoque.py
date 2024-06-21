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
    global historico_movimentacoes
    nome = entry_nome.get().upper()
    qtd = entry_qtd.get()
    preco = entry_preco.get()

    # Verificar se o nome é válido
    if not nome:
        messagebox.showerror("ERRO!", "O NOME DO PRODUTO NÃO PODE SER VAZIO!")
        return
    tem_letra = False
    for c in nome:
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
            messagebox.showerror("ERRO!", f"NÃO HÁ PRODUTO CHAMADO '{nome}' NO ESTOQUE")

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
    if not os.path.exists(nome_arquivo):
        return estoque
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

def organizar_estoque(self):
    frame_verestoque = Frame(self.root, bd=8, bg='#E8E8E8', highlightbackground='#363636', highlightthickness=3)
    frame_verestoque.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    nome_arquivo_estoque = "estoque.csv"
    estoque = ler_estoque(nome_arquivo_estoque)

    if len(estoque) == 0:
        Label(frame_verestoque, text="ESTOQUE VAZIO...", bg='#E8E8E8').place(relx=0.15, rely=0.05, relwidth=0.7, relheight=0.1)
    else:
        # Cabeçalhos da tabela
        Label(frame_verestoque, text="PRODUTO", bg='#E8E8E8').place(relx=0.05, rely=0.05, relwidth=0.45, relheight=0.05)
        Label(frame_verestoque, text="ESTOQUE", bg='#E8E8E8').place(relx=0.50, rely=0.05, relwidth=0.20, relheight=0.05)
        Label(frame_verestoque, text="PREÇO", bg='#E8E8E8').place(relx=0.70, rely=0.05, relwidth=0.25, relheight=0.05)

        for i, produto in enumerate(estoque):
            # Exibe cada valor na sua posição correspondente
            Label(frame_verestoque, text=produto['nome'], bg='#E8E8E8').place(relx=0.05, rely=0.1 + i*0.05, relwidth=0.45, relheight=0.05)
            Label(frame_verestoque, text=produto['qtd'], bg='#E8E8E8').place(relx=0.50, rely=0.1 + i*0.05, relwidth=0.20, relheight=0.05)
            Label(frame_verestoque, text=f"R${produto['preco']:.2f}", bg='#E8E8E8').place(relx=0.70, rely=0.1 + i*0.05, relwidth=0.25, relheight=0.05)

    # Botão para voltar ao menu anterior
    Button(frame_verestoque, text="Voltar ao menu anterior", command=frame_verestoque.destroy, bg='#363636', fg='white').place(relx=0.35, rely=0.88, relwidth=0.3, relheight=0.1)

# Função para acessar e gerenciar o estoque
def form_adicionar_produto(self):
    frame_adicionar = Frame(self.root, bd=8, bg='#E8E8E8', highlightbackground='#363636', highlightthickness=3)
    frame_adicionar.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    nome_arquivo_estoque = "estoque.csv"
    estoque = ler_estoque(nome_arquivo_estoque)

    Label(frame_adicionar, text="Nome do Produto", bg='#E8E8E8', fg='#363636').place(relx=0.15, rely=0.05, relwidth=0.2, relheight=0.05)
    entry_nome = Entry(frame_adicionar)
    entry_nome.place(relx=0.35, rely=0.05, relwidth=0.5, relheight=0.05)
    
    Label(frame_adicionar, text="Quantidade", bg='#E8E8E8', fg='#363636').place(relx=0.15, rely=0.15, relwidth=0.2, relheight=0.05)
    entry_qtd = Entry(frame_adicionar)
    entry_qtd.place(relx=0.35, rely=0.15, relwidth=0.5, relheight=0.05)
    
    Label(frame_adicionar, text="Preço", bg='#E8E8E8', fg='#363636').place(relx=0.15, rely=0.25, relwidth=0.2, relheight=0.05)
    entry_preco = Entry(frame_adicionar)
    entry_preco.place(relx=0.35, rely=0.25, relwidth=0.5, relheight=0.05)
    
    bt_confirmar = Button(frame_adicionar, text="Confirmar", command=lambda: adicionar_produto(estoque, nome_arquivo_estoque, entry_nome, entry_qtd, entry_preco), bg='#363636', fg='white')
    bt_confirmar.place(relx=0.35, rely=0.35, relwidth=0.3, relheight=0.1)
    bt_confirmar.config(font=('Arial', 12))
    
    Button(frame_adicionar, text="Voltar ao menu anterior", command=frame_adicionar.destroy, bg='#363636', fg='white').place(relx=0.02, rely=0.88, relwidth=0.3, relheight=0.1)
    
    Button(frame_adicionar, text="Limpar campos", command=lambda: limpar_campos_adicionar(entry_nome, entry_qtd, entry_preco), bg='#363636', fg='white').place(relx=0.35, rely=0.88, relwidth=0.3, relheight=0.1)
    
    Button(frame_adicionar, text="Gerar PDF", command=lambda: gerar_pdf(self), bg='#363636', fg='white').place(relx=0.68, rely=0.88, relwidth=0.3, relheight=0.1)

def form_remover_produto(self):
    frame_remover = Frame(self.root, bd=8, bg='#E8E8E8', highlightbackground='#363636', highlightthickness=3)
    frame_remover.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    nome_arquivo_estoque = "estoque.csv"
    estoque = ler_estoque(nome_arquivo_estoque)

    Label(frame_remover, text="Nome do Produto", bg='#E8E8E8', fg='#363636').place(relx=0.15, relwidth=0.2, rely=0.05, relheight=0.05)
    entry_nome = Entry(frame_remover)
    entry_nome.place(relx=0.35, rely=0.05, relwidth=0.5, relheight=0.05)

    Button(frame_remover, text="Confirmar", command=lambda: remover_produto(estoque, nome_arquivo_estoque, entry_nome), bg='#363636', fg='white').place(relx=0.35, rely=0.15, relwidth=0.3, relheight=0.1)
    
    Button(frame_remover, text="Limpar campos", command=lambda: limpar_campos_remover(entry_nome), bg='#363636', fg='white').place(relx=0.35, rely=0.88, relwidth=0.3, relheight=0.1)

    Button(frame_remover, text="Voltar ao menu anterior", command=frame_remover.destroy, bg='#363636', fg='white').place(relx=0.02, rely=0.88, relwidth=0.3, relheight=0.1)

def ver_estoque(frame_verestoque):
    organizar_estoque(frame_verestoque)

def voltar_menu_principal_estoque(frame_estoque, frame_main):
    frame_estoque.place_forget()  # Oculta o frame atual
    frame_main.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)  # Mostra o frame anterior

def limpar_campos_adicionar(entry_nome, entry_qtd, entry_preco):
    entry_nome.delete(0, END)
    entry_qtd.delete(0, END)
    entry_preco.delete(0, END)

def limpar_campos_remover(entry_nome):
    entry_nome.delete(0, END)

def gerar_pdf(self):
    messagebox.showinfo("Gerar PDF", "Lógica para gerar PDF ainda não implementada! (Somente na próxima atualização)")
