import os
import csv
from datetime import datetime
from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter
from estoque import ler_estoque, escrever_estoque, salvar_historico_movimentacoes

altura, largura = 720, 1280

def ler_vendas(nome_arquivo):
    vendas = []
    if os.path.exists(nome_arquivo):
        arquivo = open(nome_arquivo, 'r', newline='')
        reader = csv.reader(arquivo)
        for linha in reader:
            if len(linha) == 5:
                data, produto, qtd, preco, meio_pagamento = linha
                vendas.append({"data": data, "produto": produto, "qtd": int(qtd), "preco": float(preco), "meio_pagamento": meio_pagamento})
            else:
                print(f"Linha ignorada por formatação incorreta: {linha}")
        arquivo.close()
    return vendas

def escrever_vendas(nome_arquivo, vendas):
    arquivo = open(nome_arquivo, 'w', newline='')
    writer = csv.writer(arquivo)
    for venda in vendas:
        preco_formatado = round(venda['preco'], 2)  # Limita o preço a dois pontos flutuantes após a vírgula
        writer.writerow([venda['data'], venda['produto'], venda['qtd'], preco_formatado, venda['meio_pagamento']])
    arquivo.close()

def atualizar_preco(entry_produto, entry_qtd, estoque, label_preco):
    # Obtém o nome do produto e a quantidade inserida
    produto_nome = entry_produto.get().upper()
    qtd = entry_qtd.get()
    # Procura o produto no estoque
    produto_estoque = next((item for item in estoque if item["nome"] == produto_nome), None)

    # Se o produto existir e a quantidade for um valor numérico inteiro e positivo
    if produto_estoque and qtd.isnumeric() and int(qtd) > 0:
        # Calcula o preço total e exibe no rótulo
        preco_total = produto_estoque["preco"] * int(qtd)
        label_preco.config(text=f"Preço: R${preco_total:.2f}")
    else:
        # Se o produto não existir ou a quantidade for inválida, exibe "-"
        label_preco.config(text="Preço: -")

def atualizar_valor_mensal(entry_qtd, entry_produto, entry_parcelas, estoque, label_valor_mensal, meio_pagamento):
    produto_nome = entry_produto.get().upper()
    qtd = entry_qtd.get()
    parcelas = entry_parcelas.get()

    # Verifica se é cartão de crédito e se tem mais de 12 parcelas
    if meio_pagamento == "Cartão de Crédito":
        if not parcelas.isnumeric() or int(parcelas) < 1 or int(parcelas) > 12:
            messagebox.showerror("Erro", "PARCELAMENTO DEVE SER DE 1 A 12 VEZES!")
            return

    # Procura o produto no estoque
    produto_estoque = None
    for item in estoque:
        if item["nome"] == produto_nome:
            produto_estoque = item
            break

    if produto_estoque and qtd.isnumeric() and int(qtd) > 0 and parcelas.isnumeric() and 1 <= int(parcelas) <= 12:
        preco_total = produto_estoque["preco"] * int(qtd)
        valor_mensal = preco_total / int(parcelas)
        label_valor_mensal.config(text=f"Valor Mensal: R${valor_mensal:.2f}")
    elif produto_estoque and qtd.isnumeric() and int(qtd) > 0 and parcelas.isnumeric() and int(parcelas) > 12:
        messagebox.showerror("Erro", "Número máximo de parcelas permitido é 12 para cartão de crédito.")
        label_valor_mensal.config(text="Valor Mensal: R$")
    else:
        label_valor_mensal.config(text="Valor Mensal: R$")

def encontrar_produto_estoque(produto_nome, estoque):
    for item in estoque:
        if item["nome"] == produto_nome:
            return item
    return None

def validar_quantidade(qtd):
    return qtd.isnumeric() and int(qtd) > 0

def validar_parcelas(parcelas):
    return parcelas.isnumeric() and 1 <= int(parcelas) <= 12

def registrar_venda(vendas, estoque, nome_arquivo_vendas, entry_produto, entry_qtd, entry_meio_pagamento, entry_parcelas, label_preco, label_valor_mensal):
    # Cria um dicionário para armazenar os dados da venda
    venda = {"data": None, "produto": None, "qtd": None, "preco": None, "meio_pagamento": None}

    # Obtém a data e hora atual
    venda["data"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Obtém o nome do produto inserido pelo usuário
    venda["produto"] = entry_produto.get().upper()

    if not venda["produto"].isalnum():
        messagebox.showerror("Erro", "Produtos com caracteres especiais não são registrados no estoque, tente novamente com nomes alfanuméricos.")
        return
    
    if venda["produto"][0].isnumeric():
        messagebox.showerror("Erro", "Produtos que começam com números não são registrados no estoque, tente novamente com outras combinações alfanuméricas.")

    # Verifica se o produto está no estoque
    produto_estoque = encontrar_produto_estoque(venda["produto"], estoque)
    if not produto_estoque:
        messagebox.showerror("Erro", "PRODUTO NÃO ENCONTRADO NO ESTOQUE!")
        return

    # Verifica se a quantidade inserida é um valor numérico inteiro e positivo
    qtd = entry_qtd.get()
    if not validar_quantidade(qtd):
        messagebox.showerror("Erro", "POR FAVOR INSIRA SOMENTE NÚMEROS, QUE SEJAM INTEIROS E POSITIVOS!")
        return
    venda["qtd"] = int(qtd)

    # Verifica se há quantidade suficiente no estoque
    if venda["qtd"] > produto_estoque["qtd"]:
        messagebox.showerror("Erro", "QUANTIDADE INSUFICIENTE NO ESTOQUE!")
        return

    # Calcula o preço da venda
    venda["preco"] = produto_estoque["preco"] * venda["qtd"]

    # Adiciona a escolha do meio de pagamento
    meio_pagamento = entry_meio_pagamento.get()
    if meio_pagamento == "Escolha a forma de pagamento":
        messagebox.showerror("Erro", "POR FAVOR ESCOLHA UM MEIO DE PAGAMENTO!")
        return
    venda["meio_pagamento"] = meio_pagamento

    # Verifica se o parcelamento é válido
    parcelas = entry_parcelas.get()
    if meio_pagamento == "Cartão de Crédito" and not validar_parcelas(parcelas):
        messagebox.showerror("Erro", "PARCELAMENTO DEVE SER DE 1 A 12 VEZES!")
        return

    # Atualiza o preço e valor mensal
    atualizar_preco(entry_produto, entry_qtd, estoque, label_preco)
    atualizar_valor_mensal(entry_qtd, entry_produto, entry_parcelas, estoque, label_valor_mensal, meio_pagamento)

    # Adiciona a venda ao histórico
    produto_estoque["qtd"] -= venda["qtd"]

    escrever_estoque("estoque.csv", estoque)
    vendas.append(venda)
    # Limita o histórico a 12 vendas
    if len(vendas) > 12:
        vendas = [venda]
    escrever_vendas(nome_arquivo_vendas, vendas)



    # Exibe uma mensagem de sucesso e limpa os campos de entrada
    messagebox.showinfo("Sucesso", "VENDA REGISTRADA COM SUCESSO!")
    entry_produto.delete(0, END)
    entry_qtd.delete(0, END)
    entry_meio_pagamento.set('Escolha a forma de pagamento')
    entry_parcelas.delete(0, END)
    label_preco.config(text="")
    label_valor_mensal.config(text="")


def exibir_graficos(frame, vendas):
    # Criação de um frame para exibir os gráficos
    frame_graficos = Frame(frame, bd=8, bg='#E8E8E8', highlightbackground='#363636', highlightthickness=3)
    frame_graficos.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    if not vendas:
        mostrar_mensagem_erro(frame_graficos)
        return

    # Processamento dos dados de vendas
    produtos_vendidos, meios_pagamento = processar_dados_vendas(vendas)

    # Obtenção dos produtos mais vendidos e meios de pagamento mais utilizados
    produtos_mais_vendidos = produtos_vendidos.most_common()
    meios_pagamento_utilizados = meios_pagamento.most_common()

    # Criação e exibição dos gráficos
    criar_grafico_pizza(frame_graficos, produtos_mais_vendidos, 'Produtos mais vendidos por quantidade', 0.02)
    criar_grafico_pizza(frame_graficos, meios_pagamento_utilizados, 'Meios de pagamento mais utilizados', 0.52)

    # Botão para voltar ao menu anterior
    Button(frame_graficos, text="Voltar ao menu anterior", command=lambda: frame_graficos.destroy(), bg='#363636', fg='white').place(relx=0.35, rely=0.88, relwidth=0.3, relheight=0.1)

def mostrar_mensagem_erro(frame_graficos):
    Label(frame_graficos, text="NENHUM DADO COMPUTADO...", bg='#E8E8E8').place(relx=0.15, rely=0.05, relwidth=0.7, relheight=0.1)
    Button(frame_graficos, text="Voltar ao menu anterior", command=lambda: frame_graficos.destroy(), bg='#363636', fg='white').place(relx=0.35, rely=0.88, relwidth=0.3, relheight=0.1)

def processar_dados_vendas(vendas):
    produtos_vendidos = Counter()
    meios_pagamento = Counter()

    for venda in vendas:
        produto = venda.get("produto")
        meio_pagamento = venda.get("meio_pagamento")
        quantidade = venda.get("qtd", 1)

        if produto and isinstance(quantidade, int) and quantidade > 0:
            produtos_vendidos[produto] += quantidade

        if meio_pagamento == 'Crédito Parcelado':
            meio_pagamento = 'Cartão de Crédito'

        if meio_pagamento:
            meios_pagamento[meio_pagamento] += 1

    return produtos_vendidos, meios_pagamento

def criar_grafico_pizza(frame_graficos, dados, titulo, relx):
    fig = plt.figure(figsize=(4, 4), facecolor='#E8E8E8')
    ax = fig.add_subplot(111)

    if dados:
        labels, valores = zip(*dados)
        ax.pie(valores, labels=labels, autopct='%1.1f%%', startangle=140)
    else:
        ax.pie([1], labels=["Sem dados"], startangle=140)

    ax.set_title(titulo)
    ax.set_facecolor('#E8E8E8')

    canvas = FigureCanvasTkAgg(fig, master=frame_graficos)
    canvas.draw()
    canvas.get_tk_widget().place(relx=relx, rely=0.02, relwidth=0.45, relheight=0.86)

# Função para exibir o histórico de vendas
def historico_vendas(frame, vendas):
    frame_historico = Frame(frame, bd=8, bg='#E8E8E8', highlightbackground='#363636', highlightthickness=3)
    frame_historico.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    if len(vendas) == 0:
        Label(frame_historico, text="NENHUMA VENDA REGISTRADA...", bg='#E8E8E8').place(relx=0.15, rely=0.05, relwidth=0.7, relheight=0.1)
    else:
        # Cabeçalhos da tabela
        Label(frame_historico, text="DATA", bg='#E8E8E8').place(relx=0.05, rely=0.05, relwidth=0.15, relheight=0.05)
        Label(frame_historico, text="PRODUTO", bg='#E8E8E8').place(relx=0.20, rely=0.05, relwidth=0.25, relheight=0.05)
        Label(frame_historico, text="QTD", bg='#E8E8E8').place(relx=0.45, rely=0.05, relwidth=0.10, relheight=0.05)
        Label(frame_historico, text="PREÇO UNITÁRIO", bg='#E8E8E8').place(relx=0.55, rely=0.05, relwidth=0.20, relheight=0.05)
        Label(frame_historico, text="MEIO PAGAMENTO", bg='#E8E8E8').place(relx=0.75, rely=0.05, relwidth=0.20, relheight=0.05)

        total = 0
        for i, venda in enumerate(vendas):
            # Exibe cada valor na sua posição correspondente
            Label(frame_historico, text=venda['data'], bg='#E8E8E8').place(relx=0.05, rely=0.1 + i*0.05, relwidth=0.15, relheight=0.05)
            Label(frame_historico, text=venda['produto'], bg='#E8E8E8').place(relx=0.20, rely=0.1 + i*0.05, relwidth=0.25, relheight=0.05)
            Label(frame_historico, text=venda['qtd'], bg='#E8E8E8').place(relx=0.45, rely=0.1 + i*0.05, relwidth=0.10, relheight=0.05)
            Label(frame_historico, text=f"{venda['preco']:.2f}", bg='#E8E8E8').place(relx=0.55, rely=0.1 + i*0.05, relwidth=0.20, relheight=0.05)
            Label(frame_historico, text=venda['meio_pagamento'], bg='#E8E8E8').place(relx=0.75, rely=0.1 + i*0.05, relwidth=0.20, relheight=0.05)
            total += venda['qtd'] * venda['preco']
        
        # Exibe o total vendido
        Label(frame_historico, text=f"TOTAL VENDIDO: R${total:.2f}", bg='#E8E8E8').place(relx=0.05, rely=0.1 + len(vendas)*0.05, relwidth=0.9, relheight=0.05)

        # Botão para exibir os gráficos
        Button(frame_historico, text="Exibir Gráficos", command=lambda: exibir_graficos(frame, vendas), bg='#363636', fg='white').place(relx=0.02, rely=0.88, relwidth=0.3, relheight=0.1)

    # Botão para voltar ao menu anterior
    Button(frame_historico, text="Voltar ao menu anterior", command=frame_historico.destroy, bg='#363636', fg='white').place(relx=0.35, rely=0.88, relwidth=0.3, relheight=0.1)

# Função para acessar o caixa
def acessar_caixa(application):
    nome_arquivo_vendas = 'historico.csv'
    # Lê o histórico de vendas e o estoque do arquivo
    vendas = ler_vendas(nome_arquivo_vendas)
    estoque = ler_estoque("estoque.csv")

    # Classe principal da aplicação
    class CaixaApp:
        def __init__(self, root):
            self.root = root
            self.vendas = vendas
            self.estoque = estoque
            self.nome_arquivo_vendas = nome_arquivo_vendas
            self.frames()
            self.objetos_frame1()

        # Criação dos frames
        def frames(self):
            self.frame1 = Frame(self.root, bd=8, bg='#E8E8E8',
                                highlightbackground='#363636', highlightthickness=3)
            self.frame1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

        # Adiciona os widgets ao frame principal
        def objetos_frame1(self):
            Label(self.frame1, text="Caixa", font=('Arial Black', 30), bg='#E8E8E8').place(relx=0.35, rely=0.05, relwidth=0.3, relheight=0.1)

            self.bt_caixa = Button(self.frame1, text="Registrar Venda", command=self.form_registrar_venda, bg='#363636', fg='white')
            self.bt_caixa.place(relx=0.35, rely=0.20, relwidth=0.3, relheight=0.1)

            self.bt_historico = Button(self.frame1, text='Ver Histórico de Vendas', command=lambda: historico_vendas(self.frame1, self.vendas), bg='#363636', fg='white')
            self.bt_historico.place(relx=0.35, rely=0.35, relwidth=0.3, relheight=0.1)

            self.bt_grafico = Button(self.frame1, text='Ver Gráficos', command=lambda: exibir_graficos(self.frame1, self.vendas), bg='#363636', fg='white')
            self.bt_grafico.place(relx=0.35, rely=0.50, relwidth=0.3, relheight=0.1)

            self.bt_sair = Button(self.frame1, text='Voltar ao Menu Principal', command=self.voltar_menu_principal, bg='#363636', fg='white')
            self.bt_sair.place(relx=0.35, rely=0.65, relwidth=0.3, relheight=0.1)

        # Criação do formulário para registrar uma venda

        def form_registrar_venda(self):
            # Função para atualizar o preço com base no produto e na quantidade
            def atualizar_preco(entry_produto, entry_qtd, estoque, label_preco):
                # Lógica para calcular o preço com base no produto e quantidade (exemplo)
                preco_unitario = estoque.get(entry_produto.get(), 0)  # Substitua pela lógica adequada
                quantidade = int(entry_qtd.get()) if entry_qtd.get().isdigit() else 0
                preco_total = preco_unitario * quantidade
                label_preco.config(text=f"Preço: R${preco_total:.2f}")

            # Função para limpar os campos do formulário
            def limpar_campos(entry_produto, entry_qtd, entry_meio_pagamento, label_preco):
                entry_produto.delete(0, 'end')
                entry_qtd.delete(0, 'end')
                entry_meio_pagamento.set("Escolha a forma de pagamento")
                label_preco.config(text="Preço: -")

            # Função para atualizar visibilidade de parcelas e valor mensal
            def atualizar_parcelas(*args):
                if meio_pagamento_var.get() == "Cartão de Crédito":
                    frame_parcelas.place(relx=0.35, rely=0.35, relwidth=0.5, relheight=0.1)
                    label_valor_mensal.place(relx=0.35, rely=0.45, relwidth=0.5, relheight=0.05)
                    entry_parcelas.bind("<KeyRelease>", lambda event: atualizar_valor_mensal(entry_qtd, entry_produto, entry_parcelas, self.estoque, label_valor_mensal, meio_pagamento_var))
                else:
                    frame_parcelas.place_forget()
                    label_valor_mensal.place_forget()

            # Criar o frame principal para o formulário
            frame_registrar = Frame(self.frame1, bd=8, bg='#E8E8E8', highlightbackground='#363636', highlightthickness=3)
            frame_registrar.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

            # Widgets do formulário
            Label(frame_registrar, text="Nome do Produto", bg='#E8E8E8').place(relx=0.15, rely=0.05, relwidth=0.2, relheight=0.05)
            entry_produto = Entry(frame_registrar)
            entry_produto.place(relx=0.35, rely=0.05, relwidth=0.5, relheight=0.05)

            Label(frame_registrar, text="Quantidade", bg='#E8E8E8').place(relx=0.15, rely=0.12, relwidth=0.2, relheight=0.05)
            entry_qtd = Entry(frame_registrar)
            entry_qtd.place(relx=0.35, rely=0.12, relwidth=0.5, relheight=0.05)

            label_preco = Label(frame_registrar, text="Preço: -", bg='#E8E8E8')
            label_preco.place(relx=0.35, rely=0.19, relwidth=0.5, relheight=0.05)

            meio_pagamento_var = StringVar(frame_registrar)
            meio_pagamento_var.set("Escolha a forma de pagamento")
            entry_meio_pagamento = OptionMenu(frame_registrar, meio_pagamento_var, "Dinheiro", "Cartão de Crédito", "Cartão de Débito", "Pix")
            entry_meio_pagamento.place(relx=0.35, rely=0.26, relwidth=0.5, relheight=0.05)

            frame_parcelas = Frame(frame_registrar, bg='#E8E8E8')
            frame_parcelas.place(relx=0.35, rely=0.35, relwidth=0.5, relheight=0.1)

            Label(frame_parcelas, text="Número de Parcelas:", bg='#E8E8E8').place(relx=0.0, rely=0.0, relwidth=0.5, relheight=0.5)
            entry_parcelas = Entry(frame_parcelas)
            entry_parcelas.place(relx=0.5, rely=0.0, relwidth=0.5, relheight=0.5)

            label_valor_mensal = Label(frame_registrar, text="Valor Mensal: R$", bg='#E8E8E8')

            # Associar a função de atualização ao trace do meio de pagamento
            meio_pagamento_var.trace_add("write", atualizar_parcelas)

            # Botões
            Button(frame_registrar, text="Voltar ao menu anterior", command=frame_registrar.destroy, bg='#363636', fg='white').place(relx=0.02, rely=0.88, relwidth=0.3, relheight=0.1)
            Button(frame_registrar, text="Limpar Campos", command=lambda: limpar_campos(entry_produto, entry_qtd, meio_pagamento_var, label_preco), bg='#363636', fg='white').place(relx=0.35, rely=0.88, relwidth=0.3, relheight=0.1)
            Button(frame_registrar, text="Confirmar", command=lambda: registrar_venda(self.vendas, self.estoque, "historico.csv", entry_produto, entry_qtd, meio_pagamento_var, entry_parcelas, label_preco, label_valor_mensal), bg='#363636', fg='white').place(relx=0.68, rely=0.88, relwidth=0.3, relheight=0.1)

        def voltar_menu_principal(self):
            self.frame1.place_forget()  # Oculta o frame atual
            application.frame_atual.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)  # Mostra o frame anterior
        
        def limpar_campos(self, entry_produto, entry_qtd, meio_pagamento_var, label_preco, label_valor_mensal=None, entry_parcelas=None):
            entry_produto.delete(0, END)
            entry_qtd.delete(0, END)
            meio_pagamento_var.set("Escolha a forma de pagamento")
            label_preco.config(text="Preço: -")
            # Limpa o campo de parcelas e valor mensal, se necessário
            entry_parcelas.delete(0, END)
            label_valor_mensal.config(text="Valor Mensal: R$")
    
    CaixaApp(application.root)

class MainApp:
    def __init__(self, root):
        self.root = root
        self.tela()
        self.frames()
        self.objetos_frame1()

    def tela(self):
        self.altura = altura
        self.largura = largura
        self.root.title("Gerenciamento de Caixa")
        self.root.configure(background='#363636')
        self.root.geometry(f"{self.largura}x{self.altura}")
        self.root.resizable(True, True)

    def frames(self):
        self.frame1 = Frame(self.root, bd=8, bg='#E8E8E8',
                            highlightbackground='#363636', highlightthickness=3)
        self.frame1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    def objetos_frame1(self):
        self.bt_acessar_caixa = Button(self.frame1, text="Acessar Caixa", command=lambda: acessar_caixa(self), bg='#363636', fg='white')
        self.bt_acessar_caixa.place(relx=0.35, rely=0.40, relwidth=0.3, relheight=0.1)
        self.bt_sair = Button(self.frame1, text='Sair', command=self.root.destroy, bg='#363636', fg='white')
        self.bt_sair.place(relx=0.35, rely=0.55, relwidth=0.3, relheight=0.1)

# Exemplo de chamada à função principal
if __name__ == "__main__":
    root = Tk()
    app = MainApp(root)
    root.mainloop()