import tkinter as tk
from tkinter import messagebox
from estoque import *
from caixa import *

def main_gui():
    root = tk.Tk()
    root.title("Sistema de Gestão")
    root.geometry("1080x720")

    def abrir_caixa():
        acessar_caixa_gui()

    def abrir_estoque():
        acessar_estoque_gui()

    frame = tk.Frame(root)
    frame.pack(pady=20)

    btn_caixa = tk.Button(frame, text="Acessar Caixa", width=30, height=3, command=abrir_caixa)
    btn_caixa.grid(row=0, column=0, padx=10, pady=5)

    btn_estoque = tk.Button(frame, text="Acessar Estoque", width=30, height=3, command=abrir_estoque)
    btn_estoque.grid(row=1, column=0, padx=10, pady=5)

    btn_sair = tk.Button(frame, text="Sair", width=30, height=3, command=root.destroy)
    btn_sair.grid(row=2, column=0, padx=10, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main_gui()
