import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from estoque import ler_estoque, escrever_estoque

def ler_vendas(nome_arquivo):
    vendas = []
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, 'r') as arquivo:
            for linha in arquivo:
                data, produto, qtd, preco = linha.strip().split(',')
                vendas.append({"data": data, "produto": produto, "qtd": int(qtd), "preco": float(preco)})
    return vendas

def escrever_vendas(nome_arquivo, vendas):
    with open(nome_arquivo, 'w') as arquivo:
        for venda in vendas:
            arquivo.write(f"{venda['data']},{venda['produto']},{venda['qtd']},{venda['preco']}\n")

def acessar_caixa_gui():
    root = tk.Tk()
    root.title("Caixa")
    root.geometry("800x600")

    estoque = ler_estoque("estoque.txt")
    vendas = ler_vendas("historico.txt")

    def registrar_venda():
        produto = entry_produto.get().upper()
        qtd = entry_qtd.get()
        preco_unitario = entry_preco_unitario.get()

        if not produto or not qtd or not preco_unitario:
            messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos!")
            return

        qtd = int(qtd)
        preco_unitario = float(preco_unitario)

        produto_estoque = next((item for item in estoque if item["nome"] == produto), None)
        if not produto_estoque:
            messagebox.showerror("Produto Não Encontrado", "O produto não foi encontrado no estoque!")
            return

        if qtd > produto_estoque["qtd"]:
            messagebox.showerror("Quantidade Insuficiente", "Quantidade insuficiente no estoque!")
            return

        venda = {"data": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "produto": produto, "qtd": qtd, "preco": preco_unitario}
        vendas.append(venda)
        escrever_vendas("historico.txt", vendas)

        produto_estoque["qtd"] -= qtd
        if produto_estoque["qtd"] == 0:
            estoque.remove(produto_estoque)
        escrever_estoque("estoque.txt", estoque)

        messagebox.showinfo("Venda Registrada", "Venda registrada com sucesso!")
        entry_produto.delete(0, tk.END)
        entry_qtd.delete(0, tk.END)
        entry_preco_unitario.delete(0, tk.END)

    def ver_historico():
        if not vendas:
            messagebox.showinfo("Histórico de Vendas", "Nenhuma venda registrada ainda.")
            return

        historico = "DATA\t\t\tPRODUTO\t\tQTD\tPREÇO UNITÁRIO\n"
        for venda in vendas:
            historico += f"{venda['data']}\t{venda['produto']}\t{venda['qtd']}\t{venda['preco']}\n"
        messagebox.showinfo("Histórico de Vendas", historico)

    def calcular_total_vendido():
        total = sum(venda['qtd'] * venda['preco'] for venda in vendas)
        messagebox.showinfo("Total Vendido", f"O TOTAL VENDIDO É: R${total:.2f}")

    frame = tk.Frame(root)
    frame.pack(pady=20)

    label_produto = tk.Label(frame, text="Produto:")
    label_produto.grid(row=0, column=0, padx=10, pady=5)
    entry_produto = tk.Entry(frame)
    entry_produto.grid(row=0, column=1, padx=10, pady=5)

    label_qtd = tk.Label(frame, text="Quantidade:")
    label_qtd.grid(row=1, column=0, padx=10, pady=5)
    entry_qtd = tk.Entry(frame)
    entry_qtd.grid(row=1, column=1, padx=10, pady=5)

    label_preco_unitario = tk.Label(frame, text="Preço Unitário:")
    label_preco_unitario.grid(row=2, column=0, padx=10, pady=5)
    entry_preco_unitario = tk.Entry(frame)
    entry_preco_unitario.grid(row=2, column=1, padx=10, pady=5)

    btn_registrar = tk.Button(frame, text="Registrar Venda", width=15, command=registrar_venda)
    btn_registrar.grid(row=3, columnspan=2, padx=10, pady=10)

    btn_historico = tk.Button(frame, text="Ver Histórico de Vendas", width=20, command=ver_historico)
    btn_historico.grid(row=4, columnspan=2, padx=10, pady=10)

    btn_total = tk.Button(frame, text="Calcular Total Vendido", width=20, command=calcular_total_vendido)
    btn_total.grid(row=5, columnspan=2, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    acessar_caixa_gui()
