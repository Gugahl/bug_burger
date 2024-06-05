import tkinter as tk
from tkinter import messagebox
from caixa import registrar_venda, calcular_total_vendido, obter_historico_vendas
from estoque import adicionar_produto, remover_produto, obter_estoque

estoque_insumos = []

def adicionar_insumo(nome, quantidade):
    global estoque_insumos
    for item in estoque_insumos:
        if item['nome'] == nome:
            item['quantidade'] += quantidade
            return f"{quantidade} unidades de '{nome}' foram adicionadas ao estoque."
    estoque_insumos.append({'nome': nome, 'quantidade': quantidade})
    return f"{quantidade} unidades de '{nome}' foram adicionadas ao estoque."

def remover_insumo(nome):
    global estoque_insumos
    for item in estoque_insumos:
        if item['nome'] == nome:
            estoque_insumos.remove(item)
            return f"{nome} foi removido do estoque."
    return f"{nome} não encontrado no estoque."

def obter_insumos():
    return estoque_insumos

def tela_principal(root):
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("1280x720")
    tk.Label(root, text="Sistema de Gerenciamento", font=("Helvetica", 24)).pack(pady=30)
    tk.Button(root, text="Acessar Caixa", command=lambda: acessar_caixa(root), width=30, height=2, font=("Helvetica", 14)).pack(pady=10)
    tk.Button(root, text="Acessar Estoque", command=lambda: acessar_estoque(root), width=30, height=2, font=("Helvetica", 14)).pack(pady=10)
    tk.Button(root, text="Sair", command=root.quit, width=30, height=2, font=("Helvetica", 14)).pack(pady=10)

def gerenciar_ingredientes_tela(root):
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("1280x720")
    tk.Label(root, text="Gerenciar Ingredientes", font=("Helvetica", 24)).pack(pady=30)
    tk.Button(root, text="Adicionar Insumo", command=lambda: adicionar_insumo_tela(root), width=30, height=2, font=("Helvetica", 14)).pack(pady=10)
    tk.Button(root, text="Remover Insumo", command=lambda: remover_insumo_tela(root), width=30, height=2, font=("Helvetica", 14)).pack(pady=10)
    tk.Button(root, text="Ver Insumos", command=lambda: ver_insumos_tela(root), width=30, height=2, font=("Helvetica", 14)).pack(pady=10)
    tk.Button(root, text="Voltar ao Menu Principal", command=lambda: tela_principal(root), width=30, height=2, font=("Helvetica", 14)).pack(pady=10)

def adicionar_insumo_tela(root):
    def confirmar_adicao():
        nome_insumo = entry_nome_insumo.get().upper()
        quantidade = entry_quantidade.get()

        if not quantidade.isdigit() or int(quantidade) <= 0:
            messagebox.showerror("Erro", "Por favor insira somente números inteiros e positivos para a quantidade.")
            return

        quantidade = int(quantidade)
        mensagem = adicionar_insumo(nome_insumo, quantidade)
        messagebox.showinfo("Resultado", mensagem)
        janela_adicao.destroy()

    janela_adicao = tk.Toplevel(root)
    janela_adicao.title("Adicionar Insumo")

    tk.Label(janela_adicao, text="Nome do Insumo:").pack(pady=5)
    entry_nome_insumo = tk.Entry(janela_adicao)
    entry_nome_insumo.pack(pady=5)

    tk.Label(janela_adicao, text="Quantidade:").pack(pady=5)
    entry_quantidade = tk.Entry(janela_adicao)
    entry_quantidade.pack(pady=5)

    tk.Button(janela_adicao, text="Confirmar", command=confirmar_adicao).pack(pady=20)

def remover_insumo_tela(root):
    def confirmar_remocao():
        nome_insumo = entry_nome_insumo.get().upper()
        mensagem = remover_insumo(nome_insumo)
        messagebox.showinfo("Resultado", mensagem)
        janela_remocao.destroy()

    janela_remocao = tk.Toplevel(root)
    janela_remocao.title("Remover Insumo")

    tk.Label(janela_remocao, text="Nome do Insumo:").pack(pady=5)
    entry_nome_insumo = tk.Entry(janela_remocao)
    entry_nome_insumo.pack(pady=5)

    tk.Button(janela_remocao, text="Confirmar", command=confirmar_remocao).pack(pady=20)

def ver_insumos_tela(root):
    insumos = obter_insumos()

    janela_insumos = tk.Toplevel(root)
    janela_insumos.title("Ver Insumos")

    if not insumos:
        tk.Label(janela_insumos, text="Estoque de insumos vazio.").pack(pady=20)
    else:
        tk.Label(janela_insumos, text="INSUMO\t\tQUANTIDADE").pack(pady=5)
        for item in insumos:
            insumo_info = f"{item['nome']}\t\t{item['quantidade']}"
            tk.Label(janela_insumos, text=insumo_info).pack()

def acessar_caixa(root):
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("1280x720")
    tk.Label(root, text="Caixa", font=("Helvetica", 24)).pack(pady=30)
    tk.Button(root, text="Registrar Venda", command=lambda: registrar_venda_tela(root), width=30, height=2, font=("Helvetica", 14)).pack(pady=10)
    tk.Button(root, text="Ver Histórico de Vendas", command=lambda: ver_historico_vendas_tela(root), width=30, height=2, font=("Helvetica", 14)).pack(pady=10)
    tk.Button(root, text="Calcular Total Vendido", command=lambda: calcular_total_vendido_tela(root), width=30, height=2, font=("Helvetica", 14)).pack(pady=10)
    tk.Button(root, text="Voltar ao Menu Principal", command=lambda: tela_principal(root), width=30, height=2, font=("Helvetica", 14)).pack(pady=10)

def registrar_venda_tela(root):
    def confirmar_venda():
        nome_produto = entry_nome_produto.get().upper()
        quantidade = entry_quantidade.get()
        preco = entry_preco.get()

        if not quantidade.isdigit() or int(quantidade) <= 0:
            messagebox.showerror("Erro", "Por favor insira somente números inteiros e positivos para a quantidade.")
            return

        if not preco.replace('.', '', 1).isdigit() or float(preco) <= 0:
            messagebox.showerror("Erro", "Por favor insira um valor positivo para o preço.")
            return

        quantidade = int(quantidade)
        preco = float(preco)

        mensagem = registrar_venda(nome_produto, quantidade, preco)
        messagebox.showinfo("Resultado", mensagem)
        janela_registro.destroy()

    janela_registro = tk.Toplevel(root)
    janela_registro.title("Registrar Venda")

    tk.Label(janela_registro, text="Nome do Produto:").pack(pady=5)
    entry_nome_produto = tk.Entry(janela_registro)
    entry_nome_produto.pack(pady=5)

    tk.Label(janela_registro, text="Quantidade:").pack(pady=5)
    entry_quantidade = tk.Entry(janela_registro)
    entry_quantidade.pack(pady=5)

    tk.Label(janela_registro, text="Preço Unitário:").pack(pady=5)
    entry_preco = tk.Entry(janela_registro)
    entry_preco.pack(pady=5)

    tk.Button(janela_registro, text="Confirmar", command=confirmar_venda).pack(pady=20)

def ver_historico_vendas_tela(root):
    vendas = obter_historico_vendas()

    janela_historico = tk.Toplevel(root)
    janela_historico.title("Histórico de Vendas")

    if not vendas:
        tk.Label(janela_historico, text="Nenhuma venda registrada.").pack(pady=20)
    else:
        tk.Label(janela_historico, text="DATA\t\t\tPRODUTO\t\tQTD\tPREÇO UNITÁRIO").pack(pady=5)
        for venda in vendas:
            venda_info = f"{venda['data']}\t{venda['produto']}\t\t{venda['qtd']}\t{venda['preco']}"
            tk.Label(janela_historico, text=venda_info).pack()

def calcular_total_vendido_tela(root):
    total = calcular_total_vendido()
    messagebox.showinfo("Total Vendido", f"O total vendido é: R${total:.2f}")

def acessar_estoque(root):
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("1280x720")
    tk.Label(root, text="Estoque", font=("Helvetica", 24)).pack(pady=30)
    tk.Button(root, text="Adicionar Produto", command=lambda: adicionar_produto_tela(root), width=30, height=2, font=("Helvetica", 14)).pack(pady=10)
    tk.Button(root, text="Remover Produto", command=lambda: remover_produto_tela(root), width=30, height=2, font=("Helvetica", 14)).pack(pady=10)
    tk.Button(root, text="Ver Estoque", command=lambda: ver_estoque_tela(root), width=30, height=2, font=("Helvetica", 14)).pack(pady=10)
    tk.Button(root, text="Gerenciamento de Insumos", command=lambda: gerenciar_ingredientes_tela(root), width=30, height=2, font=("Helvetica", 14)).pack(pady=10)
    tk.Button(root, text="Voltar ao Menu Principal", command=lambda: tela_principal(root), width=30, height=2, font=("Helvetica", 14)).pack(pady=10)


def adicionar_produto_tela(root):
    def confirmar_adicao():
        nome_produto = entry_nome_produto.get().upper()
        preco = entry_preco.get()

        if not preco.replace('.', '', 1).isdigit() or float(preco) <= 0:
            messagebox.showerror("Erro", "Por favor insira um preço válido.")
            return

        preco = float(preco)
        mensagem = adicionar_produto(nome_produto, preco)
        messagebox.showinfo("Resultado", mensagem)
        janela_adicao.destroy()

    janela_adicao = tk.Toplevel(root)
    janela_adicao.title("Adicionar Produto")

    tk.Label(janela_adicao, text="Nome do Produto:").pack(pady=5)
    entry_nome_produto = tk.Entry(janela_adicao)
    entry_nome_produto.pack(pady=5)

    tk.Label(janela_adicao, text="Preço:").pack(pady=5)
    entry_preco = tk.Entry(janela_adicao)
    entry_preco.pack(pady=5)

    tk.Button(janela_adicao, text="Confirmar", command=confirmar_adicao).pack(pady=20)

def remover_produto_tela(root):
    def confirmar_remocao():
        nome_produto = entry_nome_produto.get().upper()
        mensagem = remover_produto(nome_produto)
        messagebox.showinfo("Resultado", mensagem)
        janela_remocao.destroy()

    janela_remocao = tk.Toplevel(root)
    janela_remocao.title("Remover Produto")

    tk.Label(janela_remocao, text="Nome do Produto:").pack(pady=5)
    entry_nome_produto = tk.Entry(janela_remocao)
    entry_nome_produto.pack(pady=5)

    tk.Button(janela_remocao, text="Confirmar", command=confirmar_remocao).pack(pady=20)

def ver_estoque_tela(root):
    estoque = obter_estoque()

    janela_estoque = tk.Toplevel(root)
    janela_estoque.title("Ver Estoque")

    if not estoque:
        tk.Label(janela_estoque, text="Estoque vazio.").pack(pady=20)
    else:
        tk.Label(janela_estoque, text="PRODUTO\t\tPREÇO").pack(pady=5)
        for item in estoque:
            produto_info = f"{item['nome']}\t\t{item['preco']}"
            tk.Label(janela_estoque, text=produto_info).pack()

if __name__ == "__main__":
    root = tk.Tk()
    tela_principal(root)
    root.mainloop()
