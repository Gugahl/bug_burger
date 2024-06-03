import os
import tkinter as tk
from tkinter import messagebox

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

def acessar_estoque_gui():
    root = tk.Tk()
    root.title("Estoque")
    root.geometry("1280x720")

    estoque = ler_estoque("estoque.txt")

    def adicionar_produto():
        produto = entry_produto.get().upper()
        qtd = entry_qtd.get()

        if not produto or not qtd:
            messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos!")
            return

        qtd = int(qtd)

        existe = False
        for item in estoque:
            if item["nome"] == produto:
                item["qtd"] += qtd
                existe = True
                break

        if not existe:
            estoque.append({"nome": produto, "qtd": qtd})

        escrever_estoque("estoque.txt", estoque)
        messagebox.showinfo("Produto Adicionado", f"{qtd} unidades de {produto} foram adicionadas ao estoque!")
        entry_produto.delete(0, tk.END)
        entry_qtd.delete(0, tk.END)

    def remover_produto():
        produto = entry_produto.get().upper()

        if not produto:
            messagebox.showwarning("Campo Vazio", "Por favor, insira o nome do produto a ser removido!")
            return

        for item in estoque:
            if item["nome"] == produto:
                estoque.remove(item)
                escrever_estoque("estoque.txt", estoque)
                messagebox.showinfo("Produto Removido", f"O produto {produto} foi removido do estoque!")
                entry_produto.delete(0, tk.END)
                return

        messagebox.showwarning("Produto Não Encontrado", f"O produto {produto} não foi encontrado no estoque!")

    def ver_estoque():
        if not estoque:
            messagebox.showinfo("Estoque Vazio", "O estoque está vazio!")
            return

        mensagem = "Estoque:\n"
        for item in estoque:
            mensagem += f"{item['nome']}: {item['qtd']} unidades\n"
        messagebox.showinfo("Estoque", mensagem)

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

    btn_adicionar = tk.Button(frame, text="Adicionar Produto", width=20, command=adicionar_produto)
    btn_adicionar.grid(row=2, columnspan=2, padx=10, pady=10)

    btn_remover = tk.Button(frame, text="Remover Produto", width=20, command=remover_produto)
    btn_remover.grid(row=3, columnspan=2, padx=10, pady=10)

    btn_ver = tk.Button(frame, text="Ver Estoque", width=20, command=ver_estoque)
    btn_ver.grid(row=4, columnspan=2, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    acessar_estoque_gui()
