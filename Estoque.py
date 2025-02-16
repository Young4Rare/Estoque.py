import tkinter as tk
from tkinter import ttk, messagebox

# Configuração do arquivo de notas
NOTAS_ARQUIVO = "estoque.txt"

def carregar_estoque():
    estoque = []
    try:
        with open(NOTAS_ARQUIVO, "r") as file:
            for line in file:
                estoque.append(line.strip().split(","))
    except FileNotFoundError:
        pass
    return estoque

def salvar_estoque(estoque):
    with open(NOTAS_ARQUIVO, "w") as file:
        for item in estoque:
            file.write(",".join(item) + "\n")

def adicionar_mercadoria():
    nome = entry_nome.get()
    quantidade = entry_quantidade.get()
    if nome and quantidade:
        estoque = carregar_estoque()
        estoque.append([str(len(estoque) + 1), nome, quantidade])
        salvar_estoque(estoque)
        atualizar_lista()
        messagebox.showinfo("Sucesso", "Mercadoria adicionada com sucesso!")
    else:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")

def remover_mercadoria():
    item_selecionado = tree.selection()
    if item_selecionado:
        estoque = carregar_estoque()
        ids_remover = [tree.item(item, "values")[0] for item in item_selecionado]
        estoque = [item for item in estoque if item[0] not in ids_remover]
        salvar_estoque(estoque)
        atualizar_lista()
        messagebox.showinfo("Sucesso", "Mercadoria removida com sucesso!")
    else:
        messagebox.showwarning("Aviso", "Selecione um item para remover!")

def atualizar_lista():
    for item in tree.get_children():
        tree.delete(item)
    estoque = carregar_estoque()
    for row in estoque:
        tree.insert("", "end", values=row)

# Interface gráfica
root = tk.Tk()
root.title("DETECH - Controle de Estoque")
root.geometry("600x400")

frame_form = tk.Frame(root)
frame_form.pack(pady=10)

tk.Label(frame_form, text="Nome:").grid(row=0, column=0)
entry_nome = tk.Entry(frame_form)
entry_nome.grid(row=0, column=1)

tk.Label(frame_form, text="Quantidade:").grid(row=1, column=0)
entry_quantidade = tk.Entry(frame_form)
entry_quantidade.grid(row=1, column=1)

tk.Button(frame_form, text="Adicionar", command=adicionar_mercadoria).grid(row=2, column=0, columnspan=2, pady=5)

tree = ttk.Treeview(root, columns=("ID", "Nome", "Quantidade"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nome", text="Nome")
tree.heading("Quantidade", text="Quantidade")
tree.pack(expand=True, fill="both")

tk.Button(root, text="Remover", command=remover_mercadoria).pack(pady=5)

atualizar_lista()
root.mainloop()
