import os
import csv
from datetime import datetime
from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter
from estoque import ler_estoque, escrever_estoque  # Importando diretamente as funções necessárias do módulo estoque

altura = 720
largura = 1280

# Função para ler o histórico de vendas do arquivo CSV
def ler_vendas(nome_arquivo):
    vendas = []
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, 'r', newline='') as arquivo:
            reader = csv.reader(arquivo)
            for linha in reader:
                if len(linha) == 5:
                    data, produto, qtd, preco, meio_pagamento = linha
                    vendas.append({"data": data, "produto": produto, "qtd": int(qtd), "preco": float(preco), "meio_pagamento": meio_pagamento})
                else:
                    print(f"Linha ignorada por formatação incorreta: {linha}")
    return vendas

# Função para escrever o histórico de vendas no arquivo CSV
def escrever_vendas(nome_arquivo, vendas):
    with open(nome_arquivo, 'w', newline='') as arquivo:
        writer = csv.writer(arquivo)
        for venda in vendas:
            preco_formatado = round(venda['preco'], 2)  # Limita o preço a dois pontos flutuantes após a vírgula
            writer.writerow([venda['data'], venda['produto'], venda['qtd'], preco_formatado, venda['meio_pagamento']])

# Função para registrar uma venda
def registrar_venda(vendas, estoque, nome_arquivo_vendas, entry_produto, entry_qtd, entry_meio_pagamento, label_preco):
    # Cria um dicionário para armazenar os dados da venda
    venda = {"data": None, "produto": None, "qtd": None, "preco": None, "meio_pagamento": None}
    # Obtém a data e hora atual
    venda["data"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Obtém o nome do produto inserido pelo usuário
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

    # Atualiza a quantidade no estoque
    produto_estoque["qtd"] -= venda["qtd"]
    if produto_estoque["qtd"] == 0:
        estoque.remove(produto_estoque)
    escrever_estoque("estoque.csv", estoque)

    # Calcula o preço da venda
    venda["preco"] = produto_estoque["preco"]

    # Adiciona a escolha do meio de pagamento
    meio_pagamento = entry_meio_pagamento.get()
    venda["meio_pagamento"] = meio_pagamento

    # Adiciona a venda ao histórico
    vendas.append(venda)
    # Limita o histórico a 12 vendas
    if len(vendas) > 12:
        vendas = [venda]
    escrever_vendas(nome_arquivo_vendas, vendas)

    # Exibe uma mensagem de sucesso e limpa os campos de entrada
    messagebox.showinfo("Sucesso", "VENDA REGISTRADA COM SUCESSO!")
    entry_produto.delete(0, END)
    entry_qtd.delete(0, END)
    label_preco.config(text="")

# Função para atualizar o preço com base no produto e na quantidade inseridos
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

# Função para exibir os gráficos do caixa
def exibir_graficos(frame, vendas):
    # Criação de um frame para exibir os gráficos
    frame_graficos = Frame(frame, bd=8, bg='#E8E8E8', highlightbackground='#363636', highlightthickness=3)
    frame_graficos.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    # Verificação se o arquivo de histórico existe e se há dados de vendas
    if not os.path.exists('historico.csv') or not vendas:
        # Exibir mensagem de erro se não houver dados
        Label(frame_graficos, text="NENHUM DADO COMPUTADO...", bg='#E8E8E8').place(relx=0.15, rely=0.05, relwidth=0.7, relheight=0.1)
        # Botão para voltar ao menu anterior
        Button(frame_graficos, text="Voltar ao menu anterior", command=lambda: frame_graficos.destroy(), bg='#363636', fg='white').place(relx=0.35, rely=0.88, relwidth=0.3, relheight=0.1)
        return
    
    # Inicialização dos contadores para produtos vendidos e meios de pagamento
    produtos_vendidos = Counter()
    meios_pagamento = Counter()

    # Processamento dos dados de vendas
    for venda in vendas:
        produto = venda.get("produto")
        meio_pagamento = venda.get("meio_pagamento")
        quantidade = venda.get("qtd", 1)
        
        # Verificação e adição da quantidade vendida ao contador de produtos
        if produto and isinstance(quantidade, int) and quantidade > 0:
            produtos_vendidos[produto] += quantidade
        # Adição do meio de pagamento ao contador
        if meio_pagamento:
            meios_pagamento[meio_pagamento] += 1
    
    # Obtenção dos produtos mais vendidos e meios de pagamento mais utilizados
    produtos_mais_vendidos = produtos_vendidos.most_common()
    meios_pagamento_utilizados = meios_pagamento.most_common()
    
    # Criação e exibição do gráfico de pizza para produtos mais vendidos
    fig1 = plt.figure(figsize=(4, 4), facecolor='#E8E8E8')
    ax1 = fig1.add_subplot(111)
    
    if produtos_mais_vendidos:
        # Dados para o gráfico de pizza
        produtos, quantidades = zip(*produtos_mais_vendidos)
        ax1.pie(quantidades, labels=produtos, autopct='%1.1f%%', startangle=140)
    else:
        # Exibir mensagem se não houver dados
        ax1.pie([1], labels=["Sem dados"], startangle=140)

    ax1.set_title('Produtos mais vendidos por quantidade')
    ax1.set_facecolor('#E8E8E8')  # Define a cor de fundo do gráfico
    
    # Adicionar o gráfico ao frame
    canvas1 = FigureCanvasTkAgg(fig1, master=frame_graficos)
    canvas1.draw()
    canvas1.get_tk_widget().place(relx=0.02, rely=0.02, relwidth=0.45, relheight=0.86)
    
    # Criação e exibição do gráfico de pizza para meios de pagamento
    fig2 = plt.figure(figsize=(4, 4), facecolor='#E8E8E8')
    ax2 = fig2.add_subplot(111)
    
    if meios_pagamento_utilizados:
        # Dados para o gráfico de pizza
        meios, frequencias = zip(*meios_pagamento_utilizados)
        ax2.pie(frequencias, labels=meios, autopct='%1.1f%%', startangle=140)
    else:
        # Exibir mensagem se não houver dados
        ax2.pie([1], labels=["Sem dados"], startangle=140)

    ax2.set_title('Meios de pagamento mais utilizados')
    ax2.set_facecolor('#E8E8E8')  # Define a cor de fundo do gráfico
    
    # Adicionar o gráfico ao frame
    canvas2 = FigureCanvasTkAgg(fig2, master=frame_graficos)
    canvas2.draw()
    canvas2.get_tk_widget().place(relx=0.52, rely=0.02, relwidth=0.45, relheight=0.86)

    # Botão para voltar ao menu anterior
    Button(frame_graficos, text="Voltar ao menu anterior", command=lambda: frame_graficos.destroy(), bg='#363636', fg='white').place(relx=0.35, rely=0.88, relwidth=0.3, relheight=0.1)

# Função para exibir o histórico de vendas
def historico_vendas(frame, vendas):
    frame_historico = Frame(frame, bd=8, bg='#E8E8E8', highlightbackground='#363636', highlightthickness=3)
    frame_historico.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    if len(vendas) == 0:
        Label(frame_historico, text="NENHUMA VENDA REGISTRADA...", bg='#E8E8E8').place(relx=0.15, rely=0.05, relwidth=0.7, relheight=0.1)
    else:
        historico = "DATA\t\t\tPRODUTO\t\t\tQTD\tPREÇO UNITÁRIO\tMEIO PAGAMENTO\n"  # Ajuste de espaçamento
        total = 0
        for venda in vendas:
            # Constrói a string de histórico com os dados de cada venda
            historico += f"{venda['data']}\t{venda['produto']}\t\t\t{venda['qtd']}\t{venda['preco']:.2f}\t\t{venda['meio_pagamento']}\n"  # Ajuste de espaçamento
            total += venda['qtd'] * venda['preco']
        historico += f"\nTOTAL VENDIDO: R${total:.2f}\n"
        # Exibe o histórico no frame
        Label(frame_historico, text=historico, bg='#E8E8E8').place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.7)

        # Botão para exibir os gráficos
        Button(frame_historico, text="Exibir Gráficos", command=lambda: exibir_graficos(frame_historico, vendas), bg='#363636', fg='white').place(relx=0.02, rely=0.88, relwidth=0.3, relheight=0.1)

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
            frame_registrar = Frame(self.frame1, bd=8, bg='#E8E8E8', highlightbackground='#363636', highlightthickness=3)
            frame_registrar.place(relx=0.02, relwidth=0.96, relheight=0.96)

            Label(frame_registrar, text="Nome do Produto", bg='#E8E8E8').place(relx=0.15, rely=0.05, relwidth=0.2, relheight=0.05)
            entry_produto = Entry(frame_registrar)
            entry_produto.place(relx=0.35, rely=0.05, relwidth=0.5, relheight=0.05)
            
            # Rótulo para exibir o preço do produto
            label_preco = Label(frame_registrar, text="Preço: -", bg='#E8E8E8')
            label_preco.place(relx=0.35, rely=0.12, relwidth=0.5, relheight=0.05)
            
            Label(frame_registrar, text="Quantidade", bg='#E8E8E8').place(relx=0.15, rely=0.20, relwidth=0.2, relheight=0.05)
            entry_qtd = Entry(frame_registrar)
            entry_qtd.place(relx=0.35, rely=0.20, relwidth=0.5, relheight=0.05)
            
            # Função para atualizar o preço quando o nome do produto ou a quantidade são alterados
            entry_produto.bind("<KeyRelease>", lambda event: atualizar_preco(entry_produto, entry_qtd, self.estoque, label_preco))
            entry_qtd.bind("<KeyRelease>", lambda event: atualizar_preco(entry_produto, entry_qtd, self.estoque, label_preco))

            Label(frame_registrar, text="Meio de Pagamento", bg='#E8E8E8').place(relx=0.15, rely=0.30, relwidth=0.2, relheight=0.05)
            entry_meio_pagamento = StringVar(frame_registrar)
            entry_meio_pagamento.set("À vista")
            pagamentos = ["À vista", "PIX", "Cartão de débito", "Cartão de crédito 1x", "Cartão de crédito 2x", "Cartão de crédito 3x",
                          "Cartão de crédito 4x", "Cartão de crédito 5x", "Cartão de crédito 6x", "Cartão de crédito 7x", 
                          "Cartão de crédito 8x", "Cartão de crédito 9x", "Cartão de crédito 10x", "Cartão de crédito 11x", "Cartão de crédito 12x"]
            OptionMenu(frame_registrar, entry_meio_pagamento, *pagamentos).place(relx=0.35, rely=0.30, relwidth=0.5, relheight=0.05)

            bt_confirmar = Button(frame_registrar, text="Confirmar", command=lambda: registrar_venda(self.vendas, self.estoque, self.nome_arquivo_vendas, entry_produto, entry_qtd, entry_meio_pagamento, label_preco), bg='#363636', fg='white')
            bt_confirmar.place(relx=0.35, rely=0.40, relwidth=0.3, relheight=0.1)

            Button(frame_registrar, text="Limpar Campos", command=lambda: self.limpar_campos(entry_produto, entry_qtd, entry_meio_pagamento, label_preco), bg='#363636', fg='white').place(relx=0.02, rely=0.88, relwidth=0.3, relheight=0.1)

            Button(frame_registrar, text="Voltar ao menu anterior", command=frame_registrar.destroy, bg='#363636', fg='white').place(relx=0.35, rely=0.88, relwidth=0.3, relheight=0.1)

        def voltar_menu_principal(self):
            self.frame1.place_forget()  # Oculta o frame atual
            application.frame_atual.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)  # Mostra o frame anterior
        
        def limpar_campos(self, entry_produto, entry_qtd, entry_meio_pagamento, label_preco):
            entry_produto.delete(0, END)
            entry_qtd.delete(0, END)
            entry_meio_pagamento.set("à vista")
            label_preco.config(text="Preço: -")
    
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



